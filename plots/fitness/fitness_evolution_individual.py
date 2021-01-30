# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557 """

import os
import numpy as np
import matplotlib.pyplot as plt

def create_binaries():
    """
    Create the 32 binaries from 00000 - 11111
    :return: list of binaries
    """
    binaries = []
    for a in (0, 1):  # create array of binary files
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    for e in (0, 1):
                        binaries.append(str(a) + str(b) + str(c) + str(d) + str(e))
    return binaries

def read_log():
    """
    Parse through the log file and extract the the fitness value of each generation
    Data is printed to the log file every 5 generations beginning with gen 0
        Gen = fitness index * 5

    :return numpy array of fitness data
    """
    try:
        log = open('beam_bending_0.log', 'r')
        fitness = np.zeros([0])  # holds fitness data

        # read log file
        lines = log.readlines()
        for line in lines:
            if 'fitness: ' in line:  # checks if fitness is present in current line
                fitness_value = line.split('fitness: ')[-1].strip()
                fitness = np.append(fitness, float(fitness_value))

        log.close()  # close file
        return fitness

    except FileNotFoundError:
        print('log file absent: ' + os.getcwd())

def extend_fitness_array(t_fitness, length):
    """
    Extend all the arrays inside t_fitness to have the same lengths.
    The last value in the array is repeated to increase its size
    :param length: length of data arrays
    :param t_fitness: nested list of fitness arrays
    """
    # find the length of the largest fitness array in the training point data
    for fit in t_fitness:
        if len(fit) > length:
            length = len(fit)

    # extend the length of the other fitness arrays.
    # this allows a mean to be taken
    for i in range(len(t_fitness)):
        fit = t_fitness[i]

        if len(fit) < length:
            length_diff = length - len(fit)
            last_value = fit[-1]
            extension = [last_value]*length_diff
            fit = np.append(fit, extension)  # add the extension
            t_fitness[i] = fit

    return t_fitness


def average_fitness(t_fitness, length):
    """
    Returns the average fitness values for a given array of lists
    :param length:
    :param t_fitness: A list of fitness value arrays
    :return: An average of all the fitness values in t_fitness
    """
    # get all the fitness arrays to match lengths
    t_fitness = extend_fitness_array(t_fitness, length)
    t = np.array(t_fitness)
    return np.average(t, axis=0)

def main():
    """ main """
    binaries_all = create_binaries()
    testPath = 'N:/tests/boundary/'
    binaries = ['00100', '01111', '10011']
    fitness_list = []
    fitness_list_all = []

    # get fitness values from each successful test
    for binary in binaries:
        os.chdir(testPath + binary + '/')
        fitness = read_log()
        fitness_list.append(fitness)

    # plot successful tests
    for i in range(len(fitness_list)):
        fitness = fitness_list[i]
        gen = np.arange(len(fitness)) * 5
        label = 'Success ' + str(i+1)
        plt.plot(gen, fitness, label=label)

    # plot average fitness and correct solution threshold
    for binary in binaries_all:
        os.chdir(testPath + binary + '/')
        fitness = read_log()
        fitness_list_all.append(fitness)
    length = len(gen)
    avg_fit = average_fitness(fitness_list_all, length)
    plt.plot(gen, avg_fit[:length], 'k-.', label='Avg. Solution')
    plt.plot(gen, np.ones(len(gen)) * 1e-7, 'b--', label='Correct Solution Threshold')

    # configure plot
    plt.title('Evolution of Successful Boundary Problems')
    plt.xlabel('Generation')
    plt.ylabel('Solution Fitness')
    plt.yscale('log')
    plt.ylim(bottom=1e-8, top=1e-2)
    plt.legend(fontsize='small')
    plt.savefig(testPath + 'fitness_plot.png')
    plt.show()
    plt.close()

main()
