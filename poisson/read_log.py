# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557 """

import numpy as np
import h5py
import json
import os


def read_log(test_name):
    """
    Parses through the poisson log file and collect fitness and generational data as a numpy array, then
    extracts the test hyperparameters from poisson.json.
    All data are stored in a H5PY data format.
        N:/tests/poisson/results.h5
    :param test_name: test directory containing the log file
    """
    gen = np.array([]).astype(float)
    fit = np.array([]).astype(float)
    log_path = 'N:/tests/poisson/' + test_name + '/log_0.log'

    try:
        log = open(log_path, 'r')
        # read log file, line by line
        lines = log.readlines()
        for line in lines:
            if 'Generation: ' in line:
                split = line.split(' ')

                # results before gen = 4 have results printed for each of the 52 tasks
                # only values of gen >= 4 can be reliably parsed this way
                if int(split[2]) >= 4:
                    gen = np.append(gen, int(split[2]))  # convert to int
                    fit = np.append(fit, float(split[-3]))  # convert to float
        log.close()

        # Create results.h5
        h5 = h5py.File('N:/tests/poisson/results.h5', 'a')
        try:  # handles existing group name errors
            group = h5.create_group(test_name)
        except ValueError:
            del h5[test_name]
            group = h5.create_group(test_name)

        group.create_dataset('hyperparams', data=read_poisson_json(test_name))  # extract hyperparams from poisson.json
        group.create_dataset('fit', data=fit)
        group.create_dataset('gen', data=gen)

        # add best_fit and eq to results.h5
        best_fit, eq = read_results_json(test_name)
        group.create_dataset('best_fit', data=best_fit)
        group.create_dataset('equation', data=eq)
        h5.close()
    except FileNotFoundError:
        print('\nLog file not found\t' + log_path)


def save_all():
    """ Writes the results of all tests to results.h5 """
    os.chdir('N:/tests/poisson/')
    for folder in os.scandir():
        if folder.is_dir():
            read_log(folder.name)


def read_poisson_json(test_name):
    """
    Returns the hyperparameter values contained in the poisson.json file
    contained in each test directory.
    :param: test_name: name of poisson test directory.
    :return: values: Hyperparameter values stored in a numpy array
    """
    path = 'N:/tests/poisson/' + test_name + '/poisson.json'
    jason = json.load(open(path, 'r'))
    hyperparams = jason['hyperparams']  # dict object
    hyperparams.pop('evolution_algorithm')  # removes string parameter
    values = np.asarray(list(hyperparams.values()))  # convert dict to array
    return values


def read_results_json(test_name):
    """
    Reads the final best equation and fitness from the test results json
    :param test_name: Name of poisson test dir
    :return: best fitness and equation
    """
    path = 'N:/tests/poisson/' + test_name + '/results.json'
    jason = json.load(open(path, 'r'))
    eqs = jason[0]['pareto_front']
    best_fit = eqs[0]['fitness']
    best_eq = eqs[0]['equation']
    return best_fit, best_eq


def main():
    """ main """
    save_all()


if __name__ == '__main__':
    main()
