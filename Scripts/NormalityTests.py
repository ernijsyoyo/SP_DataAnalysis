from math import sqrt
from scipy.stats.stats import kurtosis
from Constants import *
from Utilities import *
from os import listdir
import datetime
import scipy.stats
from scipy.stats import anderson
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import ksone
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import poisson

""" Test the data for Gaussian distribution """
timesElapsedWithAR = []
timesElapsedWithoutAR = []

hurriedWith = []
hurriedWithout = []
hardworkWith = []
hardworkWithout = []
insecureWith = []
insecureWithout = []
mentaldemandWith = []
mentaldemandWithout = []
physicaldemandWith = []
physicaldemandWithout = []
successWith = []
successWithout = []

def main():
    fillDataVariables()
    print("")

    dataWithAR = [x[1] for x in timesElapsedWithAR if x[0] != 'P1']
    dataWithoutAR = [x[1] for x in timesElapsedWithoutAR]

    tmp1 : np.ndarray=np.array(dataWithAR)
    tmp2 : np.ndarray=np.array(dataWithoutAR)

    print(tmp1.mean())
    print(tmp1.std())
    print(tmp2.mean())
    print(tmp2.std())
    

    # testPerformSW(hurriedWith[0][1], "hurriedWith")
    # testPerformSW(hurriedWithout[0][1], "hurriedWithout")
    # testPerformSW(hardworkWith[0][1], "hardworkWith")
    # testPerformSW(hardworkWithout[0][1], "hardworkWithout")
    # testPerformSW(insecureWith[0][1], "insecureWith")
    # testPerformSW(insecureWithout[0][1], "insecureWithout")
    # testPerformSW(mentaldemandWith[0][1], "mentaldemandWith")
    # testPerformSW(mentaldemandWithout[0][1], "mentaldemandWithout")
    # testPerformSW(physicaldemandWith[0][1], "physicaldemandWith")
    # testPerformSW(physicaldemandWithout[0][1], "physicaldemandWithout")
    # testPerformSW(successWith[0][1], "successWith")
    # testPerformSW(successWithout[0][1], "successWithout")

    plotTimes(dataWithAR, dataWithoutAR)
    testDataKS(dataWithAR, dataWithoutAR)
    testDataAD(dataWithAR, dataWithoutAR)
    testDataSW(dataWithAR, dataWithoutAR)
    


def plotTimes(withAR, withoutAR):
    plotData(withAR, f"n={len(withAR)}")    
    plotData(withoutAR, f"n={len(withoutAR)}")    


def testDataKS(withAR, withoutAR):
    testPerformKS(withAR, "With AR")
    testPerformKS(withoutAR, "Without AR")

def testDataAD(withAR, withoutAR):
    testPerformAD(withAR, "With AR")
    testPerformAD(withoutAR, "Without AR")

def testDataSW(withAR, withoutAR):
    testPerformSW(withAR, "With AR")
    testPerformSW(withoutAR, "Without AR")


#######################################################################################

def plotData(resultArray, title):
    """ Plots the data as a histogram for qualitative analysis for data distribution

    Args:
        resultArray ([type]): dataset
        title ([type]): title of the plot
    """
    # Extract the
    times, bins = convertDataIntoBins(resultArray, 1)
    
    # Plot the histogram and add labels
    fig,ax = plt.subplots(1, 1)
    ax.hist(times, bins=bins, density=False, edgecolor = "black", color = 'green')
    ax.set_yticks([0, 1, 2])
    ax.set_xlabel(f"Time(s)")
    ax.set_ylabel("Number of test subjects")
    ax.title.set_text(title)

    # Annotate with precise X axis data
    for i, rect in enumerate(ax.patches):
        height = rect.get_height()
        addToLabelHeight = 0.1
        if height == 0:
            continue
        
        if(i % 2):
            addToLabelHeight += 0.03
        else:
            addToLabelHeight -= 0.05
        ax.annotate(f'{int(rect.get_x())}', xy=(rect.get_x()+rect.get_width()/2, height + addToLabelHeight), 
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    fig.savefig(f"{os.path.join(FOLDER_GRAPHS_POSITIONS, title)}.png")
    plt.show()


def testPerformSW(input, description):
    """ Performs Shapiro-Wilk test on the input data """
    print(f"Performing Shapiro-Wilk Test with {description}")

    # normality test
    stat, p = shapiro(input)
    print('Statistics=%.3f, p=%.3f' % (stat, p))

    # interpret
    alpha = 0.05
    if p > alpha:
        print('Data looks normal (accept H0)\n')
    else:
        print('Data does not look normal (reject H0) \n')


def testPerformAD(input, description):
    """ Perform Anderson-Darling test on the input data """
    print(f"Performing Anderson-Darling Test with {description}")

    # normality test
    result = anderson(input)
    print('Statistic: %.3f' % result.statistic)
    sl, cv = result.significance_level[2], result.critical_values[2] # 5% confidence
    statistic = result.statistic
    
    # Evaluate
    if statistic < cv:
        print('%.3f: %.3f, Data looks normal (accept H0)\n' % (sl, cv))
    else:
        print('%.3f: %.3f, Data does not look normal (reject H0)\n' % (sl, cv))


def testPerformKS(input, description):
    """ Performs the Kolmogorov-Smirnov Test on data with and without navigation """
    print(f"Plotting {description}")
     
    # Prepare the data
    sorted = np.sort(input, axis=0)
    # Calculate the zScore and obtain the critical value
    zScores = (sorted - sorted.mean()) / (sorted.std())
    criticalValue = ksone.ppf(1 - 0.05 / 2, len(input))

    # Run the test and evaluate
    output = scipy.stats.kstest(zScores, 'norm')
    if(output.pvalue > criticalValue):
        print(f"p0: {output.pvalue}; Critical value: {criticalValue}. Data looks normal (accept H0)")
    else:
        print(f"p0: {output.pvalue}; Critical value: {criticalValue}. Data does not look normal (reject H0)")
    

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

    # Questionnaire
    files = listdir(FOLDER_DATA_QUESTIONNAIRE)
    questionnarePaths = [os.path.join(FOLDER_DATA_QUESTIONNAIRE, x) for x in files]
    for fullFilePath in questionnarePaths:
        if "HardWorkWith" == os.path.basename(fullFilePath):
            hardworkWith.append(getLinesFromTextFile(fullFilePath))
            
        elif "HardWorkWithout" == os.path.basename(fullFilePath):
            hardworkWithout.append(getLinesFromTextFile(fullFilePath))
            
        elif "HurriedWith" == os.path.basename(fullFilePath):
            hurriedWith.append(getLinesFromTextFile(fullFilePath))
            
        elif "HurriedWithout" == os.path.basename(fullFilePath):
            hurriedWithout.append(getLinesFromTextFile(fullFilePath))
            
        elif "InsecureWith" == os.path.basename(fullFilePath):
            insecureWith.append(getLinesFromTextFile(fullFilePath))

        elif "InsecureWithout" == os.path.basename(fullFilePath):
            insecureWithout.append(getLinesFromTextFile(fullFilePath))

        elif "MentalDemandWith" == os.path.basename(fullFilePath):
            mentaldemandWith.append(getLinesFromTextFile(fullFilePath))

        elif "MentalDemandWithout" == os.path.basename(fullFilePath):
            mentaldemandWithout.append(getLinesFromTextFile(fullFilePath))

        elif "PhysicalDemandWith" == os.path.basename(fullFilePath):
            physicaldemandWith.append(getLinesFromTextFile(fullFilePath))

        elif "PhysicalDemandWithout" == os.path.basename(fullFilePath):
            physicaldemandWithout.append(getLinesFromTextFile(fullFilePath))

        elif "SuccessWith" == os.path.basename(fullFilePath):
            successWith.append(getLinesFromTextFile(fullFilePath))

        elif "SuccessWithout" == os.path.basename(fullFilePath):
            successWithout.append(getLinesFromTextFile(fullFilePath))



if __name__ == '__main__':
    main()