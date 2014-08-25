import requests
import random
import signal
import sys
import time
from datetime import datetime, timedelta
import RPi.GPIO as io
import os
import glob
#import threading
#import Adafruit_DHT

#setup for the on-off pin
io.setmode(io.BCM)

switch_pin = 17

io.setup(switch_pin, io.OUT)
io.output(switch_pin, False)

#setup for the temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 

def is_running():
		#retrieves state of switch_pin
	return io.input(switch_pin)

def set_state(desired_state):
		#sets state of switch_pin to desired_state
	if desired_state:
		io.output(switch_pin, True)
	else:
		io.output(switch_pin, False)

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
	return temperature

def send_current_state():
		#threading.Timer(1,send_current_state).start()
	data_to_be_sent = {
		"temperature": current_temperature(),
		"is_running": is_running()
	}
	r = requests.post('http://10.0.5.236:5000/ac_status', data=data_to_be_sent, timeout=5)
	desired_state = r.json()['desired_state']
	desired_temp = r.json()['desired_temp']
	home_mode = r.json()['home_mode']

	### need to make this accomodate temp and home mode
	if desired_state != is_running():
		set_state(desired_state)

def signal_handler(signal, frame):
	cleanup()

def cleanup():
#   io.setup(switch_pin,io.OUT)
	#io.output(switch_pin, False)
	io.cleanup()
	sys.exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	io.setmode(io.BCM)
	switch_pin = 4
	io.setup(switch_pin, io.OUT)
	io.output(switch_pin, False)
	try:
		#last_connect=''
		while True:
			#print 'hello'
			time.sleep(1)
			try:
				print 'hello'
				pre_connect = datetime.now()
				send_current_state()
				print current_temperature()
				last_connect = datetime.now()
			except IOError:
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
		#print 'crap'
		cleanup()

