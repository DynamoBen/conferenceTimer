# http://weblogs.asp.net/yousefjadallah/grid-layout-in-jquery-mobile

from flask import Flask, render_template, request, jsonify
from threading import Thread
import pirsclockfull as clock
import time

durationTime = 0
sumupTime = 0
timeRemaining = 0
timerState = False

app = Flask(__name__)

# return index page when IP address of RPi is typed in the browser
@app.route("/")
def Index():
    return render_template("index.html", uptime=GetUptime())

# ajax GET call this function to set led state
# depeding on the GET parameter sent
@app.route("/_onAir")
def _onAir():
    state = request.args.get('state')
    if state=="on":
        clock.setInd(0, 1)
    else:
        clock.setInd(0, 0)
    return ""

@app.route("/_timer")
def _timer():
    global timerState
    global timeRemaining
    global sumupTime
    global durationTime
    
    state = request.args.get('state')
    
    if state=="start":     
        if timeRemaining <= 0:
            durationTime = int(request.args.get('duration')) * 60
            sumupTime = int(request.args.get('sumup')) * 60
            timeRemaining = durationTime
        timerState = True
        
    elif state=="stop":
        timerState = False
        
    elif state=="clear":
        timerState = False

        timeRemaining = 0

        clock.setInd(1, 0)			# Clear Indicators
        clock.setInd(2, 0)
        clock.setInd(3, 0)	        
    return ""
    
# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_status")
def _status():
    if clock.readInd(0):
        onAirstatus = "on"
    else:
        onAirstatus = "off"

    if clock.readInd(1):
        indStatus = clock.txt2
    elif clock.readInd(2):
        indStatus = clock.txt3
    elif clock.readInd(3):
        indStatus = clock.txt4   
    else:
        indStatus = "None"

    return jsonify(indState=indStatus,onAirState=onAirstatus,time=(timeRemaining/60),duration=(durationTime/60),sumup=(sumupTime/60))    
	
def GetUptime():
    # get uptime from the linux terminal command
    from subprocess import check_output
    output = check_output(["uptime"])
    # return only uptime info
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime

def indicators_timer():
    global timeRemaining
    global timerState
    global sumupTime

    while True:
        if timerState == True:
            timeRemaining -= 1
            
            if timeRemaining > sumupTime:
                clock.setInd(1, 1)			# "Talk"
                clock.setInd(2, 0)
                clock.setInd(3, 0)	
            elif timeRemaining <= sumupTime and timeRemaining > 0:				
                clock.setInd(1, 0)			# "Sum-up"
                clock.setInd(2, 1)
                clock.setInd(3, 0)
            elif timeRemaining <= 0:
                clock.setInd(1, 0)			# "Stop"
                clock.setInd(2, 0)
                clock.setInd(3, 1)
                timerState = False
                 
        time.sleep(1)

def start_web_server():
    # run the webserver on standard port 80, requires sudo
    app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False, threaded=True)  

t = Thread(target=start_web_server)
t.daemon = True
t.start()

c = Thread(target=indicators_timer)
c.daemon = True        
c.start() 

while True:
    clock.drawclock()

    
