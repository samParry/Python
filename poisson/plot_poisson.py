# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557 """

import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import os
import shutil
import sys


class Test:
    """ Creates an object with each results.h5 dataset stored as a class attribute """

    def __init__(self, test_name, group):
        self.name = test_name
        self.best_fit = group['best_fit'][()]
        self.equation = group['equation'][()]
        Test.simplify(self)
        self.fit = group['fit'][()]
        self.gen = np.array(group['gen'][()], dtype=int)  # convert to int
        self.hyperparams = group['hyperparams'][()]

    def simplify(self):
        """ Edits self.equation to have python syntax """
        xy = self.equation[1:-1].replace('X_0', 'x')
        xy = xy.replace('X_1', 'y')
        xy = xy.replace(')(', '*')
        self.equation = xy.replace('sin', 'np.sin')

    def plot_fitness(self, dest):
        """
        Plots the generations vs. fitness
        :param dest: where to save plot
        """
        plt.figure()
        plt.plot(self.gen, self.fit)
        plt.title('Poisson: Evolution of Solution Fitness')
        plt.xlabel('Generations')
        plt.ylabel('Solution Fitness')
        plt.savefig('{0}{1}.png'.format(dest, self.name))
        plt.close()

    def plot_solution(self, dest):
        """
        Surface plot of final solution.
        :param dest: where to save plot
        """
        x_1D = np.linspace(0, np.pi)
        y_1D = np.linspace(0, np.pi)
        x_sol_1D = np.linspace(0,1)
        y_sol_1D = np.linspace(0,1)
        x_sol, y_sol = np.meshgrid(x_sol_1D, y_sol_1D)
        x, y = np.meshgrid(x_1D,y_1D)
        z = eval(self.equation)
        z_sol = np.sin(np.pi*x_sol) * np.sin(np.pi*y_sol)
        """ works
        fig, ax = plt.subplots()
        plot = ax.contourf(x,y,z, 100, locator=ticker.LinearLocator())
        cbar = fig.colorbar(plot)"""
        fig = plt.figure(figsize=[7.5,6])
        plot = plt.contourf(x, y, z, 100, locator=ticker.LinearLocator())
        sol_plot = plt.contour(x_sol,y_sol, z_sol, linestyles='dotted', colors='k')
        cbar = fig.colorbar(plot)
        # labels = [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5]
        # plt.clabel(sol_plot, labels, inline=True, fmt='%.0d', fontsize=10, colors='k')

        # plt.show()
        # sys.exit()  # TODO delete me
        plt.title('Poisson: Final Solution Surface')
        plt.savefig('{0}{1}.png'.format(dest, self.name))
        plt.close()


def read_results():
    """ Gets fitness data needed to plot test results. """
    path = 'N:/ptests/results.h5'
    h5 = h5py.File(path, 'r')

    test_list = []
    for test_name in h5.keys():
        group = h5[test_name]
        test = Test(test_name, group)
        test_list.append(test)

    return test_list


def main():
    """ Create plots of the fitness evolution and final solution surface """
    test_list = read_results()
    dest1 = 'C:/Users/User/Desktop/OneDrive - University of Utah/Research/Poisson Plots/fitness_evolution/'
    dest2 = 'C:/Users/User/Desktop/OneDrive - University of Utah/Research/Poisson Plots/solution/'

    if os.path.isdir(dest1):  # store plots in my OneDrive
        shutil.rmtree(dest1)
    os.mkdir(dest1)
    if os.path.isdir(dest2):
        shutil.rmtree(dest2)
    os.mkdir(dest2)
    
    for test in test_list:
        test.plot_fitness(dest1)
        test.plot_solution(dest2)


main()
