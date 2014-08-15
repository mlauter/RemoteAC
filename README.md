RemoteAC - a web app for turning my dumb window air conditioner into a remote-controllable, programmable AC
========

## Dependencies
* Flask
* time
* datetime
* sqlite3

## Introduction

The internet of things comes to my apartment! I've set up the AC to be connected to my raspberry pi via this [souped up relay](http://www.adafruit.com/products/268). I also have a temperature sensor like [this](http://www.adafruit.com/products/381) connected. The pi runs a script, see my [gist](https://gist.github.com/mlauter/ab1ab393eabaaf0c6c2b) and posts to the server every second. 

The flask server responds to the post request with data set by the user in the browser. This server also displays the UI, using some javascript with jQuery for the buttons and input fields. I'm currently playing around with some css to make it look better. 

If you're interested in turning your dumb window AC into a smart, awesome AC feel free to email me at lauter.miriam@gmail.com. 

Note, this project is still under development.
