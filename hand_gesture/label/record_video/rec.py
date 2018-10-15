import cv2 

def hist_equal(img):
	equ = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	equ[:,:,2] = cv2.equalizeHist(equ[:,:,2])
	equ = cv2.cvtColor(equ, cv2.COLOR_HSV2BGR)
	return equ

http = 'http://'
ip_address = '10.27.173.250'
url =  http + ip_address + ':4747/mjpegfeed?1024x768'

cap = cv2.VideoCapture(url)

MAX_FRAME = 50000
FRAME_SKIP = 3
j = -10

for i in range(MAX_FRAME):
	if i <= 0:
		continue
	_,img = cap.read()
	cv2.imshow('output',img)
	cv2.waitKey(1)
	#img = hist_equal(img)
	if i % FRAME_SKIP != 1:
		j+=1
		cv2.imwrite('./imgs_7/%d.png'%j,img) 
