import gesture_detection
import time
import itertools
import pypot.dynamixel

from camera_module import camera_thread

camera_thread = camera_thread()
camera_thread.start()

ports = pypot.dynamixel.get_available_ports()


dxl_io = pypot.dynamixel.DxlIO('/dev/ttyUSB0')
servos_ids = dxl_io.scan([1,2])
print (ports)
#time.sleep(1)

while True:
	t1=time.time()
	img = camera_thread.read()
	img_height,img_width,_=img.shape
	coords = gesture_detection.get_coord_from_detection(img)
	while True:
		try:
			if coords:
				lefthand_0 =False
				lefthand_1 =False
				righthand_0=False
				righthand_1=False
				for coord in coords:
					x_hand,y_hand,w_hand,h_hand,z_hand,cat_hand = coord

					if x_hand<=(img_width/2):
						if cat_hand ==0:
							lefthand_0 = True
							lefthand_1 = False
						elif cat_hand ==1:
							lefthand_0 = False
							lefthand_1 = True
					else:
						if cat_hand ==1:
							righthand_0 = True
							righthand_1 = False
						elif cat_hand ==0:
							righthand_0 = False
							righthand_1 = True

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
			break
		except:
			break
	#print t2-t1

