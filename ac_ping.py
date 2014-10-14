import requests
import random
import signal
import sys
import time
from datetime import datetime, timedelta
import RPi.GPIO as io
import os
import glob
import json

def send_current_state():
    data_to_be_sent = {
        "is_running": is_running(),
        "room_temp": current_temperature(),
        "state_num": state['state_num'], #get the current global state
        "goal_temp": state['goal_temp']
    }
    url = "your.url.here/your_route"
    #for testing server running on your computer's local host, url = 'your.ip.address/your_route'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    #make POST request with current state and temp information
    r = requests.post(url, data=json.dumps(data_to_be_sent), headers=headers, timeout=5)

    #retrieve response from server
    state_num = r.json()['state_num']
    goal_temp = r.json()['goal_temp']

    #for debugging:
    # print state_num
    # print goal_temp

    #in this function, modify the state of the air conditioner to meet user request and update global state
    set_state(state_num,goal_temp) 
    
def set_state(state_num, goal_temp):
    """Takes in a desired state from the server, represented by a state number and possibly a desired temperature, determines whether the output pin should be set HIGH or LOW (AC on or off), and sets the global state variable to reflect the new current state"""

    room_temp = current_temperature()

    # State-handling logic
    # If we have the purely "OFF" state, set pin LOW
    if state_num == 1:
        io.output(switch_pin, False)
        goal_temp = ''

    # If we have the purely "ON" state, set pin HIGH
    elif state_num == 2:
        io.output(switch_pin, True)
        goal_temp = ''

    # Thermostat mode
    else:
        #this is the thermostat mode where we try to achieve a goal temp
        #this does not perform very well at the edges of the temp range (turns off and on a lot)
        #could definitely be improved
        
        # print "home_mode" #for debugging

        goal_temp_range_max = int(goal_temp) + 2 # don't get warmer than 2 degrees above temp that user asked for

        if room_temp > goal_temp_range_max:
            # if we're hotter than max, turn on
            io.output(switch_pin, True)
        elif room_temp <= goal_temp:
            # if we're at or under the temp range turn off
            io.output(switch_pin, False)
        #otherwise no change

    #set the global state
    state['state_num'] = state_num
    state['goal_temp'] = goal_temp

def is_running():
    """retrieves state of switch_pin"""
    return io.input(switch_pin)

def read_temp_raw():
    """reads raw temp info from the sensor"""
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    """return processed temp info in degrees F"""
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def current_temperature():
    """get the current temperature in the room"""
    temperature = read_temp()[1]
    return int(temperature)

def signal_handler(signal, frame):
    cleanup()

def cleanup():
    """clean up the pins (sets output to LOW so AC turns off)"""
    io.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    #set signal handler to catch interruptions and turn ac off
    signal.signal(signal.SIGINT, signal_handler)

    #setup for switch pins
    io.setmode(io.BCM)
    switch_pin = 17
    io.setup(switch_pin, io.OUT)
    io.output(switch_pin, False)

    #setup for the temperature sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')
    device_file = device_folder[0] + '/w1_slave'

    #initialize global state with off
    state={'state_num':1,'goal_temp':''}

    #initialize last connection time
    last_connect = None

    #main loop, try to connect to server every second
    try:
        while True:
            time.sleep(1)
            try:
                pre_connect = datetime.now()
                send_current_state()
                last_connect = datetime.now()

            # if the server is down and we fail to connect, keep trying for five minutes, then shut the AC off, and continue trying to connect
            except IOError as e:
                print e
                t_delt = timedelta(minutes=5)
                if last_connect:
                    if datetime.now()>(last_connect+t_delt):
                        io.output(switch_pin,False)
                else:
                    if datetime.now()>(pre_connect+t_delt):
                        io.output(switch_pin,False)

    # for all other expections, print out the error, but cleanup before quitting 
    except Exception as e:
        print e
    finally:
        cleanup()

