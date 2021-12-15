from scipy.stats.stats import kurtosis
from Constants import *
from Utilities import *
from os import listdir
import datetime
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

""" Test the data for Gaussian distribution """
timesElapsedWithAR = []
timesElapsedWithoutAR = []

def main():
    fillDataVariables()
    plotTimes()
    #testDataKS()

def splitDataIntoBins(array):
    
    pass

def plotTimes():
    plotData(timesElapsedWithAR, "With AR Navigation")    
    plotData(timesElapsedWithoutAR, "Without AR Navigation")    

def testDataKS():
    testPerformKS(timesElapsedWithAR, "With AR")
    testPerformKS(timesElapsedWithoutAR, "Without AR")

def plotData(resultArray, title):
    """ Plots the data as a histogram for qualitative analysis for data distribution

    Args:
        resultArray ([type]): dataset
        title ([type]): title of the plot
    """
    print(f"Plotting {title}")
    # Fit a normal distribution to the data:
    times = [x[1] for x in resultArray if x[0] != 'P1']
    mu, std = scipy.stats.norm.fit(times)
    
    # Plot the histogram.
    binwidth = 1
    bins = np.arange(min(times), max(times) + binwidth, binwidth)
    plt.hist(times, bins=bins, alpha=0.6, color='g')

    # Add labels and show
    plt.xlabel(f"Time bands ({binwidth} sec)")
    plt.ylabel("Number of test subjects")
    plt.title(title)
    plt.show()

def testPerformKS(resultArray, description):
    """ Performs the Kolmogorov-Smirnov Test on data with and without navigation """
    # Extract the times in seconds
    print(f"Plotting {description}")
    times = [x[1] for x in resultArray if x[0] != 'P1']

    print(f"Kurtosis {kurtosis(times)}")
    print(f"Skewness {scipy.stats.skew(times)}")
    output = scipy.stats.kstest(times, 'norm')
    pass

def fillDataVariables():
    """ Parses the Positions data directory and extracts start/finish
        time per each subject, split into with and without AR navigation
    """

    # Get the file directory
    files = listdir(FOLDER_DATA_POSITIONS)

    # Extract all file paths WITH and WITHOUT navigation
    resultsWithAr = [os.path.join(FOLDER_DATA_POSITIONS, x) for x in files if "WithAR" in x]
    resultsWithoutAR = [os.path.join(FOLDER_DATA_POSITIONS, x) for x in files if "WithoutAR" in x]

    # Extract the subject IDs and start/finish times per each subject and fill the global variables
    for fullFilePath in resultsWithAr:
        # Get start/finish time
        times = getTimesElapsedWithNavigation(fullFilePath)

        # Calculate delta time
        startTime = datetime.datetime.strptime(times[0], "%H:%M:%S.%f")
        endTime = datetime.datetime.strptime(times[1], "%H:%M:%S.%f")
        deltaTime = endTime - startTime

        # Derive test subject ID
        fileName = os.path.basename(fullFilePath)
        subjectID = fileName.split("_WithAR")[0]

        # Append delta time with test subject ID
        timesElapsedWithAR.append((subjectID, deltaTime.seconds))
        
    for fullFilePath in resultsWithoutAR:
        # Get start/finish time
        times = getTimesElapsedWithNavigation(fullFilePath)

        # Calculate delta time
        startTime = datetime.datetime.strptime(times[0], "%H:%M:%S.%f")
        endTime = datetime.datetime.strptime(times[1], "%H:%M:%S.%f")
        deltaTime = endTime - startTime

        # Derive test subject ID
        fileName = os.path.basename(fullFilePath)
        subjectID = fileName.split("_WithoutAR")[0]

        # Append delta time with test subject ID
        timesElapsedWithoutAR.append((subjectID, deltaTime.seconds))


if __name__ == '__main__':
    main()