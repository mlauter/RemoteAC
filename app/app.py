from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.contrib.fixers import ProxyFix
from functools import wraps
import datetime
import time
import db
from collections import namedtuple

app = Flask(__name__, static_url_path='')
#initialize desired_state to a dictionary representing the off state
app.secret_key = ' \xd8\xf3yb\x80\xfc~y\xa7/\xed\x16VG,f\xf1\xc4\xb4\x14\xdfu\x08'

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

desired_state={'state_num':1,'goal_temp':''}

AcState = namedtuple('AcState', ['timestamp','room_temp','is_running', 'state_num','goal_temp'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'miriamlauter' or request.form['password'] != 'mysupersecretpassword':
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
#the route for the rpi to ping with latest state info (temp and on/off)
#returns desired state
def update():
    # have the ac respond with the state (which is given by the state_num 1, 2, or 3 and a goal temp, an empty string or an integer), whether it is running, and what the room temp is
    response = request.json
    
    room_temp = response['room_temp']
    is_running = response['is_running']
    state_num = response['state_num'] #1, 2, or 3
    goal_temp = str(response['goal_temp']) #an empty string or an integer
    #store temp as a string in the database because sometimes it's an empty string
    print room_temp
    print "I heard from the AC"
    db.add_ac_state(AcState(datetime.datetime.now(),room_temp,is_running,state_num,goal_temp))

    #return 
    global desired_state
    return jsonify(desired_state)

@app.route('/switch_state', methods=['GET','POST'])
@login_required
# the route the user POSTs to with desired state info
def switch_state():
    current_log = db.get_last_ac_state()
    current_state = (current_log[4], current_log[5])


    #if we have a post request, do this stuff, otherwise just populate the page with the latest database state
    if request.method == 'POST':
        print request.json
        global desired_state
        desired_state = statify(request.json)
        desired_state_tup = (desired_state['state_num'],desired_state['goal_temp'])
        #get latest state AC has reported from db
        #wait_time = 0
        # on heroku, only one worker, this will block

        # while desired_state_tup != current_state:
            # time.sleep(1)
        #    wait_time += 1
            # if wait_time > 20:
            #     print "the air conditioner did not respond"
            #     break
        #wait 4 seconds
        #time.sleep(4)
        current_log = db.get_last_ac_state()
        current_state = (current_log[4], current_log[5])

    #need to return stuff that the browser will then use
    return jsonify(is_running = current_log[3], state_num=current_state[0],goal_temp=current_state[1])

def statify(ui_state):
    #takes in inputs from the browser and returns an allowable state to give the AC. These states are in the form of dictionaries. state_num is an option 1, 2 or 3 corresponding to OFF, ON, and MANAGE_TEMpP and goal_temp is an empty string for ON (2) and OFF(1), but is the user's desired temperature input for MANAGE_TEMP (3). Returns a dictionary 
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
    app.run(threaded=True)
