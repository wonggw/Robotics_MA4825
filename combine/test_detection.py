import gesture_detection
import time
import cv2
from camera_module import camera_thread#,camera_thread_1

camera_thread = camera_thread()
camera_thread.start()

#camera_thread_1 = camera_thread_1()
#camera_thread_1.start()


while True:
	t1=time.time()
	img = camera_thread.read()
	#img_1 = camera_thread_1.read()
	#cv2.imshow('webcam',img_1)
	#cv2.waitKey(1)
	coords = gesture_detection.get_coord_from_detection(img,"handphone")
	#coords_1 = gesture_detection.get_coord_from_detection(img_1,"webcam")
	#print (coords)
	t2=time.time()
	print (t2-t1)
