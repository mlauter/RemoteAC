from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.socketio import SocketIO, send, emit
import datetime
import db

app = Flask(__name__)
global desired_state
desired_state = False

from collections import namedtuple
AcState = namedtuple('AcState', ['timestamp','temp','is_running'])

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
#the homepage route, reads latest entry from database and renders index.html
def homepage():
	last_ac_state = db.get_last_ac_state()
	temp = last_ac_state[2]
	running = last_ac_state[3]
	return render_template('index.html', temp = temp, running = bool(running), time=datetime.datetime.now())

@app.route('/ac_status', methods=['POST'])
#the route for the rpi to ping with latest state info (temp and on/off)
#returns desired state
def temp_update():
	temp = float(request.form['temperature'])
	is_running = bool(int(request.form['is_running']))
	db.add_ac_state(AcState(datetime.datetime.now(),temp,is_running))
	global desired_state
	return jsonify(desired_state=desired_state)

@app.route('/switch_state', methods=['POST'])
#the route for the UI button press, updates desired state and re-renders homepage
def switch_state():
	global desired_state
	desired_state = bool(int(request.form['switch']))
	return redirect(url_for('homepage'))

if __name__=="__main__":
	app.run(debug=True)
