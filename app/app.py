from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.socketio import SocketIO, send, emit
import threading
import datetime
import time
import db

app = Flask(__name__)
global desired_state
desired_state = False
global desired_temp
desired_temp = 100
global home_mode
home_mode = False

from collections import namedtuple
AcState = namedtuple('AcState', ['timestamp','temp','is_running'])

# def waituntil(condition,timeout,period=0.25)
# 	while True:
# 		if condition(): return True
# 		time.sleep(period)
# 	return False 

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
#the homepage route, reads latest entry from database and renders index.html
def homepage():
	last_ac_state = db.get_last_ac_state()
	temp = last_ac_state[2]
	running = bool(last_ac_state[3])
	return render_template('index.html', temp = temp, running = running, time=datetime.datetime.now())

@app.route('/ac_status', methods=['POST'])
#the route for the rpi to ping with latest state info (temp and on/off)
#returns desired state
def temp_update():
	temp = float(request.form['temperature'])
	is_running = bool(int(request.form['is_running']))
	db.add_ac_state(AcState(datetime.datetime.now(),temp,is_running))
	global desired_state
	global desired_temp
	global home_mode
	return jsonify(desired_state=desired_state, desired_temp=desired_temp, home_mode=home_mode)

@app.route('/switch_state', methods=['GET'])
#the route for the UI button press, updates desired state and re-renders homepage
def switch_state():
	global desired_state
	desired_state = not desired_state
	print desired_state

	running = bool(db.get_last_ac_state()[3])
	print running
	while desired_state != running:
		time.sleep(1)
		running = bool(db.get_last_ac_state()[3])
	print "redirecting"
	return jsonify(running=running)

@app.route('/mode', methods=['POST'])
#set to home mode or away mode
def mode():
	global home_mode
	home_mode=bool(int(request.form['home_mode']))
	#print "home mode ="+str(home_mode)
	return redirect(url_for('homepage'))

@app.route('/set_temp', methods=['POST'])
#set the desired temperature for the air conditioner to achieve in the room
def set_temp():
	global desired_temp
	desired_temp = int(request.form['desired_temp'])
	print desired_temp
	return redirect(url_for('homepage'))

if __name__=="__main__":
	app.run('0.0.0.0',threaded=True)
