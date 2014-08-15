import requests
import random
import signal
import sys
import time
from datetime import datetime, timedelta
import RPi.GPIO as io
io.setmode(io.BCM)

switch_pin = 4

io.setup(switch_pin, io.OUT)
io.output(switch_pin, False)

def is_running():
		#retrieves state of switch_pin
	return io.input(switch_pin)

def set_state(desired_state):
		#sets state of switch_pin to desired_state
	if desired_state:
		io.output(switch_pin, True)
	else:
		io.output(switch_pin, False)

def current_temperature():
		""" Should be replaced with an implementation that
				retrieves it from the sensor """
	return random.randint(60, 80)

def send_current_state():
		#threading.Timer(1,send_current_state).start()
	data_to_be_sent = {
		"temperature": current_temperature(),
		"is_running": is_running()
	}
	r = requests.post('http://10.0.6.84:5000/ac_status', data=data_to_be_sent, timeout=5)
	desired_state = r.json()['desired_state']
	desired_temp = r.json()['desired_temp']
	home_mode = r.json()['home_mode']
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
		while True:
			#print 'hello'
			time.sleep(1)
			try:
				send_current_state()
				last_connect = datetime.now()
			except IOError:
				t_delt = timedelta(minutes=5)
				if datetime.now()>(last_connect+t_delt):
					io.output(switch_pin,False) 
	except Exception as e:
		print e
	finally:
		#print 'crap'
		cleanup()

