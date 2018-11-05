import cv2 
import threading
import time 
import os


class camera_thread(threading.Thread):
	def __init__(self):
		self.http = 'http://'
		self.ip_address = '10.27.67.27' #10.27.79.85
		self.url =  self.http + self.ip_address + ':4747/mjpegfeed?1024x768'
		self.cap = cv2.VideoCapture(self.url)
		_,self.img = self.cap.read()
		threading.Thread.__init__(self)

	def run(self):
		while True:
			time.sleep(0.03)
			try:
				_,self.img = self.cap.read()
			except:
				pass

	def read(self):
		return self.img 

class camera_thread_1(threading.Thread):
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		_,self.img = self.cap.read()
		threading.Thread.__init__(self)

	def run(self):
		while True:
			time.sleep(0.03)
			try:
				_,self.img = self.cap.read()
			except:
				pass

	def read(self):
		return self.img 
