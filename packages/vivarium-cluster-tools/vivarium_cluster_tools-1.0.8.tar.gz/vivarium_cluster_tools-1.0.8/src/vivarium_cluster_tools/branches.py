import os
from itertools import product

import yaml
import numpy as np

from vivarium.framework.utilities import collapse_nested_dict


class Keyspace:
    """A representation of a collection of simulation configurations."""

    def __init__(self, branches, keyspace):
        self.branches = branches
        self._keyspace = keyspace

    @classmethod
    def from_branch_configuration(cls, num_input_draws, num_random_seeds, branch_configuration_file):
        """
        Parameters
        ----------
        num_input_draws: int
            The number of GBD input draws to run.
        num_random_seeds: int
            The number of different random seeds to use for each GBD input draw.  Each model
            draw creates a simulation with fixed GBD data, but a different sample of the
            exogenous randomness used in the simulation.
        branch_configuration_file: str
            Absolute path to the branch configuration file.
        """
        branches, input_draw_count, random_seed_count = load_branches(num_input_draws,
                                                                      num_random_seeds,
                                                                      branch_configuration_file)
        keyspace = calculate_keyspace(branches)
        keyspace['input_draw'] = calculate_input_draws(input_draw_count)
        keyspace['random_seed'] = calculate_random_seeds(random_seed_count)

        return Keyspace(branches, keyspace)

    @classmethod
    def from_previous_run(cls, path):
        with open(os.path.join(path, "keyspace.yaml")) as f:
                keyspace = yaml.load(f)
        with open(os.path.join(path, "branches.yaml")) as f:
                branches = yaml.load(f)
        return Keyspace(branches, keyspace)

    def get_data(self):
        """Returns a copy of the underlying keyspace data."""
        return self._keyspace.copy()

    def get_branch_number(self, branch):
        for (i, b) in enumerate(self.branches):
            if b == branch:
                return i
        raise KeyError(f"No matching branch {branch}")

    def persist(self, results_writer):
        results_writer.write_output(self.get_data(), 'keyspace.yaml')
        results_writer.write_output(self.branches, 'branches.yaml')

    def __iter__(self):
        """Yields and individual simulation configuration from the keyspace."""
        for job_config in product(self._keyspace['input_draw'], self._keyspace['random_seed'], self.branches):
            yield job_config

    def __len__(self):
        """Returns the number of individual simulation runs this keyspace represents."""
        return len(list(product(self._keyspace['input_draw'], self._keyspace['random_seed'], self.branches)))


def calculate_input_draws(input_draw_count):
    """Determines a random sample of the GBD input draws to use given a draw count.

    Parameters
    ----------
    input_draw_count: int
        The number of draws to pull.

    Returns
    -------
    Iterable:
        A set of unique input draw numbers.
    """
    np.random.seed(123456)
    if 0 < input_draw_count <= 1000:
        return np.random.choice(range(1000), input_draw_count, replace=False).tolist()
    else:
        raise ValueError(f"Input draw count must be between 1 and 1000 (inclusive). "
                         f"You specified {input_draw_count}")


def calculate_random_seeds(random_seed_count):
    np.random.seed(654321)
    return np.random.randint(10*random_seed_count, size=random_seed_count).tolist()


def calculate_keyspace(branches):
    if branches[0] is None:
        return {}

    keyspace = {k: {v} for k, v in collapse_nested_dict(branches[0])}

    for branch in branches[1:]:
        branch = dict(collapse_nested_dict(branch))
        if set(branch.keys()) != set(keyspace.keys()):
            raise ValueError("All branches must have the same keys")
        for k, v in branch.items():
            keyspace[k].add(v)
    keyspace = {k: list(v) for k, v in keyspace.items()}
    return keyspace


def load_branches(num_input_draws, num_random_seeds, branch_configuration_file):
    if num_input_draws is None and num_random_seeds is None and branch_configuration_file is not None:
        input_draw_count, random_seed_count, branches = load_branch_configurations(branch_configuration_file)
    elif num_input_draws is not None and branch_configuration_file is None:
        input_draw_count = num_input_draws
        random_seed_count = num_random_seeds if num_random_seeds is not None else 1
        branches = [None]
    else:
        raise ValueError('Must supply one of branch_configuration_file or --num_input_draws but not both')

    return branches, input_draw_count, random_seed_count


def load_branch_configurations(path):
    with open(path) as f:
        data = yaml.load(f)

    input_draw_count = data.get('input_draw_count', 1)
    random_seed_count = data.get('random_seed_count', 1)

    assert input_draw_count <= 1000, "Cannot use more that 1000 draws from GBD"

    branches = expand_branch_templates(data['branches'])

    return input_draw_count, random_seed_count, branches


def expand_branch_templates(templates):
    """
    Take a list of dictionaries of configuration values (like the ones used in
    experiment branch configurations) and expand it by taking any values which
    are lists and creating a new set of branches which is made up of the
    product of all those lists plus all non-list values.

    For example this:

    {'a': {'b': [1,2], 'c': 3, 'd': [4,5,6]}}

    becomes this:

    [
        {'a': {'b': 1, 'c': 3, 'd': 4}},
        {'a': {'b': 2, 'c': 3, 'd': 5}},
        {'a': {'b': 1, 'c': 3, 'd': 6}},
        {'a': {'b': 2, 'c': 3, 'd': 4}},
        {'a': {'b': 1, 'c': 3, 'd': 5}},
        {'a': {'b': 2, 'c': 3, 'd': 6}}
    ]

    """
    expanded_branches = []

    for branch in templates:
        branch = sorted(collapse_nested_dict(branch))
        branch = [(k, v if isinstance(v, list) else [v]) for k, v in branch]
        expanded_size = np.product([len(v) for k, v in branch])
        new_branches = []
        pointers = {k: 0 for k, _ in branch}
        for _ in range(expanded_size):
            new_branch = []
            tick = True
            for k, v in branch:
                new_branch.append((k, v[pointers[k]]))
                if tick:
                    i = pointers[k]+1
                    if i < len(v):
                        tick = False
                        pointers[k] = i
                    else:
                        pointers[k] = 0
            new_branches.append(new_branch)
        expanded_branches.extend(new_branches)

    final_branches = []
    for branch in expanded_branches:
        root = {}
        final_branches.append(root)
        for k, v in branch:
            current = root
            *ks, k = k.split('.')
            for sub_k in ks:
                if sub_k in current:
                    current = current[sub_k]
                else:
                    current[sub_k] = {}
                    current = current[sub_k]
            current[k] = v

    return final_branches
