import os
import numpy as np

def checkIfFirstCharIsDigit(string):
    return string[0].isdigit()

def convertDataIntoBins(data, width):
    """Returns the given data quantized into bins of a given width. Bin range is the value + width

    Args:
        data ([type]): Array of the data that we want to categorize in bins
        width ([type]): Width of a bin
    """

    minimum = min(data)
    maximum = max(data)
    bins = np.arange(minimum, maximum + width, width)
    digitized = np.digitize(data, bins)
    output = np.array([])
    for i in digitized:
        output = np.append(output, bins[i - 1])

    return output, bins


def getLinesFromTextFile(pathToTextFile):
    assert(os.path.exists(pathToTextFile), f"Text file at{pathToTextFile} does not exist!")
    
    with open(pathToTextFile) as f:
        subjectName = None
        output = []
        for line in f.readlines():
            if line == '\n':
                continue
            elif not line[0].isdigit():
                subjectName = line
            else:
                tmp = line.strip("\n")
                tmp = int(tmp)
                output.append(tmp)
        
        return subjectName, output

def getTimesElapsedWithNavigation(pathToTextFile):
    assert(os.path.exists(pathToTextFile), f"Text file at{pathToTextFile} does not exist!")

    with open(pathToTextFile) as f:
        lines = f.readlines()
        start = lines[1] # In all positions, second line is always a valid numerical entry
        end = None

        # Get the last line that is a numerical entry
        for line in lines:
            if(checkIfFirstCharIsDigit(line)):
                end = line

        # Prepare the output and return it
        start = start.split()[0]
        end = end.split()[0]
        return (start, end)

    


