import os

def getAbsPath(relativePath):
    output = os.path.abspath( os.path.join( os.path.dirname( __file__ ), relativePath) )
    if (os.path.exists(output)):
        return output
    else:
        raise Exception(f"Path <{relativePath}> relative to Constants.py does not exis")


FOLDER_DATA_POSITIONS = getAbsPath("../Data/Positions")
FOLDER_DATA_QUESTIONNAIRE = getAbsPath("../Data/Questionnaire")
FOLDER_DATA_SCENE = getAbsPath("../Data/arScene")
FOLDER_GRAPHS_POSITIONS = getAbsPath("../Graphs/Positions")
FOLDER_GRAPHS_HEATMAPS = getAbsPath("../Graphs/Heatmaps")

