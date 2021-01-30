""" @author: Sam Parry """
import json
import os
import shutil


def modifyBendingBeam(tdata, filepath):
    """
    alters the original beam_bending.json file
    original beam_bending.json file is represented by a dict
    key values are changed via input params
    returns a json object with indent=4
    :param tdata: number of training points
    :param filepath: location to store new .json file
    """
    # copy of the original beam_bending.json expressed as a dictionary
    new_json_as_dict = {
        "problem": "beam_bending",
        "operators": ["+", "-", "*"],
        "problem_args": [5.0e-5, 0.0, 10.0, 2],
        "hyperparams": {
            "pop_size": 100,
            "stack_size": 40,
            "max_generations": 100000,
            "fitness_threshold": 1e-7,
            "stagnation_threshold": 10000,
            "differential_weight": 0.1,
            "check_frequency": 5,
            "min_generations": 1,
            "crossover_rate": 0.6,
            "mutation_rate": 1.0,
            "evolution_algorithm": "DeterministicCrowding"
        },
        "result_file": "beam_bending.res.json",
        "log_file": "log",
        "checkpoint_file": "chk"
    }
    # change number of training points
    new_json_as_dict["problem_args"][3] = tdata
    # Write new json file to given directory
    filename = filepath + "beam_bending.json"
    with open(filename, 'w') as outfile:
        json.dump(new_json_as_dict, outfile, indent=4)

def make_trials(tdata, t_path):
    """
    Create 30 trial folders within a tdata folder
    :param tdata: number of training points for the current set of trials
    :param t_path: path of the parent directory containing the trials
    """
    files = ['N:/tests/bnd_tdata/doit.slurm', 'N:/tests/bnd_tdata/soln_tests_cas_simpl.py']
    # create beam_bending.json
    modifyBendingBeam(tdata, t_path)

    for i in range(1, 31):
        trial = 'trial' + str(i)
        trial_path = t_path + trial + '/'
        os.mkdir(trial_path)

        # copy files into trial folder
        shutil.copy(files[0], trial_path)
        shutil.copy(files[1], trial_path)
        shutil.copy(t_path + 'beam_bending.json', trial_path)

def make_tdir(tdata_list, test_path):
    """
    Create the directories and subdirectories for tests involving a specified number of training points.
    :param tdata_list: list of training data points
    :param test_path: absolute path to the test directory
    """
    for tdata in tdata_list:
        t_path = '{0}t{1}/'.format(test_path, tdata)
        os.mkdir(t_path)
        make_trials(tdata, t_path)

def main():
    """ its a main """
    tdata_list = [2, 4, 8, 16, 32, 64]
    test_path = 'N:/tests/bnd_tdata/'
    make_tdir(tdata_list, test_path)

main()
