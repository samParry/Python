# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 22:57:33 2020

@author: Sam
"""

import json
import os
import shutil

#tdata
problem_args = [[5.0e-5, 0.0, 10.0, 2], [5.0e-5, 0.0, 10.0, 4], [5.0e-5, 0.0, 10.0, 6], [5.0e-5, 0.0, 10.0, 8], [5.0e-5, 0.0, 10.0, 10]]

# binaries to undergo training data variation testing
binaries = ["00000", "00001", "00010", "00011", "00111", "10110", "10111"]

# 5 variable hyperparams
pop_size = [100,300]
stack_size = [50,100]
differential_weight = [0.1,1]
crossover_rate = [0.4,0.8]
mutation_rate = [0.4,0.8]

# for reference
original_params = [500, 120, 0.1, 0.8, 0.2] 
number_of_trials = 5

# file paths
chpc_parent_dir = ["/uufs/chpc.utah.edu/common/home/u1008557/tdata_binaries/t2", "/uufs/chpc.utah.edu/common/home/u1008557/tdata_binaries/t4", 
                   "/uufs/chpc.utah.edu/common/home/u1008557/tdata_binaries/t6", "/uufs/chpc.utah.edu/common/home/u1008557/tdata_binaries/t8",
                   "/uufs/chpc.utah.edu/common/home/u1008557/tdata_binaries/t10"]

# alters the original beam_bending.json file
# original beam_bending.json file is represented by a dict
# key values are changed via input params
# returns a json object with indent=4
def modifyBendingBeam(params, problem_args, filepath):

    pop_size,stack_size,differential_weight, crossover_rate, mutation_rate, = params[:]
    dictKeys = ["pop_size", "stack_size", "differential_weight", "crossover_rate", "mutation_rate"]
    
    # copy of the original beam_bending.json expressed as a dictionary
    new_json_as_dict =  {
      "problem": "beam_bending",
      "operators": ["+", "-", "*", "/", "^"],
      "problem_args": [5.0e-5, 0.0, 10.0, 5],
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
      "log_file": "beam_bending",
      "checkpoint_file": "beam_bending"
    }
    
    # change values of specified hyperparameters
    for i in range(len(params)):
        new_json_as_dict["hyperparams"][dictKeys[i]] = params[i]
        new_json_as_dict["problem_args"] = problem_args
        
    # Write new json file to given directory
    filename = filepath + "/beam_bending.json"
    with open(filename, 'w') as outfile:
        json.dump(new_json_as_dict, outfile, indent=4)
    

# create a directory and sub directories in a given location
# calls modifyBeamBending and passes the subfolder file path so the json can we written
def createDirectories(params, problem_args, parent_dir, folder, number_of_trials):    
    # Path 
    path = os.path.join(parent_dir, folder) 
    
    # create the directory "bin" in "parent_dir"
    # if the directory already exists, deletes existing
    # directory and recreates a new one
    try:
        os.mkdir(path)
    except:
        shutil.rmtree(path)
        os.mkdir(path)
    
    # create subfolders for each trial run
    subfolder_parent_dir = parent_dir + "/" + folder
    
    # files to copy into new directories
    file1 = "/uufs/chpc.utah.edu/common/home/u1008557/models/fifth_deriv_penalty/doit.slurm"
    
    # subfolders names trial1, trial2 etc.
    for i in range(number_of_trials):
        subfolder = "trial" + str(i)
        filepath = os.path.join(subfolder_parent_dir, subfolder)
        
        os.mkdir(filepath)
        
        # write json to new trial bin
        modifyBendingBeam(params, problem_args, filepath)
    
        # copy over .py and .slurm files
        shutil.copy(file1, filepath)
        
# constuct the combination of hyperparameters dictated by the binary file. 
def getParams(binary_str):
    hyperparams = [[100,300], [50,100], [0.1,1], [0.4,0.8], [0.4,0.8]]
    params = list()
    i = 0
    for digit in map(int,binary_str):
        params.append(hyperparams[i][digit])
        i += 1
    return params
        
for folder in binaries:
    params = getParams(folder)
    for i in range(len(problem_args)):
        createDirectories(params, problem_args[i], chpc_parent_dir[i], folder, number_of_trials)
