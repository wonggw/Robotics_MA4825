import tinyik
import itertools
import gesture_detection
import pypot.dynamixel
import numpy as np
import time

from camera_module import camera_thread_1

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
motor_ids = dxl_io.scan([3,4,5])
print('Found ids:', motor_ids)

arm = tinyik.Actuator([[0.0, -0.055, -0.115],'y',[0., -0.046, 0.],'x', [0., -0.2, 0.], 'x', [0., -0.18, 0.05]])
#arm.angles = [np.pi / 6, np.pi / 3]  # or np.deg2rad([30, 60])

#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})

dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(-45))))
dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(50))))
dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-40))))
time.sleep(1)


arm_counter =0

while True:
	t1=time.time()
	img = camera_thread_1.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img)

	if coords:
		for coord in coords:
			x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord
			print (x_hand-320,y_hand-240,z_hand)
			if cat_hand==1:
				x_real=z_hand*(x_hand-320)/375
				y_real=z_hand*(y_hand-240)/375
				#print("a",x_real,y_real,z_hand,w_hand,h_hand)
				arm.ee = [x_real, y_real,z_hand]
				arm_deg=np.round(np.rad2deg(arm.angles))
				arm_deg[1]=np.maximum(arm_deg[1],-90)
				#arm_deg[2]=np.maximum(arm_deg[2],150)
				#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})

#				dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(50))))
#				dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(-arm_deg[0]))))
#				dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(50))))
#				dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(arm_deg[1]))))
#				dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(50))))
#				dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(arm_deg[2]))))

				#print (arm.angles)
				#print (arm_deg)
				#print (arm.ee)

	if arm_counter >=30:
#		dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(50))))
#		dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
#		dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(50))))
#		dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(-45))))
#		dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(50))))
#		dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(-40))))
		arm_counter =0

	arm_counter +=1
	#print(arm_counter)
