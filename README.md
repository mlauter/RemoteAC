RemoteAC 
========
turning a dumb window air conditioner into a remote-controllable, programmable AC

## Dependencies
* Flask
* time
* datetime
* sqlite3
* requests
* RPi.GPIO
* gunicorn

Hardware
--------
RemoteAC is created using a raspberry pi with this [souped up relay](http://www.adafruit.com/products/268) and a temperature sensor like [this](http://www.adafruit.com/products/381). 

Packages used on the pi
-------
On the pi, I'm using the requests library to post to the server, RPi.GPIO to interface with the pins, and using [Adafruit's tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software) for the temperature sensing.

Server
-------
The server uses Flask, python, and will soon be hosted on Heroku. I'm also using an sqlite3 database to store information about the temperature in my room over time. Soon, this will be displayed in the browser.

UI
------
I've used some javascript with jQuery for the buttons and input fields. I'm currently playing around with css Bootstrap to make it look better. 

If you're interested in turning your dumb window AC into a smart, awesome AC feel free to email me at lauter.miriam@gmail.com. 

Note, this project is still under development.
