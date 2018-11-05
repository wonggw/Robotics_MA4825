import cv2 
import numpy as np 
import random

class reader():

	def __init__(self,height=480,width=640,scale_range=[0.7,1.2]):
		# set class params
		self.height = height
		self.width = width
		self.scale_range = scale_range
		print('Loading images...')
		self.data = []

		f = open('drive/Colab/hand_gesture/annotation_c.txt')
		counter = 0
		for i in f:
			i = i.strip().split('\t')
			# split the line, get the filename and coordinates 
			fname = i[0]
			coord = i[1:]
			coord = [float(x) for x in coord]
			# split the coordinates 
			x = coord[0::5]
			y = coord[1::5]
			w = coord[2::5]
			h = coord[3::5]
			category = coord[4::5]
			# combine the coordinates 
			coord = list(zip(x,y,w,h,category))
			if len(coord)!=0:
				# write into data list
				# print(fname)
				img = cv2.imread(fname)
#				random_int=np.random.randint(2)
#				if random_int==0:
#					equ= cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
#					equ[:,:,1] = cv2.equalizeHist(equ[:,:,1])
#					img = cv2.cvtColor(equ, cv2.COLOR_HLS2BGR)
				if not img is None:
					self.data.append([img,coord])
				else:
					print(fname)

			counter+=1
			print counter
		print('Finish reading. Total valid data:',len(self.data))

	def random_crop(self,img,annot):
		# right btm corner
		x2s = [i[0] for i in annot]
		y2s = [i[1] for i in annot]
		# left top corner
		x1s = [i[0]-i[2] for i in annot]
		y1s = [i[1]-i[3] for i in annot]
		# get the shift range
		xmin = np.max(np.array(x2s)) - self.width
		xmax = np.min(np.array(x1s))
		ymin = np.max(np.array(y2s)) - self.height
		ymax = np.min(np.array(y1s))
		# get transform value
		x_trans = random.random()*(xmax-xmin) + xmin
		y_trans = random.random()*(ymax-ymin) + ymin
		# get transformation matrix and do transform
		# print(xmin,xmax)
		M = np.float32([[1,0,-x_trans],[0,1,-y_trans]])
		img_result = img.copy()
		img_result = cv2.warpAffine(img_result,M,(self.width,self.height))
		# substract the transformed pixels
		annot = np.float32(annot) - np.float32([[x_trans,y_trans,0,0,0]])
		# print(annot)
		return img_result,annot

	def random_scale(self,img,annot):
		# set scale range
		scale_range = self.scale_range
		annot = np.float32(annot)
		scale = random.random()*(scale_range[1]-scale_range[0])+scale_range[0]
		# scaling the annotation and image
		annot = annot * scale
		annot[0][4] = annot[0][4]/scale
		img_result = cv2.resize(img,None,fx=scale,fy=scale)
		return img_result,annot

	def show_img(self,img,coord):
		imgbuff = img.copy()
		for x,y,w,h,category in coord:
			x = int(x)
			y = int(y)
			w = int(w)
			h = int(h)
			cv2.rectangle(imgbuff,(x,y),(x-w,y-h),(0,0,255),5)
		for i in range(1000):
			cv2.line(imgbuff, (i*32, 0), (i*32, 768), (255, 0, 0), 1)
			cv2.line(imgbuff, (0, i*32), (1024, i*32), (255, 0, 0), 1)
		cv2.imshow('img',imgbuff)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def get_mtx(self,imgsize,coord):
		# lower_bound indicates the log2 of minimum grid size
		# choose the size of each grid
		indices = []
		grid_sizes = 64
		coords = []

		# create dictionary for conf and bias
		# key: indices, value: [conf,bias]
		result_dict = []

		height = int(np.ceil(float(imgsize[0])/grid_sizes))
		width = int(np.ceil(float(imgsize[1])/grid_sizes))
		# if no key in dictionary, create empty conf and bias array

		bias_empty = np.zeros([height,width,4],np.float32)
		conf_empty = np.zeros([height,width,1],np.float32)
		cat_empty = np.zeros([height,width,2],np.float32)
		# print(imgsize,grid_sizes[i])
		result_dict=[conf_empty,bias_empty,cat_empty]
		# get the column number and row number 
		for x,y,w,h,category in coord:
			xc = x-w/2
			yc = y-h/2
			col_num = int(np.floor(xc/float(grid_sizes)))
			row_num = int(np.floor(yc/float(grid_sizes)))
			# print(height,width,row_num,col_num)
			# comute the bias_x and bias_y
			grid_center_x = col_num*grid_sizes+grid_sizes//2
			grid_center_y = row_num*grid_sizes+grid_sizes//2
			bias_x = (xc - grid_center_x)/grid_sizes
			bias_y = (yc - grid_center_y)/grid_sizes
			# update the bias matrix and conf matrix
			conf_mtx = result_dict[0]
			bias_mtx = result_dict[1]
			cat_mtx = result_dict[2]
			conf_mtx[row_num][col_num][0] = 1.
			cat_mtx[row_num][col_num][int(category)] = 1.
			bias_mtx[row_num][col_num][0] = bias_x
			bias_mtx[row_num][col_num][1] = bias_y
			bias_mtx[row_num][col_num][2] = w/self.width
			bias_mtx[row_num][col_num][3] = h/self.height
		#print (row_num,col_num,bias_x,bias_y)
		#conf_img = cv2.resize(conf_mtx, (640, 480))
		#cv2.imshow('a',conf_img)
		#cv2.waitKey(1)
		return result_dict

	def get_img(self):
		# return one single image

		img,coord = random.sample(self.data,1)[0]
		img,coord = self.random_scale(img,coord)
		img,coord = self.random_crop(img,coord)
		result_dict = self.get_mtx(img.shape,coord)
		#self.show_img(img,coord)
		return img,result_dict

#while True:
#	a = reader()
#	a.get_img()
