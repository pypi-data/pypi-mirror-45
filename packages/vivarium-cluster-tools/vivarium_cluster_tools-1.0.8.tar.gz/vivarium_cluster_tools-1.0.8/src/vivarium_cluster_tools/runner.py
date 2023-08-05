import os
import atexit
import math
import tempfile
import shutil
import socket
import subprocess
from pathlib import Path
from time import sleep, time
from types import SimpleNamespace

from loguru import logger
import numpy as np
import pandas as pd

from vivarium.framework.configuration import build_model_specification
from vivarium.framework.results_writer import ResultsWriter
from vivarium.framework.utilities import collapse_nested_dict
from vivarium_public_health.dataset_manager import Artifact, parse_artifact_path_config

from vivarium_cluster_tools.branches import Keyspace
from vivarium_cluster_tools import utilities, globals as vtc_globals
from .registry import RegistryManager

drmaa = utilities.get_drmaa()


def init_job_template(jt, peak_memory, sge_log_directory, worker_log_directory,
                      project, job_name, worker_settings_file):
    launcher = tempfile.NamedTemporaryFile(mode='w', dir='.', prefix='vivarium_cluster_tools_launcher_',
                                           suffix='.sh', delete=False)
    atexit.register(lambda: os.remove(launcher.name))
    output_dir = str(worker_settings_file.resolve().parent)
    launcher.write(f'''
    export VIVARIUM_LOGGING_DIRECTORY={worker_log_directory}
    export PYTHONPATH={output_dir}:$PYTHONPATH
    
    {shutil.which('rq')} worker -c {worker_settings_file.stem} --name ${{JOB_ID}}.${{SGE_TASK_ID}} --burst -w "vivarium_cluster_tools.distributed_worker.ResilientWorker" --exception-handler "vivarium_cluster_tools.distributed_worker.retry_handler" vivarium

    ''')
    launcher.close()

    jt.workingDirectory = os.getcwd()
    jt.remoteCommand = shutil.which('sh')
    jt.args = [launcher.name]
    jt.outputPath = f":{sge_log_directory}"
    jt.errorPath = f":{sge_log_directory}"
    sge_cluster = utilities.get_cluster_name()
    jt.jobEnvironment = {
        'LC_ALL': 'en_US.UTF-8',
        'LANG': 'en_US.UTF-8',
        'SGE_CLUSTER_NAME': sge_cluster,
    }
    jt.joinFiles = True
    jt.nativeSpecification = utilities.get_uge_specification(peak_memory, project, job_name)
    return jt


def get_random_free_port():
    # NOTE: this implementation is vulnerable to rare race conditions where some other process gets the same
    # port after we free our socket but before we use the port number we got. Should be so rare in practice
    # that it doesn't matter.
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def launch_redis(port):
    try:
        # inline config for redis server.
        redis_process = subprocess.Popen(["redis-server", "--port", f"{port}",
                                          "--timeout", "2",
                                          "--protected-mode", "no"], stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise OSError("In order for redis to launch you need both the redis client and the python bindings. "
                      "You seem to be missing the redis client.  Do 'conda install redis' and try again. If "
                      "failures continue you may need to download redis yourself, make it and add it to PATH.")
    atexit.register(redis_process.kill)
    return redis_process


def launch_redis_processes(num_processes):
    hostname = socket.getfqdn()
    redis_ports = []
    for i in range(num_processes):
        port = get_random_free_port()
        logger.info(f'Starting Redis Broker at {hostname}:{port}')
        launch_redis(port)
        redis_ports.append((hostname, port))

    redis_urls = [f'redis://{hostname}:{port}' for hostname, port in redis_ports]
    worker_config = f"import random\nredis_urls = {redis_urls}\nREDIS_URL = random.choice(redis_urls)\n\n"
    return worker_config, redis_ports


def start_cluster(drmaa_session, num_workers, peak_memory, sge_log_directory, worker_log_directory,
                  project, worker_settings_file, job_name="vivarium"):
    s = drmaa_session
    jt = init_job_template(s.createJobTemplate(), peak_memory, sge_log_directory,
                           worker_log_directory, project, job_name, worker_settings_file)
    if num_workers:
        job_ids = s.runBulkJobs(jt, 1, num_workers, 1)
        array_job_id = job_ids[0].split('.')[0]

        def kill_jobs():
            if "drmaa" not in dir():
                # FIXME: The global drmaa should be available here.
                # This is maybe a holdover from old code?
                # Maybe something to do with atexit?
                drmaa = utilities.get_drmaa()

            try:
                s.control(array_job_id, drmaa.JobControlAction.TERMINATE)
            # FIXME: Hack around issue where drmaa.errors sometimes doesn't
            # exist.
            except Exception as e:
                if 'There are no jobs registered' in str(e):
                    # This is the case where all our workers have already shut down
                    # on their own, which isn't actually an error.
                    pass
                elif 'Discontinued delete' in str(e):
                    # sge has already cleaned up some of the jobs.
                    pass
                else:
                    raise

        atexit.register(kill_jobs)


class RunContext:
    def __init__(self, arguments):
        # TODO This constructor has side effects (it creates directories under some circumstances) which is weird.
        # It should probably be split into two phases with the side effects in the second phase.

        self.cluster_project = arguments.project
        self.peak_memory = arguments.peak_memory
        self.number_already_completed = 0
        self.results_writer = ResultsWriter(arguments.result_directory)
        self.job_name = Path(arguments.result_directory).resolve().parts[-2]  # The model specification name.

        if arguments.restart:
            self.keyspace = Keyspace.from_previous_run(self.results_writer.results_root)
            self.existing_outputs = pd.read_hdf(os.path.join(self.results_writer.results_root, 'output.hdf'))
        else:
            model_specification = build_model_specification(arguments.model_specification_file)

            self.keyspace = Keyspace.from_branch_configuration(arguments.num_input_draws, arguments.num_random_seeds,
                                                               arguments.branch_configuration_file)

            if "input_data.artifact_path" in self.keyspace.get_data():
                raise ValueError("An artifact path can only be supplied in the model specification file, "
                                 "not the branches configuration.")

            if "artifact_path" in model_specification.configuration.input_data:
                artifact_path = parse_artifact_path_config(model_specification.configuration)
                if arguments.copy_data:
                    self.copy_artifact(artifact_path, self.keyspace.get_data().get('input_data.location'))
                    artifact_path = os.path.join(self.results_writer.results_root, "data_artifact.hdf")
                model_specification.configuration.input_data.update(
                    {"artifact_path": artifact_path},
                    source=__file__)

            model_specification_path = os.path.join(self.results_writer.results_root, 'model_specification.yaml')
            shutil.copy(arguments.model_specification_file, model_specification_path)

            self.existing_outputs = None

            # Log some basic stuff about the simulation to be run.
            self.keyspace.persist(self.results_writer)
        self.model_specification = os.path.join(self.results_writer.results_root, 'model_specification.yaml')

        self.sge_log_directory = os.path.join(self.results_writer.results_root, "sge_logs")
        os.makedirs(self.sge_log_directory, exist_ok=True)
        self.worker_log_directory = os.path.join(self.results_writer.results_root, 'worker_logs')
        os.makedirs(self.worker_log_directory, exist_ok=True)

    def copy_artifact(self, artifact_path, locations):
        full_art = Artifact(artifact_path)

        artifact_locs = set(full_art.load('metadata.locations'))
        if not set(locations).issubset(artifact_locs):
            raise ValueError(f'You have specified locations {", ".join(set(locations) - artifact_locs)} in your '
                             f'branches/model specifications that are not present in the specified artifact.')

        # very slow to copy just relevant locs so copy the whole artifact
        self.results_writer.copy_file(artifact_path, "data_artifact.hdf")


def build_job_list(ctx):
    jobs = []
    number_already_completed = 0

    for (input_draw, random_seed, branch_config) in ctx.keyspace:
        parameters = {'model_specification_file': ctx.model_specification,
                      'branch_configuration': branch_config,
                      'input_draw': int(input_draw),
                      'random_seed': int(random_seed),
                      'results_path': ctx.results_writer.results_root,
                      }

        do_schedule = True
        if ctx.existing_outputs is not None:
            mask = ctx.existing_outputs.input_draw == int(input_draw)
            mask &= ctx.existing_outputs.random_seed == int(random_seed)
            for k, v in collapse_nested_dict(branch_config):
                if isinstance(v, float):
                    mask &= np.isclose(ctx.existing_outputs[k], v)
                else:
                    mask &= ctx.existing_outputs[k] == v
            do_schedule = not np.any(mask)

        if do_schedule:
            jobs.append(parameters)
        else:
            number_already_completed += 1

    if number_already_completed:
        logger.info(f"{number_already_completed} of {len(ctx.keyspace)} jobs completed in previous run.")
        if number_already_completed != len(ctx.existing_outputs):
            logger.warning("There are jobs from the previous run which would not have been created "
                           "with the configuration saved with the run. That either means that code "
                           "has changed between then and now or that the outputs or configuration data "
                           "have been modified. This may represent a serious error so give it some thought.")

    ctx.number_already_completed = number_already_completed
    np.random.shuffle(jobs)
    return jobs


def concat_results(old_results, new_results):
    # Skips all the pandas index checking because columns are in the same order.
    start = time()
    if not old_results.empty:
        old_results = old_results.reset_index(drop=True)
        results = pd.DataFrame(data=np.concatenate([d.values for d in new_results] + [old_results.values]),
                               columns=old_results.columns)
    else:
        columns = new_results[0].columns
        results = pd.DataFrame(data=np.concatenate([d.reset_index(drop=True).values for d in new_results]),
                               columns=columns)
    results = results.set_index(['input_draw', 'random_seed'], drop=False)
    results.index.names = ['input_draw_number', 'random_seed']
    end = time()
    logger.info(f"Concatenated {len(new_results)} results in {end - start:.2f}s.")
    return results


def write_results_batch(ctx, written_results, unwritten_results, batch_size=50):
    new_results_to_write, unwritten_results = (unwritten_results[:batch_size], unwritten_results[batch_size:])
    results_to_write = concat_results(written_results, new_results_to_write)
    start = time()
    retries = 3
    while retries:
        try:
            ctx.results_writer.write_output(results_to_write, 'output.hdf')
            break
        except Exception as e:
            logger.warning(f'Error trying to write results to hdf, retries remaining {retries}')
            sleep(30)
            retries -= 1
    end = time()
    logger.info(f"Updated output.hdf in {end - start:.4f}s.")
    return results_to_write, unwritten_results


def process_job_results(registry_manager, ctx):
    start_time = time()

    if ctx.existing_outputs is not None:
        written_results = ctx.existing_outputs
    else:
        written_results = pd.DataFrame()
    unwritten_results = []

    logger.info('Entering main processing loop.')
    batch_size = 200
    while registry_manager.jobs_to_finish:
        sleep(5)
        unwritten_results.extend(registry_manager.get_results())
        if len(unwritten_results) > batch_size:
            written_results, unwritten_results = write_results_batch(ctx, written_results,
                                                                     unwritten_results, batch_size)

        registry_manager.update_and_report()
        logger.info(f'Unwritten results: {len(unwritten_results)}')
        logger.info(f'Elapsed time: {(time() - start_time)/60:.1f} minutes.')

    batch_size = 500
    while unwritten_results:
        written_results, unwritten_results = write_results_batch(ctx, written_results, unwritten_results,
                                                                 batch_size=batch_size)
        logger.info(f'Unwritten results: {len(unwritten_results)}')
        logger.info(f'Elapsed time: {(time() - start_time) / 60:.1f} minutes.')


def check_user_sge_config():
    """Warn if a user has set their stdout and stderr output paths
    in a home directory config file. This overrides settings from py-drmaa."""

    sge_config = Path().home() / ".sge_request"

    if sge_config.exists():
        with sge_config.open('r') as f:
            for line in f:
                line = line.strip()
                if (('-o ' in line) or ('-e' in line)) and not line.startswith("#"):
                    logger.warning("You may have settings in your .sge_request file "
                                   "that could overwrite the log location set by this script. "
                                   f"Your .sge_request file is here: {sge_config}.  Look for "
                                   "-o and -e and comment those lines to recieve logs side-by-side"
                                   "with the worker logs.")


def main(model_specification_file, branch_configuration_file, result_directory, project, peak_memory, redis_processes,
         copy_data=False, num_input_draws=None, num_random_seeds=None, restart=False):

    output_directory = utilities.get_output_directory(model_specification_file, result_directory, restart)
    utilities.configure_master_process_logging_to_file(output_directory)

    arguments = SimpleNamespace(model_specification_file=model_specification_file,
                                branch_configuration_file=branch_configuration_file,
                                result_directory=output_directory,
                                project=project,
                                peak_memory=peak_memory,
                                copy_data=copy_data,
                                num_input_draws=num_input_draws,
                                num_random_seeds=num_random_seeds,
                                restart=restart)
    ctx = RunContext(arguments)
    check_user_sge_config()
    jobs = build_job_list(ctx)

    if len(jobs) == 0:
        logger.info("Nothing to do")
        return

    logger.info('Starting jobs. Results will be written to: {}'.format(ctx.results_writer.results_root))

    if redis_processes == -1:
        redis_processes = int(math.ceil(len(jobs) / vtc_globals.DEFAULT_JOBS_PER_REDIS_INSTANCE))

    worker_template, redis_ports = launch_redis_processes(redis_processes)
    worker_file = output_directory / 'settings.py'
    with worker_file.open('w') as f:
        f.write(worker_template)

    registry_manager = RegistryManager(redis_ports, ctx.number_already_completed)
    registry_manager.enqueue(jobs)

    drmaa_session = drmaa.Session()
    drmaa_session.initialize()

    start_cluster(drmaa_session, len(jobs), ctx.peak_memory, ctx.sge_log_directory,
                  ctx.worker_log_directory, project, worker_file, ctx.job_name)

    process_job_results(registry_manager, ctx)

    logger.info('Jobs completed. Results written to: {}'.format(ctx.results_writer.results_root))
