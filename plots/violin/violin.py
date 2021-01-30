# -*- coding: utf-8 -*-
""" @author: Sam Parry u1008557 """

import pandas as pd
import plotly.graph_objects as go

"""
This script was designed to read fitness data from a .csv and into a DataFrame object.
This csv had 20 adjacent columns. 5 hyperparameters with 4 data values for each hyperparameter.
Violin plots are created using the plotly library
"""

# name of column headers.
popList = ['pop 75', 'pop 100', 'pop 125', 'pop 300']
stackList = ['stack 40', 'stack 50', 'stack 60', 'stack 100']
difList = ['dif 0.1', 'dif 0.4', 'dif 0.7', 'dif 1.0']
crossList = ['cross 0.4', 'cross 0.6', 'cross 0.8', 'cross 1.0']
mutList = ['mut 0.4', 'mut 0.6', 'mut 0.8', 'mut 1.0']

# 2D list of column headers.
lists = [popList, stackList, difList, crossList, mutList]

# hyperparameter name used for figure titles.
listNames = ['Population', 'Stack Size', "Differential Weight", 'Crossover Rate', 'Mutation Rate']

# A Panda DataFrame object holds the 4 columns of data for each of the 5 hyperparameters.
pop = pd.read_csv('violin.csv', usecols=popList)
stack = pd.read_csv('violin.csv', usecols=stackList)
dif = pd.read_csv('violin.csv', usecols=difList)
cross = pd.read_csv('violin.csv', usecols=crossList)
mut = pd.read_csv('violin.csv', usecols=mutList)

# List of DataFrame Objects (df -> DataFrame)
dfList = [pop, stack, dif, cross, mut]

# Iterate through each of the DataFrame's and create a plot for each of them.
for i in range(len(lists)):
    fig = go.Figure()   # creates figure object.
    for value in lists[i]:  # iterates through each hyperparameter group
        fig.add_trace(  # adds each of the 4 data sets to a violin plot for the hyperparameter
            go.Violin(x0=listNames[i], y=dfList[i][value], name=value[-3:], legendgroup=listNames[i]))

    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(title_text='Hyperparameter: ' + listNames[i], violinmode='group',
                      yaxis=dict(range=[-0.0001, 0.0025], title='Fitness'))

    # Change legend location to overlap the left side of the figure.
    fig.update_layout(legend=dict(font=dict(family="Courier", size=12, color="black"), y=1, x=0),
                      legend_title=dict(font=dict(family="Courier", size=12, color="blue")))
    fig.show()
