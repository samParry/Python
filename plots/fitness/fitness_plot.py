# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import shutil
import h5py

"""
    REQUIRMENTS
        Test dir's are assumed to be in /uufs/chpc.utah.edu/common/home/u1008557/tests/
        Must be run while connected to the CHPC via VPN.
        Must be connected to U of U OneDrive via the desktop
    
    .h5 structure
        name: fitness.h5
        groups: test names [gen1, gen2, gen3]
            32 data sets (names of binary)
                5 values (list of fitness data from each trial)
"""


def main():
    """
    Navigates through each test bin.
    Extracts the fitness data of each test run as it evolved every 5 generations.
    Plots fitness against generations and saves the plot in the trial directory.
    """
    print('\nPlots are being generated')
    tic = time.time()

    # make lists and needed to navigate the test directories
    # test > binaries > trials > .log
    tests = ['gen1', 'gen2', 'gen3']
    binaries = create_binaries()
    trials = ['trial0', 'trial1', 'trial2', 'trial3', 'trial4']

    # .h5 file to store each tests fitness data
    h5path = 'C:/Users/User/Desktop/OneDrive - University of Utah/Research/Results/fitness_vs_gen_param.h5'
    if os.path.isfile(h5path):
        os.remove(h5path)
    h5 = h5py.File(h5path, 'w')

    think_count = 0
    # iterate through each test bin
    for test in tests:
        think_count = thinking(think_count)
        group = h5.create_group(test)  # create group in .h5
        testpath = 'N:/tests/' + test + '/'
        plotdir = testpath + 'fitness_plots/'
        if os.path.isdir(plotdir):  # create directory to store binary figures
            shutil.rmtree(plotdir)
        os.mkdir(plotdir)

        for binary in binaries:
            binarypath = testpath + binary + '/'
            trial_fitness = []  # fitness arrays of all 5 trials

            for trial in trials:
                trialpath = binarypath + trial + '/'
                os.chdir(trialpath)
                fitness = read_log()  # extract fitness values
                plot_trial_fitness(fitness, trialpath)  # plot fitness values and store them in the trial bin
                trial_fitness.append(fitness)

            # plot each trials fitness
            plot_binary_fitness(trial_fitness, binarypath, plotdir, binary)

            # add data set to the .h5
            group.create_dataset(binary, data='data')
    h5.close()
    toc = time.time()
    print('Execution Time: ' + str(round((toc - tic) / 60., 1)) + ' min')


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


def plot_binary_fitness(trial_fitness, binarypath, plotdir, binary):
    """
    Plot the fitness values for each of the 5 trial folders
    contained within a single binary test bin

    :param trial_fitness: Numpy array containing fitness data for each trial
    :param binarypath: Location of new plot within the binary directory
    :param plotdir: Location of plot directory with each binary plot
    :param binary: Name of current binary bin. Used in figure title.
    """

    # plot each of the 5 data sets
    for i in range(len(trial_fitness)):
        fitness = trial_fitness[i]
        gen = np.arange(len(fitness)) * 5
        label = 'trial ' + str(i)
        plt.plot(gen, fitness, label=label)

    plt.title('Evolution of Best Fitness: ' + binary)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.yscale('log')
    plt.legend()
    plt.savefig(binarypath + 'fitness_plot.png')
    plt.savefig(plotdir + binary + '.png')
    plt.close()


def plot_trial_fitness(fitness, dest):
    """
    Plots the fitness values as a function of generations
    Stores plot in the trial bin

    :param fitness: 1D numpy array of fitness values
    :param dest: location of new plot
    """
    fit = fitness
    gen = np.arange(len(fit)) * 5
    plt.plot(gen, fit)
    plt.title('Evolution of Best Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.yscale('log')
    plt.savefig(dest + 'fitness_plot.png')
    plt.close()


def thinking(think_count):
    """
    I'm Thinking
    """
    if think_count is 0:
        print('\n\tHaving a good think...')
        think_count += 1
    elif think_count is 1:
        print('\tA real good think')
        think_count += 1
    elif think_count is 2:
        print('\tNumber rock go Brrrrrr\n')
    return think_count


if __name__ == "__main__":
    main()
