import itertools
import numpy
import time

import pypot.dynamixel

AMP = 30
FREQ = 0.5

ports = pypot.dynamixel.get_available_ports()

if not ports:
	raise IOError('no port found!')

print('ports found', ports)

print('connecting on the first available port:', ports[0])
dxl_io = pypot.dynamixel.DxlIO(ports[0])

servos_ids = dxl_io.scan([2])
print ('servos_ids:',servos_ids)

servos_pos =dxl_io.get_present_position((2, ))
print ('servos position:',servos_pos)


speed = dict(zip(servos_ids, itertools.repeat(200))) #value from 0 to 1023
dxl_io.set_moving_speed(speed)
pos = dict(zip(servos_ids, itertools.repeat(0))) #value from -150 to 150
dxl_io.set_goal_position(pos)

led = dxl_io.switch_led_off(servos_ids) #switch on led
print (led)

t0 = time.time()
while True:
	t = time.time()
	if (t - t0) > 5:
		break

	pos = AMP * numpy.sin(2 * numpy.pi * FREQ * t)
	dxl_io.set_goal_position(dict(zip(servos_ids, itertools.repeat(pos))))
	pid=dxl_io.get_pid_gain(servos_ids)
	print (pid)

#	time.sleep(0.02)
