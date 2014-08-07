from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.socketio import SocketIO, send, emit
import datetime
import db

app = Flask(__name__)
#socketio = SocketIO(app)
global desired_state
desired_state = False

#ac_state = {
#	'powered_on': False,
#	'current_temperature': 73,
#	'desired_temperature': 70
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
	global desired_state
	# if desired_state == "turn on":
	# 	if is_running:
	# 		desired_state = "do nothing"
	# 	else:
	# 		return "turn on"
	# elif desired_state=="turn off":
	# 	if is_running:
	# 		return "turn off"
	# 	else:
	# 		desired_state = "do nothing"
	return jsonify(desired_state=desired_state)

@app.route('/switch_state', methods=['POST'])
def switch_state():
	global desired_state
	desired_state = bool(int(request.form['switch']))
	#print desired_state
	#return render_template('switch_request.html', desired_state=desired_state)
	return redirect(url_for('homepage'))

if __name__=="__main__":
	app.run(debug=True)
