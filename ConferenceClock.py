from flask import Flask, render_template, request, jsonify
import thread as Thread
import pirsclockfull as clock
#import test as clock

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

@app.route("/_ind")
def _ind():
    state = request.args.get('state')
    if state=="1":
        clock.setInd(1, 1)
        clock.setInd(2, 0)
        clock.setInd(3, 0)
    elif state=="2":
        clock.setInd(1, 0)
        clock.setInd(2, 1)
        clock.setInd(3, 0)        
    elif state=="3":
        clock.setInd(1, 0)
        clock.setInd(2, 0)
        clock.setInd(3, 1)  
    else:
        clock.setInd(1, 0)
        clock.setInd(2, 0)
        clock.setInd(3, 0)    
    return ""

# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_onAirState")
def _onAirState():
    if clock.readInd(0):
        state = "on"
    else:
        state = "off"
    return jsonify(onAirState=state)

def GetUptime():
    # get uptime from the linux terminal command
    from subprocess import check_output
    output = check_output(["uptime"])
    # return only uptime info
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime

def start_web_server():
    # run the webserver on standard port 80, requires sudo
    app.run(host='0.0.0.0', port=80, debug=False)

t = Thread(target=start_web_server())
t.daemon = True
t.start()

while True :
    clock.drawclock()

    
