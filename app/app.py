from flask import Flask, render_template, request
import datetime

app = Flask(__name__)
ac_states = []

from collections import namedtuple
AcState = namedtuple('AcState', ['timestamp','temp','is_running'])

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def homepage():
	return render_template('index.html', temp = ac_states[-1].temp, running = ac_states[-1].is_running, time=datetime.datetime.now())

@app.route('/ac_status', methods=['POST'])
def temp_update():
	temp = float(request.form['temperature'])
	is_running = bool(int(request.form['is_running']))
	ac_states.append(AcState(datetime.datetime.now(),temp,is_running))
	print ac_states
	return ''

if __name__=="__main__":
	app.run(debug=True)
