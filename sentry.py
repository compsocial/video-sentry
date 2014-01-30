#!/usr/bin/env python

import cv
import time
import numpy
import argparse
from math import *
from collections import deque
import sys, os, random, hashlib
from twilio.rest import TwilioRestClient

class Detector:
	def __init__(self, acct, token, f, t1, t2, s):
		
		self.twilio_acct = acct
		self.twilio_token = token
		self.fromnumber = f
		self.to1 = t1
		self.to2 = t2
		self.sensitivity = s

		fps=15
		is_color = True
		self.capture = cv.CaptureFromCAM(0)
		cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320);
		cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240);
		frame = cv.QueryFrame(self.capture)
		self.writer = None
		#self.writer = cv.CreateVideoWriter("test4.mpg", cv.CV_FOURCC('P', 'I', 'M', '1'), fps, (320, 240), is_color)

	def call(self, number):
		client = TwilioRestClient(self.twilio_acct, self.twilio_token)
		client.calls.create(to=number, from_=self.fromnumber, url="http://twimlets.com/message?Message%5B0%5D=Holy%20shit%20there%20is%20movement%20on%20your%20porch%20right%20now&")

	def text(self, number, text):
		client = TwilioRestClient(self.twilio_acct, self.twilio_token)
		client.messages.create(to=number, from_=self.fromnumber, body=text)

	def block_until_movement(self):
		print "monitoring video feed ... will let you know if something happens"
		frame = cv.QueryFrame(self.capture)
		display_image = cv.QueryFrame(self.capture)
		grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
		running_average_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
		running_average_in_display_color_depth = cv.CloneImage(display_image)
		difference = cv.CloneImage(display_image)
		last_diffs = deque()
		keep_diffs = 60
		frame_count = 0
		
		while True:
			frame_count += 1
			if frame_count % 15*100 == 0: print "..."
			camera_image = cv.QueryFrame(self.capture)
			display_image = cv.CloneImage(camera_image)
			color_image = cv.CloneImage(display_image)
			cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 19, 0)
			cv.RunningAvg(color_image, running_average_image, 0.320, None)
			cv.ConvertScale(running_average_image, running_average_in_display_color_depth, 1.0, 0.0)
			cv.AbsDiff(color_image, running_average_in_display_color_depth, difference)
			cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
			cv.Threshold(grey_image, grey_image, 2, 255, cv.CV_THRESH_BINARY)
			cv.Smooth(grey_image, grey_image, cv.CV_GAUSSIAN, 19, 0)
			cv.Threshold(grey_image, grey_image, 240, 255, cv.CV_THRESH_BINARY)
			grey_image_as_array = numpy.asarray(cv.GetMat(grey_image))
			last_diffs.append(log(numpy.sum(grey_image_as_array) + 1))
			if len(last_diffs) > keep_diffs: last_diffs.popleft()
			s = 0
			for d in last_diffs:
				if d > 15: s += 1	
			if s > keep_diffs*0.75*(1-self.sensitivity): return
	
	def run(self):
		self.block_until_movement()
		print "observed a large movement"
		self.call(self.to1)
		self.text(self.to1, "Just detected movement on your porch!")
		# self.call(self.to2)
		# self.text(self.to2, "Just detected movement on your porch!")

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Monitor a camera for a large movement, then do stuff about it.')
	parser.add_argument('--acct', help='twilio acct number', required=True)
	parser.add_argument('--token', help='twilio token', required=True)
	parser.add_argument('--fromnumber', help='twilio phone number from which to place call', required=True)
	parser.add_argument('--to1', help='first phone number to call & text in case of motion', required=True)
	parser.add_argument('--to2', help='second phone number to call & text in case of motion', required=True)
	parser.add_argument('--sensitivity', type=float, default=0, help='float from 0 to 1 controlling sensitivity of motion detection; 1 is super twitchy')
	args = parser.parse_args()
	d = Detector(args.acct, args.token, args.fromnumber, args.to1, args.to2, args.sensitivity)
	d.run()
