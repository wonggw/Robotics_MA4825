import tinyik
import itertools
import pypot.dynamixel
import numpy as np
import time

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

if not ports:
	raise IOError('No port available.')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO('/dev/ttyUSB0')
print('Connected!')
found_ids = dxl_io.scan([2,3,4,5,6])
print('Found ids:', found_ids)

arm = tinyik.Actuator([[0., -0.045, 0.],'y',[0., -0.04, 0.],'x', [0., -0.123, 0.], 'x', [0., -0.103, 0.]])
#arm.angles = [np.pi / 6, np.pi / 3]  # or np.deg2rad([30, 60])
arm.ee = [0.0, -0.3,-0.1]
arm_deg=np.round(np.rad2deg(arm.angles))

#dxl_io.set_goal_position({found_ids[0]: 0,found_ids[2]: 0,found_ids[1]: 0})
#dxl_io.set_moving_speed(dict(zip((3,), itertools.repeat(120))))
#dxl_io.set_goal_position(dict(zip((3,), itertools.repeat(0))))
#dxl_io.set_moving_speed(dict(zip((5,), itertools.repeat(120))))
#dxl_io.set_goal_position(dict(zip((5,), itertools.repeat(0))))
#dxl_io.set_moving_speed(dict(zip((4,), itertools.repeat(120))))
#dxl_io.set_goal_position(dict(zip((4,), itertools.repeat(0))))
#dxl_io.set_moving_speed(dict(zip((6,), itertools.repeat(150))))
#dxl_io.set_goal_position(dict(zip((6,), itertools.repeat(80))))
dxl_io.set_moving_speed(dict(zip((2,), itertools.repeat(-500))))
time.sleep(1)


print (arm.angles)
print (arm_deg)
print (arm.ee)
