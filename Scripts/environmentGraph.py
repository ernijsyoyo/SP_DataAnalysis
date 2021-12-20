#!/usr/bin/python3
from __future__ import annotations
import re
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
from Utilities import *
from Constants import *
from scipy.ndimage.interpolation import shift

from os import listdir

def main():
    markerLocations = getMarkerLocations()
    plotScatter(markerLocations)

def plotScatter(markerLocations):
    x = [i[1][0] for i in markerLocations]
    z = [i[1][2] for i in markerLocations]
    ids = [i[0] for i in markerLocations]
    fig, ax = plt.subplots()
    colors = ['k'] * len(x)
    colors[-1] = 'r'

    # Starting point
    x.append(-0.5)
    z.append(2)
    ids.append("Starting Point")
    colors.append('g')

    rect = patches.Rectangle((0, 5.5), 5.8, -6, linewidth=1, edgecolor='c', fill=False)
    ax.add_patch(rect)
    ax.scatter(z, x, c=colors)
    ax.scatter([],[],c='k',label='Destination IDs')
    ax.scatter([],[],c='r',label='Global Origin (0, 0, 0)')
    ax.scatter([],[],c='g',label='Fixed Starting Location')
    # ax.scatter([],[],c='c',label='Environment boundaries')
    ax.set_ylabel("Length(m) relative to global point of origin")
    ax.set_xlabel("Width(m) relative to global point of origin")
    ax.set_title("Illustration of the Optimum Path Without Navigation")
    ax.legend(loc='best')

    # annotate
    for i, txt in enumerate(ids):
        ax.annotate(f"{txt}", (z[i] + 0.1, x[i]+ 0.05))

    # Add starting point

    plt.show()


def getMarkerLocations():
    # Get the file directory
    positionFiles = listdir(FOLDER_DATA_POSITIONS)
    arScene = listdir(FOLDER_DATA_SCENE)

    # Extract all file paths WITH and WITHOUT navigation
    arScene = [os.path.join(FOLDER_DATA_SCENE, x) for x in arScene]
    return parseScene(arScene[0])
    


if __name__ == '__main__':
    main()