from Constants import *
from Utilities import *
from os import listdir
from os.path import isfile, join


""" Test the data for Gaussian distribution """
print(FOLDER_DATA_POSITIONS)
print(FOLDER_DATA_QUESTIONNAIRE)

files = listdir(FOLDER_DATA_POSITIONS)
files = [os.path.join(FOLDER_DATA_POSITIONS, x) for x in files]

data = []

for file in files:
    subjectName, output = getLinesFromTextFile(file)
    data.append((subjectName, output))
    pass