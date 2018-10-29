import tinyik
import time
import itertools
import gesture_detection
import pypot.dynamixel

import tinyik
import numpy as np

from camera_module import camera_thread,camera_thread_1

camera_thread = camera_thread()
camera_thread.start()

camera_thread_1 = camera_thread_1()
camera_thread_1.start()

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

if not ports:
	raise IOError('No port available.')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO('/dev/ttyUSB0')
print('Connected!')
servos_ids = dxl_io.scan([1,2,3,4,5,6])
print('Found ids:', servos_ids)

arm = tinyik.Actuator([[0., -0.055, -0.11],'y',[0., -0.04, 0.],'x', [0., -0.123, 0.], 'x', [0., -0.103, 0.]])

dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(150))))
dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(150))))
dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(-45))))
dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(150))))
dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-30))))
time.sleep(1)


arm_counter =0

while True:
	t1=time.time()
	img = camera_thread.read()
	img_1 = camera_thread_1.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img,"handphone")
	coords_1 = gesture_detection.get_coord_from_detection(img_1,"webcam")

	if coords:
		lefthand_0 =False
		lefthand_1 =False
		lefthand_2 =False
		righthand_0=False
		righthand_1=False
		righthand_2=False

		for coord in coords:
			x_hand,y_hand,w_hand,h_hand,_,cat_hand = coord

			if x_hand>=(img_width/2):
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

		if lefthand_0 ==True:
			dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(200))))
		elif lefthand_1 ==True:
			dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(-200))))
		else:
			dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(0))))

		if righthand_0 ==True:
			dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(-200))))
		elif righthand_1 ==True:
			dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(200))))
		else:
			dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(0))))

		if lefthand_2 ==True and righthand_2 ==True:
			print ("cut")
		else:
			pass

	else:
		dxl_io.set_moving_speed({1: 0,2: 0})

	if coords_1:
		for coord_1 in coords_1:
			x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord_1
			x_real=z_hand*(x_hand-320)/373.3
			y_real=z_hand*(y_hand-240)/373.3
			#print("a",x_real,y_real,z_hand,w_hand,h_hand)
			arm.ee = [x_real, y_real,z_hand]
			arm_deg=np.round(np.rad2deg(arm.angles))

			dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(150))))
			dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(-arm_deg[0]))))
			dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(150))))
			dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(arm_deg[1]))))
			dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(150))))
			dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(arm_deg[2]))))

			#print (arm.angles)
			#print (arm_deg)
			#print (arm.ee)

	if arm_counter >=30:
		dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(150))))
		dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
		dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(150))))
		dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(-45))))
		dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(150))))
		dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-30))))
		arm_counter =0

	arm_counter +=1
	#print(arm_counter)

