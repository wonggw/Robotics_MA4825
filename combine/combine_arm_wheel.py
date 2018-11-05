import tinyik
import time
import itertools
import gesture_detection
import pypot.dynamixel

import tinyik
import numpy as np

from user_input import input_thread
from camera_module import camera_thread,camera_thread_1

import sys, select, termios, tty

settings = termios.tcgetattr(sys.stdin)
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

input_thread = input_thread()
input_thread.start()

camera_thread = camera_thread()
camera_thread.start()

camera_thread_1 = camera_thread_1()
camera_thread_1.start()

def getKey():
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


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

arm = tinyik.Actuator([[0.0, -0.055, -0.065],'y',[0., -0.046, 0.],'x', [0., -0.2, 0.], 'x', [0.04, -0.17, 0.04]])

dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(-45))))
dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-40))))
time.sleep(1)

arm_counter =0
cut_status =0
while True:
	t1=time.time()
	cut_status=input_thread.status()
	img = camera_thread.read()
	img_1 = camera_thread_1.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img,"handphone")
	coords_1 = gesture_detection.get_coord_from_detection(img_1,"webcam")

#	key=getKey()
#	if key =='w':
#		dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(-400))))
#		dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(400))))
#		print("Forward")
#	if key =='s':
#		dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(400))))
#		dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(-400))))
#		print("Reverse")
#	if key =='a':
#		dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(400))))
#		dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(400))))
#		print("Left")
#	if key =='d':
#		dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(-400))))
#		dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(-400))))
#		print("Right")
#	if key =='v':
#		cut_status =1
#	elif key !='v' and cut_status==1:
#		cut_status =0
#		dxl_io.set_moving_speed(dict(zip((6,), itertools.repeat(150))))
#		dxl_io.set_goal_position(dict(zip((6,), itertools.repeat(40))))
#		print("Releasing")
#	if key =='c':
#		cut_status =2
#	elif key !='c' and cut_status==2:
#		cut_status =0
#		dxl_io.set_moving_speed(dict(zip((6,), itertools.repeat(150))))
#		dxl_io.set_goal_position(dict(zip((6,), itertools.repeat(80))))
#		print("Cutting")
#	if key =='1':
#		break

	if coords:
		lefthand_0 =False
		righthand_0=False

		for coord in coords:
			x_hand,y_hand,w_hand,h_hand,_,cat_hand = coord

			if x_hand>=(img_width/2):
				if cat_hand ==0:
					lefthand_0 = True

			else:
				if cat_hand ==0:
					righthand_0 = True


		if lefthand_0 ==True:
			dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(200))))
		else:
			dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(0))))

		if righthand_0 ==True:
			dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(-200))))
		else:
			dxl_io.set_moving_speed(dict(zip((1,), itertools.repeat(0))))


	else:
		dxl_io.set_moving_speed({1: 0,2: 0})

	if coords_1:
		for coord_1 in coords_1:
			x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord_1
			if cat_hand ==1:
				x_real=z_hand*(x_hand-320)/375
				y_real=z_hand*(y_hand-240)/375
				#print (y_real)
				#print("a",x_real,y_real,z_hand,w_hand,h_hand)
				arm.ee = [x_real, y_real,z_hand]
				arm_deg=np.round(np.rad2deg(arm.angles))
				arm_deg[1]=np.maximum(arm_deg[1],-80)
				#arm_deg[2]=np.maximum(arm_deg[2],150)
				#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})

				dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(30))))
				dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(-arm_deg[0]))))
				dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(30))))
				dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(arm_deg[1]))))
				dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(30))))
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
		dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-40))))
		arm_counter =0

	if cut_status !=0:
		if cut_status ==1:
			dxl_io.set_moving_speed(dict(zip((6,), itertools.repeat(150))))
			dxl_io.set_goal_position(dict(zip((6,), itertools.repeat(40))))
			print("Releasing")
		elif cut_status ==2:
			dxl_io.set_moving_speed(dict(zip((6,), itertools.repeat(150))))
			dxl_io.set_goal_position(dict(zip((6,), itertools.repeat(85))))
			print("Cutting")
	arm_counter +=1
	#print(arm_counter)

