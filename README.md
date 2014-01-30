This is a python script that uses [OpenCV](http://opencv.org) to monitor a video feed for
large movements (big changes in the current frame relative to last n
frames), and then calls/texts you. I am using it to monitor the places
around my house (e.g., my porch) people may visit at 3am with less than
honorable intentions. Soon, I will be voicing my displeasure to them via
a wireless bluetooth speaker. But that is for a future commit.

## Installation

Install the two major dependencies:
	
	pip install cv
	pip install numpy

Then, download the sentry.py script to the directory of your choosing.

## Usage

```bash
./sentry.py yada yada
```
