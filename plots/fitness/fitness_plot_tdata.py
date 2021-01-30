# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import shutil
import h5py


def analyze_tdata():
    """
    Parse through the fitness data of the training point data sets (tdata_gen1 & tdata_gen2)
    Plot the evolution of the fitness functions with respect to generations for each training point value.
    Save data in a h5 file on the U of U OneDrive
    """
    test_list = ['tdata_gen1', 'tdata_gen2']
    t_list = ['t2', 't4', 't6', 't8', 't10']
    binary_list = ['00000', '00001', '00010', '00011', '00111']
    trial_list = ['trial0', 'trial1', 'trial2', 'trial3', 'trial4']

    plotdir = 'C:/Users/User/Desktop/OneDrive - University of Utah/Research/Plots/tdata_fitness/'
    create_plot_dir(plotdir)

    tic = time.time()
    print('tick...')
    for t in t_list:
        t_fitness = []
        best_fit = [100]  # store the best fitness and its binary
        best_binary = 00000

        for test in test_list:
            tpath = 'N:/tests/{0}/{1}/'.format(test, t)

            for binary in binary_list:
                binarypath = tpath + binary + '/'

                for trial in trial_list:
                    trialpath = binarypath + trial + '/'
                    os.chdir(trialpath)
                    fitness = read_log()  # extract fitness values
                    t_fitness.append(fitness)

                    if fitness[-1] < best_fit[-1]:
                        best_fit = fitness
                        best_binary = binary

        # Save plots on OneDrive
        print('tock:\t' + t + '\tt-minus: ' + str(round(time.time()-tic)))
        plot(t_fitness, best_fit, best_binary, t, plotdir)


def plot(t_fitness, best_fit, best_binary, t, plotdir):
    """
    Creates a figure that shows the evolution of the best and avg fitness values
    :param t_fitness: Array containing fitness data
    :param best_fit: Array of best fitness values
    :param best_binary: Binary of the best fitness value
    :param t: Number of training points
    :param plotdir: Directory to store saved plots
    """

    # prep arrays to be plotted
    best = best_fit
    length = len(best)
    avg = average_fitness(t_fitness, length)
    gen = np.arange(length) * 5
    solution = np.ones(length) * 1E-7  # correct solution threshold

    # gets the number of training points from the name of the test bin (t2, t4, .. t10)
    if t[-1] is '0':
        plt.title('Evolution of Solution Fitness\nTraining Points: ' + t[-2:])
    else:
        plt.title('Evolution of Solution Fitness\nTraining Points: ' + t[-1])

    # configure plot
    plt.plot(gen, avg[:length], label='Avg. Solution')
    plt.plot(gen, best[:length], label='Best Solution')
    plt.plot(gen, solution, 'b--', label='Correct Solution\nThreshold: 10e-7')

    plt.xlabel('Generation')
    plt.ylabel('Solution Fitness', )
    plt.yscale('log')
    # plt.annotate('10e-7', xy=((length*5)*0.8, 2E-7))  # gives a numerical value to correct solution line
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=10)

    if best_fit[-1] > 1E-7:
        plt.ylim(bottom=1E-8)

    # add hyperparameter values to plot
    params = get_params(best_binary)
    plt.figtext(0.7, 0.6, 'Best Solution Parameters')
    plt.figtext(0.7, 0.55, 'Population: ' + str(params[0]))
    plt.figtext(0.7, 0.5, 'Stack Size: ' + str(params[1]))
    plt.figtext(0.7, 0.45, 'Differential Weight: ' + str(params[2]))
    plt.figtext(0.7, 0.4, 'Crossover Rate: ' + str(params[3]))
    plt.figtext(0.7, 0.35, 'Mutation Rate: ' + str(params[4]))
    plt.tight_layout()
    # plt.show()

    # save figure on my U of U OneDrive
    plt.savefig(plotdir + t + '.png')
    plt.close()


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


def new_h5():
    """
    Create an h5 file on my U of U OneDrive
    :return h5: h5py file object
    """
    h5path = 'C:/Users/User/Desktop/OneDrive - University of Utah/Research/results/fitness_vs_gen_tdata.h5'
    if os.path.isfile(h5path):
        os.remove(h5path)
    h5 = h5py.File(h5path, 'a')
    return h5


def create_plot_dir(plotdir):
    """
    Creates a plot bin to store figures on my OneDrive
    :param plotdir: path of new directory
    """
    if os.path.isdir(plotdir):
        shutil.rmtree(plotdir)
    os.mkdir(plotdir)


def get_params(binary):
    """
    Gets the values of the hyperparameters associated with a binary tag
    :param binary: Tag representing hyperparameter values
    :return: param: list of hyperparameter values
    """
    pop = [100, 300]
    stack = [50, 100]
    diff = [0.1, 1.0]
    cross = [0.4, 0.8]
    mut = [0.4, 0.8]

    param = [
        pop[int(binary[0])],
        stack[int(binary[1])],
        diff[int(binary[2])],
        cross[int(binary[3])],
        mut[int(binary[4])]
        ]

    return param


def main():
    """ Its a main method"""
    analyze_tdata()


if __name__ == '__main__':
    tic = time.time()
    main()
    toc = time.time()
    print('Execution Time: ' + str(round((toc - tic) / 60., 1)) + ' min')
