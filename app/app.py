from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.contrib.fixers import ProxyFix
from functools import wraps
import datetime
import time
import db
from collections import namedtuple
import os

app = Flask(__name__, static_url_path='')

#Generate something secret! (import os, os.urandom(24))
app.secret_key = os.environ["SECRET_KEY"]

#initialize desired_state to a dictionary representing the off state
desired_state={'state_num':1,'goal_temp':''}

AcState = namedtuple('AcState', ['timestamp','room_temp','is_running', 'state_num','goal_temp'])

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # create your own username and password
        if request.form['username'] != os.environ["USERNAME"] or request.form['password'] != os.environ["PASSWORD"]:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash("You are now logged in!")
            return redirect(url_for('homepage'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    # flash("You have logged out!")
    return redirect(url_for('homepage'))

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@login_required
#the homepage route, reads latest entry from database and renders index.html
def homepage():
    current_log = db.get_last_ac_state()
    room_temp = current_log[2]
    is_running = bool(current_log[3])
    return render_template('index.html', room_temp = room_temp, is_running = is_running, time=datetime.datetime.now())

@app.route('/ac_status', methods=['POST'])
#The route for the rpi to ping with latest state info
def update():
    """Receive information from the Raspberry Pi about the air conditioner's state and add to the database. Respond to the Pi with the current desired state as set by the user."""

    response = request.json
    room_temp = response['room_temp']
    is_running = response['is_running']
    state_num = response['state_num'] #1, 2, or 3
    goal_temp = str(response['goal_temp']) #an empty string or an integer
    
    # print room_temp #for debugging

    # add information received from the Raspberry Pi to the database
    db.add_ac_state(AcState(datetime.datetime.now(),room_temp,is_running,state_num,goal_temp))

    #return 
    global desired_state
    return jsonify(desired_state)

@app.route('/switch_state', methods=['GET','POST'])
@login_required
# the route the user (browser) POSTs to with desired state
def switch_state():
    """Set new desired state based on user input and return the current state of the air conditioner (newest database entry) to the browser"""

    # set new desired state
    if request.method == 'POST':
        global desired_state
        desired_state = statify(request.json)
        desired_state_tup = (desired_state['state_num'],
                             desired_state['goal_temp'])

    # get current AC state
    current_log = db.get_last_ac_state()
    current_state = (current_log[4], current_log[5])

    # return current state to browser
    return jsonify(is_running = current_log[3], state_num=current_state[0],goal_temp=current_state[1])

def statify(ui_state):
    """Takes in inputs from the browser and returns an allowable state to give the AC. These states are in the form of dictionaries. state_num is an option 1, 2 or 3 corresponding to OFF, ON, and MANAGE_TEMP and goal_temp is an empty string for ON (2) and OFF(1), but is the user's desired temperature input for MANAGE_TEMP (3). Returns a dictionary."""
    
    allowed_states = {'OFF':{'state_num':1,'goal_temp':''},
                      'ON':{'state_num':2,'goal_temp':''},
                      'MANAGE_TEMP':{'state_num':3,
                                     'goal_temp':str(ui_state['desired_temp'])}}
    cleaned_state = {}
    if ui_state['desired_power_state'] == False:
        cleaned_state=allowed_states['OFF']
    elif ui_state['desired_mode_is_home']:
        cleaned_state=allowed_states['MANAGE_TEMP']
    else:
        cleaned_state=allowed_states['ON']
    return cleaned_state


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__=="__main__":
    app.run() #to run with the debuger app.run(debug=True)
    #to test with raspberry pi communication on localhost app.run('0.0.0.0')
