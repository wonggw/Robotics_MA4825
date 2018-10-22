import tinyik
import itertools
import gesture_detection
import pypot.dynamixel
import numpy as np
import time

from camera_module import camera_thread

camera_thread = camera_thread()
camera_thread.start()

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

if not ports:
	raise IOError('No port available.')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO('/dev/ttyUSB0')
print('Connected!')
found_ids = dxl_io.scan([3,4,5])
print('Found ids:', found_ids)

arm = tinyik.Actuator([[0., -0.045, 0.],'y',[0., -0.04, 0.],'x', [0., -0.123, 0.], 'x', [0., -0.103, 0.]])
#arm.angles = [np.pi / 6, np.pi / 3]  # or np.deg2rad([30, 60])

#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})
for i in range(1000):
	dxl_io.set_moving_speed({found_ids[0]:150})
	dxl_io.set_goal_position({found_ids[0]: 0})
	dxl_io.set_moving_speed({found_ids[2]:150})
	dxl_io.set_goal_position({found_ids[2]: 0})
	dxl_io.set_moving_speed({found_ids[1]:150})
	dxl_io.set_goal_position({found_ids[1]: 0})
time.sleep(1)

while True:
	t1=time.time()
	img = camera_thread.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img)

	if coords:
		for coord in coords:
			x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord

			arm.ee = [(x_hand-320)/3200, (y_hand-240)/2400,z_hand/100]
			arm_deg=np.round(np.rad2deg(arm.angles))

			#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})
			for i in range(100):
				dxl_io.set_moving_speed({found_ids[0]:150})
				dxl_io.set_goal_position({found_ids[0]: arm_deg[0]})
				dxl_io.set_moving_speed({found_ids[2]:150})
				dxl_io.set_goal_position({found_ids[2]: arm_deg[1]})
				dxl_io.set_moving_speed({found_ids[1]:150})
				dxl_io.set_goal_position({found_ids[1]: arm_deg[2]})
			#time.sleep(1)


			print (arm.angles)
			print (arm_deg)
			print (arm.ee)
