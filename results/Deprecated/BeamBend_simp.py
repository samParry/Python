# -*- coding: utf-8 -*-
""" @author: Sam Parry, Erick Solum """

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from problems.beam_bending import analytic_solution
from bingo.evolutionary_optimizers.parallel_archipelago import load_parallel_archipelago_from_file
import sys
import os
import shutil
import csv

matplotlib.use('Agg')


# This BendBeamReader file contains plot from pickle and reads a the beam_bending pickle files
# then run plot from pickel using the most recent beam_bending pickle file.

# This function contains the previous plot from pickle file. Because while it is being run,
# the working directory is each trial, there shouldn't be a need for changes.
def plot_from_pickle(fname):
    # read bingo pickle file and retrieve best model
    archipelago = load_parallel_archipelago_from_file(fname)
    best_ind = archipelago.get_best_individual()
    # print('%.3e    ' % best_ind.fitness, best_ind.get_complexity(),
    #             '   f(X_0) =', best_ind)

    L = 10.
    k = 5.e-5
    x = np.linspace(0., L, 64).reshape([64, 1])
    yan = analytic_solution(x, k, L)
    y = best_ind.evaluate_equation_at(x)

    # plot the training data too
    X_a = np.linspace(0, 10, 5)
    Y_a = analytic_solution(X_a, 5e-5, 10)

    plt.figure()
    plt.plot(x, yan, 'r-', label='Analytical Solution')
    plt.plot(X_a, Y_a, 'gx', label='Training Data Points')
    plt.plot(x, y, 'b-', label='Best GPSR Model')
    plt.xlabel('x')
    plt.ylabel('displacement')
    plt.legend()
    plt.savefig('best_individual')
    plt.close()

    # This Recent_Beam function is what traverses each trial and runs plot from pickle.
    # It is meant to be run in each binary trial bin


def bingosimplify(expr, x_type='X_0', round_num=1):
    if isinstance(expr, str):
        # finds all the floats inside of the string output. It will prioritize the earlier or's. (Seperated by | )
        v = re.findall('[0-9]+\.[0-9]+[e]...|'
                       '\-[0-9]+\.[0-9]+[e]...|'
                       '[0-9]+\.[0-9]+|'
                       '\-[0-9]+\.[0-9]+'
                       , expr)
        # Find all gives us all of the numbers, including repeats. VFilters out all the repeat values.
        v_filtered = list(set(v))
        # TODO: Replace variables hard coding with better solution
        variables = ['A', 'B', 'C', 'D',
                     'F', 'G', 'H', 'J']
        expr_v1 = str_processing(x_type, expr)

        expr_v2, replacements = str_parse_initial(v_filtered, variables, expr_v1)
        standard_trans = (lambda_notation, auto_symbol, repeated_decimals,
                          auto_number, factorial_notation, convert_xor)
        try:
            expr_v3 = parse_expr(expr_v2, transformations=standard_trans, evaluate=False)
        except:
            #raise ValueError('expr has notation not accounted for in bingosimplify')
            return " "
        # TODO: Check for negative inside sqrts
        # Reinserting the numbers back into the equation.
        # Giving sympy simplify another go at it, this time with numbers. Hopefully with a lot less truncation.
        # VFiltered is filtering out all the repeat values.
        expr_v4 = expr_v3.subs(replacements, evaluate=False)

        expr_v4 = simplify(expr_v4, evaluate=False)

        expr_v4 = str(radsimp(expr_v4, symbolic=False))

        V2 = re.findall('[0-9]+\.[0-9]+[e].[0-9]+|'
                        '\-[0-9]+\.[0-9]+[e].[0-9]+|'
                        '[0-9]+\.[0-9]+|'
                        '\-[0-9]+\.[0-9]+',
                        expr_v4)
        v_filtered = list(set(V2))
        variables = ['A', 'B', 'C', 'D',
                     'F', 'G', 'H', 'J']

        expr_v4, replacements2 = expr_parse_expand(round_num, v_filtered,
                                                   variables, expr_v4)
        try:
            # Parse expression simplifies all of the common letter
            # variables out by giving it the input standard_transformation.
            expr_v5 = parse_expr(expr_v4)

        except:
            raise ValueError('expr has notation not accounted for in bingosimplify')
        expr_v5 = expand(expr_v5.subs(replacements2), complex=False)  # Reinserting the numbers back into the equation.
        return expr_v5
    else:
        return ValueError('')


def expr_parse_expand(round_num, v_filtered,
                      variables, expr_v4):
    for i in range(0, len(v_filtered)):
        expr_v4 = re.sub(v_filtered[i], variables[i], expr_v4)
        if (re.match("\-[0-9]+\.[0]{3,}|[0-9]+\.[0]{2,}", v_filtered[i]) or
            re.match('[9]+\.[9]{4,}|\-[9]+\.[9]{4,}', v_filtered[i])) and not \
                re.match('[0]\.[0]+|-[0]\.[0]+', v_filtered[i]) and not \
                re.search('[e]', v_filtered[i]):
            v_filtered[i] = str(round(float(v_filtered[i]), round_num))

        replacements2 = [(variables[j], v_filtered[j])
                         for j in
                         range(len(v_filtered))]  # Logs what replacements were made, so they can be reinserted later.
    return expr_v4, replacements2


def str_parse_initial(v_filtered, variables, expr_v2):
    # The loop bellow cycles through the equation replacing every number with its corresponding variable.
    # The replacements variable logs what replacements were made, so they can be reinserted later.
    for i in range(0, len(v_filtered)):
        expr_v2 = re.sub(v_filtered[i], variables[i], expr_v2)
        replacements = [(variables[j], v_filtered[j]) for j in
                        range(len(v_filtered))]

    return expr_v2, replacements


def str_processing(x_type, expr):
    # All of the below are clean up methods to make sure that sympy can understand the string.
    # Replaces input x_tryp with x
    # Replaces all ^ with the more standard ** notation
    # Adds asterisks where ever parentheses face eachother.
    expr_sp = re.sub(x_type, 'x', expr)
    expr_v1 = re.sub('[)][(]', ')*(', expr_sp)
    return expr_v1


def Recent_beam(parent_dir):
    Trial_Vec = ["trial0", "trial1", "trial2", "trial3", "trial4"]
    suffix = ["_0", "_1", "_2", "_3", "_4"]
    j = 0  # increments over suffix values
    # This loop cycles through each of the trials (trial0 - trial4)
    for i in Trial_Vec:
        plotstr = "/uufs/chpc.utah.edu/common/home/u1008557/trials_gen2/plots/" + parent_dir
        os.chdir(i)
        Bending_Names = []

        # os.scandir is a alternative to listdir, and is supposedly faster.
        # it also gives the advantage of presenting all the files in alphabetical order.
        # This is a convienient alternative to splitting strings and compairing numbers.

        with os.scandir() as it:
            for entry in it:
                # Filters the files that we don't need, and gives us the 2 .pkl files in order.
                if entry.name.startswith("beam_bending") and entry.is_file() and entry.name.endswith('.pkl'):
                    Bending_Names.append(entry.name)

                    ### Copying the best_individual plot to our plots bin ###
            print(parent_dir + "    " + suffix[j] + "    " + str(Bending_Names))
            plot_from_pickle(Bending_Names[-1])
            srcstr = os.getcwd() + "/best_individual.png"
            dststr = plotstr + suffix[j] + ".png"
            shutil.copyfile(srcstr, dststr)

            ### Dict data storage ###
            archipelago = load_parallel_archipelago_from_file(Bending_Names[-1])
            best_ind = archipelago.get_best_individual()
            best_ind = bingosimplify(best_ind)
            # write the fitness data to a new row
            with open('/uufs/chpc.utah.edu/common/home/u1008557/trial_test/Fitness_data.csv', 'a') as csvfile:
                fieldsnames = ['binary', 'fitness', 'complexity', 'f(X_0)']
                w = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldsnames)
                w.writerow({'binary': parent_dir, 'fitness': best_ind.fitness, 'complexity': best_ind.get_complexity(),
                            'f(X_0)': best_ind})

        j += 1  # increment suffix index
        os.chdir("..")


# Call methods
binaries = []
for a in (0, 1):  # create array of binary files
    for b in (0, 1):
        for c in (0, 1):
            for d in (0, 1):
                for e in (0, 1):
                    binaries.append(str(a) + str(b) + str(c) + str(d) + str(e))

# delete the Fitness_data.csv if it already exists
if os.path.exists('Fitness_data.csv'):
    os.remove('Fitness_data.csv')

# write fitness data headers to a .csv file
with open('Fitness_data.csv', 'a') as csvfile:
    fieldsnames = ['binary', 'fitness', 'complexity', 'f(X_0)']
    w = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldsnames)
    w.writeheader()

for k in binaries:
    os.chdir(k)
    Recent_beam(k)
    os.chdir("..")
