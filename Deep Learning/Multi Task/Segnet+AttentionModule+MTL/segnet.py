# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 07:27:05 2021

@author: Alex
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPool2D, BatchNormalization , UpSampling2D, ReLU
from tensorflow.keras.initializers import HeNormal
import numpy as np


from tensorflow.python.framework.ops import disable_eager_execution

disable_eager_execution()

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

filters = [64,128,256,512,512]
initializer = tf.keras.initializers.HeNormal()

def conv_block(x, filters = 64,kernel = (3,3), strides = (1,1),padding = 'same',is_use_bias = False,name = None ):
    
    
    layer = Conv2D(filters, kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
    layer = BatchNormalization()(layer)
    layer = ReLU(name = name)(layer)
    
    return layer


def encoder_block(filters,input_image):
    
    encoders = []
      
    encoder  = conv_block(input_image, filters = 3,name='input_encoder_0')
    encoders.append(encoder)
    encoder = conv_block(encoder, filters = 3,name = 'input_encoder_0_0')
    encoders.append(encoder)
    
    for i in range(4):
        for j in range(3):
            encoder = conv_block(encoder,filters[i+1],name = 'encoder_{}_{}'.format(i,j))
            
        encoder = MaxPool2D()(encoder)
    return encoder


def decoder_block(filters,input_volume):
    decoder = conv_block(input_volume, filters = filters[-1], name = 'input_decoder_0')
    decoder = conv_block(decoder, filters = filters[-1], name='input_decoder_0_0')
    for i in range(4):
        for j in range(3):
            decoder = conv_block(decoder, filters[-i-1], name = 'decode_{}_{}'.format(i,j))
        
        decoder = UpSampling2D()(decoder)
    return decoder




input_image = np.random.randn(256,256,3)

input_layer = tf.keras.layers.Input(shape = input_image.shape)

encoder = encoder_block(filters, input_layer)
decoder = decoder_block(filters,encoder)

model = tf.keras.models.Model(inputs = input_layer, outputs = decoder)

model.save('segnet.h5')
        
#tf.keras.utils.plot_model(model, to_file = 'check_model.png', show_shapes = True)