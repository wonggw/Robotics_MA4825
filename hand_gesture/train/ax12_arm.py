import gesture_detection
import time
import itertools
import pypot.dynamixel

import tinyik
import numpy as np

from camera_module import camera_thread

camera_thread = camera_thread()
camera_thread.start()

ports = pypot.dynamixel.get_available_ports()


dxl_io = pypot.dynamixel.DxlIO('/dev/ttyUSB0')
servos_ids = dxl_io.scan([1,2])
print (ports)
#time.sleep(1)
arm = tinyik.Actuator(['y', [0., -0.01, 0.], 'x', [0., -0.15, 0.], 'x', [0., -0.15, 0.]])

while True:
	t1=time.time()
	img = camera_thread.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img)

	if coords:
		lefthand_0 =False
		lefthand_1 =False
		lefthand_2 =False
		righthand_0=False
		righthand_1=False
		righthand_2=False

		for coord in coords:
			x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord

			if x_hand<=(img_width/2):
				if cat_hand ==0:
					lefthand_0 = True
					lefthand_1 = False
					lefthand_2 = False
				elif cat_hand ==1:
					lefthand_0 = False
					lefthand_1 = True
					lefthand_2 = False
				elif cat_hand ==2:
					lefthand_0 = False
					lefthand_1 = False
					lefthand_2 = True
			else:
				if cat_hand ==0:
					righthand_0 = True
					righthand_1 = False
					righthand_2 = False
				elif cat_hand ==1:
					righthand_0 = False
					righthand_1 = True
					righthand_2 = False
				elif cat_hand ==2:
					righthand_0 = False
					righthand_1 = False
					righthand_2 = True

			if cat_hand == 3: #detect bomb
				arm.ee = [x_hand, y_hand, z_hand]
				arm_deg=np.round(np.rad2deg(arm.angles))
				dxl_io.set_goal_position({4: arm_deg[0],5: arm_deg[1],6: arm_deg[2]})

		if lefthand_0 ==True:
			dxl_io.set_moving_speed({1: 1023})
		elif lefthand_1 ==True:
			dxl_io.set_moving_speed({1: -1023})
		else:
			dxl_io.set_moving_speed({1: 0})

		if righthand_0 ==True:
			dxl_io.set_moving_speed({2: 1023})
		elif righthand_1 ==True:
			dxl_io.set_moving_speed({2: -1023})
		else:
			dxl_io.set_moving_speed({2: 0})

	else:
		dxl_io.set_moving_speed({1: 0,2: 0})
	#print coords

	#print t2-t1

