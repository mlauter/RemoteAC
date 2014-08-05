from flask import Flask, render_template, request, redirect, url_for
from flask.ext.socketio import SocketIO, send, emit
import datetime
import db

app = Flask(__name__)
#socketio = SocketIO(app)
global requested_state
requested_state = "do nothing"

#ac_state = {
#	'powered_on': False,
#	'current_temperature': 73,
#	'requested_temperature': 70
#}

from collections import namedtuple
AcState = namedtuple('AcState', ['timestamp','temp','is_running'])

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def homepage():
	last_ac_state = db.get_last_ac_state()
	temp = last_ac_state[2]
	running = last_ac_state[3]
	return render_template('index.html', temp = temp, running = bool(running), time=datetime.datetime.now())

@app.route('/ac_status', methods=['POST'])
def temp_update():
	temp = float(request.form['temperature'])
	is_running = bool(int(request.form['is_running']))
	db.add_ac_state(AcState(datetime.datetime.now(),temp,is_running))
	global requested_state
	if requested_state == "turn on":
		if is_running:
			requested_state = "do nothing"
		else:
			return "turn on"
	elif requested_state=="turn off":
		if is_running:
			return "turn off"
		else:
			requested_state = "do nothing"
	return ''

@app.route('/switch_state', methods=['POST'])
def switch_state():
	global requested_state
	if request.form['switch'] == "1":
		requested_state = "Turn on"
	else:
		requested_state = "Turn off"
	ac_state["powered_on"] = bool(int(request.form['switch']))
	#print requested_state
	return render_template('switch_request.html', requested_state=requested_state)
	#return redirect(url_for('homepage'), code=307)

if __name__=="__main__":
	app.run(debug=True)
