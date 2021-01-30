""" @author: Sam Parry """
import json
import os
import shutil

# 5 variable hyperparams
pop_size = [64, 128]
stack_size = [40, 50]
differential_weight = [0.1, 0.4]
crossover_rate = [0.4, 0.6]
mutation_rate = [0.8, 1.0]

# file paths
chpc_parent_dir = 'N:/tests/bnd_study/'
files = ['doit.slurm', 'soln_tests_cas_simpl.py']

def modifyBendingBeam(params, filepath):
    """
    alters the original beam_bending.json file
    original beam_bending.json file is represented by a dict
    key values are changed via input params
    returns a json object with indent=4
    :param params:
    :param filepath:
    """
    dictKeys = ["pop_size", "stack_size", "differential_weight", "crossover_rate", "mutation_rate"]

    # copy of the original beam_bending.json expressed as a dictionary
    new_json_as_dict = {
        "problem": "beam_bending",
        "operators": ["+", "-", "*"],
        "problem_args": [5.0e-5, 0.0, 10.0, 2],
        "hyperparams": {
            "pop_size": 500,
            "stack_size": 120,
            "max_generations": 100000,
            "fitness_threshold": 1e-12,
            "stagnation_threshold": 100000,
            "differential_weight": 0.1,
            "check_frequency": 5,
            "min_generations": 1,
            "crossover_rate": 0.8,
            "mutation_rate": 0.2,
            "evolution_algorithm": "DeterministicCrowding"
        },
        "result_file": "beam_bending.res.json",
        "log_file": "log",
        "checkpoint_file": "chk"
    }

    # change values of specified hyperparameters
    for i in range(len(params)):
        new_json_as_dict["hyperparams"][dictKeys[i]] = params[i]

    # Write new json file to given directory
    filename = filepath + "/beam_bending.json"
    with open(filename, 'w') as outfile:
        json.dump(new_json_as_dict, outfile, indent=4)



def createDirectories(params, parent_dir, binary, number_of_trials):
    """
    create a directory and sub directories in a given location
    calls modifyBeamBending and passes the subfolder file path so the json can we written
    :param params: parameter values of the specific binary
    :param parent_dir: absolute file path of test directory
    :param binary: binaryary directory string
    :param number_of_trials: number of trial runs to create
    """
    path = os.path.join(parent_dir, binary)  # i.e. /uufs/chpc.utah.edu/common/home/u1008557/tuning_params/00000

    # create the directory "binary" in "parent_dir"
    # if the directory already exists, deletes existing
    # directory and recreates a new one
    try:
        os.mkdir(path)
    except:
        shutil.rmtree(path)
        os.mkdir(path)

    # files to copy into new directories
    file1 = 'N:/tests/bnd_study/doit.slurm'
    file2 = 'N:/tests/bnd_study/soln_tests_cas_simpl.py'

    if number_of_trials == 0:
        # write json to new trial binary
        modifyBendingBeam(params, path)
        # copy over .slurm file
        shutil.copy(file1, path)
        shutil.copy(file2, path)
    else:
        # subfolders names trial1, trial2 etc.
        for i in range(number_of_trials):
            trial = "trial" + str(i)
            filepath = os.path.join(path, trial)
            os.mkdir(filepath)

            # write json to new trial binary
            modifyBendingBeam(params, filepath)
            # copy over .slurm file
            shutil.copy(file1, filepath)
            shutil.copy(file2, filepath)


# creates a new set of parameters for each possible combinaryation
# encapsulate this into a function later
for a in range(len(pop_size)):
    for b in range(len(stack_size)):
        for c in range(len(differential_weight)):
            for d in range(len(crossover_rate)):
                for e in range(len(mutation_rate)):
                    params = [pop_size[a], stack_size[b], differential_weight[c], crossover_rate[d], mutation_rate[e]]
                    binary = str(a) + str(b) + str(c) + str(d) + str(e)

                    # function call
                    print(binary)
                    createDirectories(params, chpc_parent_dir, binary, 0)
