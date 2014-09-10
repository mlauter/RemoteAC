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


def is_running():
        #retrieves state of switch_pin
    return io.input(switch_pin)

def set_state(state_num, goal_temp):
    #sets state of switch_pin appropriately and update global state
    room_temp = current_temperature()

    if state_num == 1:
        io.output(switch_pin, False)
        goal_temp = ''
    elif state_num == 2:
        io.output(switch_pin, True)
        goal_temp = ''
    else:
        print "home_mode"
        #this is the thermostat mode where we try to achieve a goal temp
        #this does not perform very well at the edges of the temp range (turns off and on a lot)
        #could definitely be improved
        goal_temp_range_max = int(goal_temp) + 2 # don't get warmer than 2 degrees above what user asked for
        if room_temp >= goal_temp_range_max:
            # if we're at the max of temp range or hotter, turn on
            io.output(switch_pin, True)
        elif room_temp < goal_temp:
            # if we're under the temp range turn off
            io.output(switch_pin, False)
        #otherwise just keep doing what you're doing

    #set the global state
    state['state_num'] = state_num
    state['goal_temp'] = goal_temp

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
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
    temperature = read_temp()[1]
    return int(temperature)

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
    r = requests.post(url, data=json.dumps(data_to_be_sent), headers=headers, timeout=5)

    state_num = r.json()['state_num']
    goal_temp = r.json()['goal_temp']
    print state_num
    print goal_temp
    set_state(state_num,goal_temp) #in this function, modify the state of the air conditioner to meet user request and update global state
    

def signal_handler(signal, frame):
    cleanup()

def cleanup():
    io.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
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
    #initialize global state with off, this is the AC's introspection, what it knows it's state to be
    state={'state_num':1,'goal_temp':''}
    last_connect = None
    try:
        while True:
            time.sleep(1)
            try:
                pre_connect = datetime.now()
                send_current_state()
                last_connect = datetime.now()
            except IOError as e:
                print e
                t_delt = timedelta(minutes=5)
                if last_connect:
                    if datetime.now()>(last_connect+t_delt):
                        io.output(switch_pin,False)
                else:
                    if datetime.now()>(pre_connect+t_delt):
                        io.output(switch_pin,False) 
    except Exception as e:
        print e
    finally:
        cleanup()

