# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:24:04 2020
Version 10/23/20
@author: Sam
"""


# copy command: for .pkl and .log
# cp /scratch/kingspeak/serial/u1008557/JOBID#/*.pkl .; 
# cp /scratch/kingspeak/serial/u1008557/JOBID#/*.log .;

import shutil
import os

# directory labels
scratch = "/scratch/kingspeak/serial/u1008557/"
test_dir = "tdata_binaries"
superfolder = ["t2", "t4", "t6", "t8", "t10"]
subfolder = ["00000", "00001", "00010", "00011", "00111", "10110", "10111"]
trials = ["trial0", "trial1", "trial2", "trial3", "trial4"]

jobID = []
#  add job ID's to list
for a in range(1683377, 1683552):
    jobID.append(str(a))
print(jobID[-1])
k = 0 # index for the jobID corrosponding to the current test directory

# construct filepaths between each test directory and the corrosponding bin within
# the scratch directory labeled by the tests jobID and containing the relevant .pkl &.log
# required to run plot_from_pickle.py
for i in range(len(superfolder)):
    for j in range(len(subfolder)):
        for n in range(len(trials)):
            source = scratch + jobID[k] + "/"
            k+=1
            destination = "/uufs/chpc.utah.edu/common/home/u1008557/" + test_dir + "/" + superfolder[i] + "/" + subfolder[j] + "/" + trials[n] + "/"
            
            # copies all .pkl & .log files from the scratch dir to the test dir.
            for filename in os.listdir(source): 
                if filename.endswith('.pkl'):
                    fileSource = source + filename
                    shutil.copy(fileSource, destination)
                if filename.endswith('.log'):
                    fileSource = source + filename
                    shutil.copy(fileSource, destination)
