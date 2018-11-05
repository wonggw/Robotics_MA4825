import model as M 
import numpy as np 
import tensorflow as tf 
import time 

def build_model(inp_holder):
	with tf.variable_scope('YOLO_V0'):
#		inp_holder = tf.image.random_saturation(inp_holder,lower=0.7,upper=1.6)
#		inp_holder = tf.image.random_contrast(inp_holder,lower=0.7,upper=1.7)
#		inp_holder = tf.image.random_brightness(inp_holder,20)
		mod = M.Model(inp_holder)
		mod.spconvLayer(3,6,stride=2,activation=M.PARAM_ELU,batch_norm=True)#240_ 2x2
		mod.convLayer(3,24,stride=2,activation=M.PARAM_ELU,batch_norm=True)#120_ 4x4
		mod.maxpoolLayer(3,2)#60_ 8x8
		mod.spconvLayer(3,4,stride=2,activation=M.PARAM_ELU,batch_norm=True)#30_16x16
		mod.convLayer(3,96,stride=2,activation=M.PARAM_ELU,batch_norm=True)#15_32_32
		l0=mod.maxpoolLayer(3,2)#7_ 64x64
		l1=mod.dwconvLayer(3,3,activation=M.PARAM_ELU,batch_norm=True)
		l2=mod.concat_to_current(l0)
		l3=mod.NIN(3,288,288,activation=M.PARAM_ELU)
		l4=mod.concat_to_current(l2)
		l3=mod.NIN(3,302,302,activation=M.PARAM_ELU)
		feature = mod.convLayer(1,7)

	return feature

inpholder = tf.placeholder(tf.float32,[None,None,None,3])
b_labholder = tf.placeholder(tf.float32,[None,None,None,4])
c_labholder = tf.placeholder(tf.float32,[None,None,None,1])
cat_labholder = tf.placeholder(tf.float32,[None,None,None,2])

feature = build_model(inpholder)
bias,conf,cat =tf.split(feature,[4,1,2], 3)
bias1,bias2=tf.split(bias,[2,2],3)
b1_labholder,b2_labholder=tf.split(b_labholder,[2,2],3)

with tf.variable_scope('loss_function'):
	with tf.variable_scope('bias_loss_x_y'):
		bias1_loss = tf.reduce_sum(tf.reduce_mean(tf.square(bias1 - b1_labholder)*c_labholder,axis=0)) #x,y
	with tf.variable_scope('bias_loss_w_h'):
		bias2_loss = tf.reduce_sum(tf.reduce_mean(tf.square(tf.sqrt(tf.abs(bias2)) - tf.sqrt(tf.abs(b2_labholder)))*c_labholder,axis=0))#w,h
	conf_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=c_labholder,logits=conf,name="Propose_bounding_box"))
	cat_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=cat_labholder,logits=cat,name="Categorize_class"))

with tf.variable_scope('Total_losses'):
	total_loss = 3*(bias1_loss+ bias2_loss) + conf_loss + cat_loss
gradient_accum=M.Trainer(0.0002,total_loss)
zero_ops=gradient_accum.zero()
accum_ops=gradient_accum.accumulate()
step = gradient_accum.train()
