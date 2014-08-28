RemoteAC 
========
turning a dumb window air conditioner into a remote-controllable, programmable AC

## Dependencies
Server side:
* python 2.7
* Flask==0.10
* gunicorn==19.1.1

Raspberry Pi side:
* requests
* RPi.GPIO
Note: I haven't included these in the requirements.txt file, since you don't need them for the server. If you want to use my rpi code, download the ac_ping.py file and install requests and RPi.GPIO on your raspberry pi.

Hardware
--------
RemoteAC is created using a raspberry pi with this [souped up relay](http://www.adafruit.com/products/268) and a temperature sensor like [this](http://www.adafruit.com/products/381). 

Packages used on the pi
-------
On the pi, I'm using the requests library to post to the server, RPi.GPIO to interface with the pins, and using [Adafruit's tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software) for the temperature sensing.

Server
-------
The server uses Flask in python 2.7, and will soon be hosted on Heroku. I'm also using an sqlite3 database to store information about the temperature in my room over time. 

UI
------
HTML, jQuery and some CSS (bootstrap) 

If you're interested in turning your dumb window AC into a smart, awesome AC feel free to email me at lauter.miriam@gmail.com. 

