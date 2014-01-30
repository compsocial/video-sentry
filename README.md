This is a python script that uses [OpenCV](http://opencv.org) to monitor a video feed for
large movements (big changes in the current frame relative to the last n
frames), and then calls/texts you about it. I am using it to monitor the places
around my house (e.g., my porch) people may visit at 3am with less than
honorable intentions. Soon, I will be voicing my displeasure to them via
a wireless bluetooth speaker. But that is for a future commit.

## Installation

Install the two major dependencies:
	
	brew install opencv # assuming on a mac, with details omitted
	pip install numpy

I found [this guide](http://www.jeffreythompson.org/blog/2013/08/22/update-installing-opencv-on-mac-mountain-lion) particularly helpful for setting up OpenCV and its Python bridge in OS X. YMMV. Then, download the above `sentry.py` script to the directory of your choosing.

## Usage

First, point the camera at whatever you want to monitor. Lighting that
area up as best as you can will help (in addition to likely making it
less attractive to rob ;) Once in place, run ``sentry.py.`` It takes a
number of options.


```bash
$ ./sentry.py --help
usage: sentry.py [-h] --acct ACCT --token TOKEN --fromnumber FROMNUMBER --to1
                 TO1 --to2 TO2 [--sensitivity SENSITIVITY]

Monitor a camera for a large movement, then do stuff about it.

optional arguments:
  -h, --help            show this help message and exit
  --acct ACCT           twilio acct number
  --token TOKEN         twilio token
  --fromnumber FROMNUMBER
                        twilio phone number from which to place call
  --to1 TO1             first phone number to call & text in case of motion
  --to2 TO2             second phone number to call & text in case of motion
  --sensitivity SENSITIVITY
                        float from 0 to 1 controlling sensitivity of motion
                        detection; 1 is super twitchy
```

The ``acct`` and ``token`` options refer to [your Twilio credentials](https://www.twilio.com/user/account). The ``from`` number is the Twilio-provisioned phone number from which you would like to call and text. The two options, ``to1`` and ``to2`` will receive the calls and texts. ``sensitivity`` lets you to control how twitchy the motion detection is; the defaults are pretty sensible.

## Credits

I borrowed heavily from [Derek Simkowiak's work](http://derek.simkowiak.net/motion-tracking-with-python/). You should check it out, it's great stuff. Thanks for making it available, Derek!
