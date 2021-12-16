from scipy.stats.stats import kurtosis
from Constants import *
from Utilities import *
from os import listdir
import datetime
import scipy.stats
from scipy.stats import anderson
from scipy.stats import shapiro
from scipy.stats import normaltest
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import poisson

""" Test the data for Gaussian distribution """
timesElapsedWithAR = []
timesElapsedWithoutAR = []

def main():
    fillDataVariables()
    print("")
    testDataAgostino()
    testDataAD()
    testDataSW()
    testDataKS()
    plotTimes()

def plotTimes():
    plotData(timesElapsedWithAR, "With AR")    
    plotData(timesElapsedWithoutAR, "Without AR")    

def testDataAgostino():
    testPerformDAgostino(timesElapsedWithAR, "With AR")
    testPerformDAgostino(timesElapsedWithoutAR, "Without AR")

def testDataKS():
    testPerformKS(timesElapsedWithAR, "With AR")
    testPerformKS(timesElapsedWithoutAR, "Without AR")

def testDataAD():
    testPerformAD(timesElapsedWithAR, "With AR")
    testPerformAD(timesElapsedWithoutAR, "Without AR")

def testDataSW():
    testPerformSW(timesElapsedWithAR, "With AR")
    testPerformSW(timesElapsedWithoutAR, "Without AR")


#######################################################################################

def plotData(resultArray, title):
    """ Plots the data as a histogram for qualitative analysis for data distribution

    Args:
        resultArray ([type]): dataset
        title ([type]): title of the plot
    """
    # Extract the
    times = [x[1] for x in resultArray]
    times, bins = convertDataIntoBins(times, 5)
    
    # Plot the histogram and add labels
    plt.hist(times, bins=bins, alpha=0.6, color='g')
    plt.xlabel(f"Time bands ( sec)")
    plt.ylabel("Number of test subjects")
    plt.title(title)
    plt.show()


def testPerformSW(input, description):
    """ Performs Shapiro-Wilk test on the input data """
    print(f"Performing Shapiro-Wilk Test with {description}")

    # normality test
    data = [x[1] for x in input]
    stat, p = shapiro(data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))

    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')


def testPerformDAgostino(input, description):
    """ Performs DAgostino test on the input data """
    print(f"Performing DAgostino Test with {description}")
    
    # normality test
    data = [x[1] for x in input]
    stat, p = normaltest(data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))

    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')


def testPerformAD(input, description):
    """ Perform Anderson-Darling test on the input data """
    print(f"Performing Anderson-Darling Test with {description}")

    # normality test
    data = [x[1] for x in input]
    result = anderson(data)
    print('Statistic: %.3f' % result.statistic)
    p = 0

    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
        else:
            print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))


def testPerformKS(withNavigation, description):
    """ Performs the Kolmogorov-Smirnov Test on data with and without navigation """
    # Extract the times in seconds
    print(f"Plotting {description}")
    withNav = [x[1] for x in withNavigation]

    output = scipy.stats.kstest(withNav, 'norm')
    print(output)
    

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