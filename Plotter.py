#!/usr/bin/env python3.6
# RUN_AFPO.py
# Author: Shawn Beaulieu
# July 20th, 2018

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Plotter():

    """
    Plots AFPO data, assuming data structure hasn't been changed.

    """
    
    print("Loading Data...")

    data = pd.read_csv("AFPO_History.csv", header=None)
    max_id = np.max(data.iloc[:,2])
    colors = {i:np.random.random(3) for i in range(max_id+1)}

    trajectories = {i:{'fitness':[], 'age':None} for i in range(max_id+1)}

    print("Organizing Data...")

    for j in range(data.shape[0]):

        idx = data.iloc[j,2]
        trajectories[idx]['origin'] = data.iloc[j,3]
        if trajectories[idx]['age'] == None:
            trajectories[idx]['age'] = data.iloc[j,0]
            trajectories[idx]['fitness'].append(data.iloc[j,1])
    
        elif trajectories[idx]['age'] < data.iloc[j,0]:
            trajectories[idx]['age'] = data.iloc[j,0]
            trajectories[idx]['fitness'].append(data.iloc[j,1])
        
        elif trajectories[idx]['age'] == data.iloc[j,0]:
            if data.iloc[j,1] > trajectories[idx]['fitness'][-1]:
                trajectories[idx]['fitness'][-1] = data.iloc[j,1]

    print("Plotting...")
    for key in trajectories.keys():
        start = int(trajectories[key]['origin'])
        end = start+len(trajectories[key]['fitness'])
        trajectories[key]['time'] = list(range(start, end))

    plt.figure(figsize=(10, 7.5))
    for key in trajectories.keys():
        plt.plot(trajectories[key]['time'], trajectories[key]['fitness'], color=colors[key])

    plt.title("MaxOnes AFPO: Rainbow Waterfall")
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.show()

if __name__ == '__main__':

    Plotter()
