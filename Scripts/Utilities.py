import os

def checkIfFirstCharIsDigit(string):
    return string[0].isdigit()

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
                output.append(line)
        
        return subjectName, output

def getTimesElapsedWithNavigation(pathToTextFile):
    assert(os.path.exists(pathToTextFile), f"Text file at{pathToTextFile} does not exist!")

    with open(pathToTextFile) as f:
        subjectName = None
        output = []
        lines = f.readlines()
        start = lines[1] # In all positions, second line is always a valid numerical entry
        end = None
        for line in lines:
            if(checkIfFirstCharIsDigit(line)):
                end = line

        start = start.split()
        end = end.split()
        return (start, end)
    


