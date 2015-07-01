import time
from threading import Thread
# Input states
indState = [0, 0, 0, 0]
timeVar = 0

sumup = time.time() + 5
duration = time.time() + 10
overtime = 5

def readInd(_inputNum):
    return indState[_inputNum]

def setInd(_inputNum, _state):
    indState[_inputNum] = _state

def countdown():
    global timeVar
    
    while True:
        n = time.time()
        #print(round(duration - n))
        timeVar = round(duration - n)
        
        if n < sumup:
            setInd(1, 1)			# "Talk"
            setInd(2, 0)
            setInd(3, 0)
        elif n > sumup and n < duration:				
            setInd(1, 0)			# "Sum-up"
            setInd(2, 1)
            setInd(3, 0)
            #print("Sum-up")
        elif n > duration and n < duration + overtime:
            setInd(1, 0)			# "Stop"
            setInd(2, 0)
            setInd(3, 1)
            #print("Stop")
        elif n > duration + overtime:
            setInd(1, 0)			# "Overtime"
            setInd(2, 0)
            setInd(3, 1)
            #print("Overtime")
        time.sleep(0.5)

t = Thread(target=countdown)
t.daemon = True
t.start()

while True:
    print(timeVar)
