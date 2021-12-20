#from src.project.oscNetwork import OscNetwork
#import matplotlib.pylab as plt
from __future__ import annotations
import re
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
from Utilities import *
from Constants import *
from scipy.ndimage.interpolation import shift

from os import listdir


positionsWithAR = []
positionsWithoutAR = []
markerLocations = []

def main():
    markerLocations = getMarkerLocations()
    posWithAr, posWithoutAr = fillVariables()
    npPosWith = np.array(posWithAr)
    npPosWithout = np.array(posWithoutAr) 
    plotHeatmap(npPosWith, markerLocations, "WithNav")
    plotHeatmap(npPosWithout, markerLocations, "WithoutNav")

def plotHeatmap(input, markers, str):
    for entry in input:
        for x in entry.items():
            entriesX = [i[0] for i in x[1]]
            entriesZ = [i[1] for i in x[1]]
            entriesX = np.repeat(np.array(entriesX), 1) 
            entriesZ = np.repeat(np.array(entriesZ), 1) 

            heatmap, xedges, yedges = np.histogram2d(entriesZ, entriesX, bins=50)
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

            fig, ax = plt.subplots()
            
            plt.text(entriesZ[0], entriesX[0] + 0.2, "Start", color='w')                   
            plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', interpolation='nearest')
            plt.title(x[0])
            plt.savefig(f"{x[0]}_{str}.png")

            


            # x = [i[1][0] for i in markers]
            # z = [i[1][2] for i in markers]
            # ids = [i[0] for i in markers]
            # fig, ax = plt.subplots()
            # colors = ['k'] * len(x)
            # colors[-1] = 'r'

            # # Starting point
            # x.append(-0.5)
            # z.append(2)
            # ids.append("Starting Point")
            # colors.append('g')

            # rect = patches.Rectangle((0, 5.5), 5.8, -8.8, linewidth=1, edgecolor='c', fill=False)
            # ax.add_patch(rect)
            # ax.scatter(z, x, c=colors)
            # ax.scatter([],[],c='k',label='Destination IDs')
            # ax.scatter([],[],c='r',label='Global Origin (0, 0, 0)')
            # ax.scatter([],[],c='g',label='Fixed Starting Location')
            # ax.scatter([],[],c='c',label='Environment boundaries')
            # ax.set_ylabel("Length(m) relative to global point of origin")
            # ax.set_xlabel("Width(m) relative to global point of origin")
            # ax.set_title("Illustration of the Test Lab")
            # ax.legend(loc='best')

            # # annotate
            # for i, txt in enumerate(ids):
            #     ax.annotate(f"{txt}", (z[i] + 0.1, x[i]+ 0.05))


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

    markerLocations = parseScene(arScene[0])

    return posWithAr, posWithoutAr



def getMarkerLocations():
    # Get the file directory
    positionFiles = listdir(FOLDER_DATA_POSITIONS)
    arScene = listdir(FOLDER_DATA_SCENE)

    # Extract all file paths WITH and WITHOUT navigation
    arScene = [os.path.join(FOLDER_DATA_SCENE, x) for x in arScene]
    return parseScene(arScene[0])
    

if __name__ == '__main__':
    main()