from flask import Flask, render_template, request, redirect, url_for, jsonify
import Pins

app = Flask(__name__)

# return index page when IP address of RPi is typed in the browser
@app.route("/")
def Index():
    return render_template("index.html", uptime=GetUptime())

# ajax GET call this function to set led state
# depeding on the GET parameter sent
@app.route("/_led")
def _led():
    state = request.args.get('state')
    if state=="on":
        Pins.LEDon()
    else:
        Pins.LEDoff()
    return ""

# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_button")
def _button():
    if Pins.ReadButton():
        state = "pressed"
    else:
        state = "not pressed"
    return jsonify(buttonState=state)


# Help me plaese!
# After submit message, adress in browser - 192.168.1.38:8000/_change/, is not  - 192.168.1.38:8000/. Help me plaese!
@app.route("/_change", methods=['POST'])
def _change():
    if request.method == 'POST':
        # Get the value from the submitted form
        lcdText = request.form['lcd']
        print "---Message is", lcdText

        # Send the message to the LCD  
        # lcd.clear()  
        # lcd.message(lcdText)  
    else:
        lcdText = None
    return jsonify(value=lcdText)        # - is not work
	# return ""                          # - is not work 
	# return redirect(url_for("Index"))  # - is not work 
    # return render_template("index.html", value=lcdText) # - is not work


def GetUptime():
    # get uptime from the linux terminal command
    from subprocess import check_output
    output = check_output(["uptime"])
    # return only uptime info
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime
    
# run the webserver on standard port 80, requires sudo
if __name__ == "__main__":
    Pins.Init()
    app.run(host='0.0.0.0', port=8000, debug=True)
	
