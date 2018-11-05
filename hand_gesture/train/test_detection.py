import gesture_detection
import time

from user_input import input_thread
from camera_module import camera_thread#,camera_thread_1


input_thread = input_thread()
input_thread.start()

camera_thread = camera_thread()
camera_thread.start()

#camera_thread_1 = camera_thread_1()
#camera_thread_1.start()


while True:
	t1=time.time()
	cut_status=input_thread.status()
	img = camera_thread.read()
	#img_1 = camera_thread_1.read()
	coords =gesture_detection.get_coord_from_detection(img,"handphone")
	#coords_1 =gesture_detection.get_coord_from_detection(img_1,"webcam")
	if cut_status !=0:
		if cut_status ==1:
			print("Releasing")
		elif cut_status ==2:
			print("Cutting")

	#print(coords)
	#print (coords)
	t2=time.time()
	print (t2-t1)
