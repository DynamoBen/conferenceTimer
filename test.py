# Input states
indState = [0, 0, 0, 0]

def readInd(_inputNum):
    return indState[_inputNum]

def setInd(_inputNum, _state):
    indState[_inputNum] = _state
