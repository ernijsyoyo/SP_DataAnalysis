#!/usr/bin/python3

""" 
Generates heatmaps for each test subject's movement trajectory. 
Each heatmap is displayed and automatically saved in ../Graphs/Heatmaps/ directory
"""

from __future__ import annotations
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
from Utilities import *
from Constants import *
from scipy.ndimage.interpolation import shift
import pathlib

from os import listdir


def main():
    posWithAr, posWithoutAr = fillVariables()
    npPosWith = np.array(posWithAr)
    npPosWithout = np.array(posWithoutAr) 
    plotHeatmap(npPosWith, "WithNav")
    plotHeatmap(npPosWithout, "WithoutNav")

def plotHeatmap(input, str):
    """[summary]

    Args:
        input List[ Dictionary{String, List} ]: Contains a test participant ID and its corresponding position entries
        str ([type]): [description]
    """
    # Loop over each dictionary's values
    for dictEntry in input:
        for value in dictEntry.items():
            # Extract X and Z values from the position entry list
            entriesX = [i[0] for i in value[1]]
            entriesZ = [i[1] for i in value[1]]

            # Generate a heatmap with Numpy
            heatmap, xedges, yedges = np.histogram2d(entriesZ, entriesX, bins=50)
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            
            # Annotate the image, save it and show it
            plt.text(entriesZ[0], entriesX[0] + 0.2, "Start", color='w')                   
            plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', interpolation='nearest')
            plt.title(f"{value[0]} {str} ")
            outputPath = os.path.join(FOLDER_GRAPHS_HEATMAPS, f"{value[0]}_{str}.png")
            plt.savefig(outputPath)
            print(f"Saved {outputPath}")
            plt.show()



def fillVariables():
    # Get the file directory
    positionFiles = listdir(FOLDER_DATA_POSITIONS)
    arScene = listdir(FOLDER_DATA_SCENE)
    posWithAr = []
    posWithoutAr = []

    # Extract all file paths WITH and WITHOUT navigation
    resultsWithAr = [os.path.join(FOLDER_DATA_POSITIONS, x) for x in positionFiles if "WithAR" in x]
    resultsWithoutAR = [os.path.join(FOLDER_DATA_POSITIONS, x) for x in positionFiles if "WithoutAR" in x]
    arScene = [os.path.join(FOLDER_DATA_SCENE, x) for x in arScene]

    # Extract the subject IDs and start/finish times per each subject and fill the global variables
    for fullFilePath in resultsWithAr:
        # Get start/finish time
        posWithAr.append(getPositionsFromText(fullFilePath))

    for fullFilePath in resultsWithoutAR:
        # Get start/finish time
        posWithoutAr.append(getPositionsFromText(fullFilePath))

    return posWithAr, posWithoutAr

    

if __name__ == '__main__':
    main()