import os
import numpy as np
import datetime
from dataclasses import dataclass
import collections
import xml.etree.ElementTree as ET

@dataclass
class subjectEntry():
    id : int
    totalTime : float
    locations = []

def parseScene(pathToXML):
    tree = ET.parse(pathToXML)
    root = tree.getroot()
    output = []
    for elm in root.findall("./Marker"):
        # 1. Extract pivot point and pivot orientation
        # 2. Create a mesh object and initialize it with the pivots, vertices, face
        # 3. Set the mesh object equal to the mesh member variable
        #self.mesh = Mesh(pivotPoint, pivotOrientat, self.vrtx, self.fc)
        atbpos = elm.attrib.get("pos")
        pos = convertStringToVec3(atbpos, 2)
        atbID = int(elm.attrib.get("id"))

        output.append((atbID, pos))
    return output
    

def checkIfFirstCharIsDigit(string):
    return string[0].isdigit()

def convertStringToVec3(input, roundingDigit):
    input = input.replace('(', '').replace(')', '').replace('\n','').replace(',', '')
    output = np.array(input.split(), dtype=np.float32)
    output = output.round(roundingDigit)
    return output


def getPositionsFromText(pathToTextFile):
    assert(os.path.exists(pathToTextFile), f"Text file at{pathToTextFile} does not exist!")
    
    with open(pathToTextFile) as f:
        subjectName = None
        output = collections.defaultdict(list)
        outputList = np.array([])
        for line in f.readlines():
            # Skip all new lines
            if line == '\n':
                continue
            
            # Set subject name as key
            elif not checkIfFirstCharIsDigit(line):
                lineSplit = line.split()
                subjectName = lineSplit[0] + lineSplit[1]
            
            # Prepare an entry to the output dictionary
            else:
                entry = line.split(" ", 1)
                #time = entry[0][:-4] # leave 10th of miliseconds in time
                position = convertStringToVec3(entry[1], 3)
                position = np.delete(position, 1)
                
                if(not position in outputList):
                    outputList = np.append(outputList, position)

                    outputEntry = position
                    output[subjectName].append(outputEntry)
        
        return output


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

    


