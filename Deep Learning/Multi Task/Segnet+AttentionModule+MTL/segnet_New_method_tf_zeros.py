# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:34:17 2021

@author: alexandru.vesa
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:58:52 2021

@author: alexandru.vesa
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPool2D, BatchNormalization,Conv2DTranspose , UpSampling2D, ReLU,concatenate,Multiply
from tensorflow.keras.initializers import HeNormal
import numpy as np



from tensorflow.python.framework.ops import disable_eager_execution

disable_eager_execution()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

filters = [64, 128, 256, 256, 512]
initializer = tf.keras.initializers.HeNormal()

def conv_block(x, filters = 64,kernel = (3,3), strides = (1,1),repeat = 2,padding = 'same',is_use_bias = False,name = None ):
    
    if repeat ==1 :
        layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
        
    
    if repeat ==2 :
        layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
        

    
    if repeat == 3:
        layer = Conv2D(filters, kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
        
        layer = Conv2D(filters, kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (layer)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
        
        layer = Conv2D(filters, kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (layer)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
    
    return layer



input_volume = tf.keras.layers.Input(shape = (256,256,3))


def create_segnet(input_volume, filters):
    
    encoders = [[tf.zeros((0))]*3]*5
    
    encoders_copy = np.copy(encoders)
    
    decoders = [[tf.zeros((0))]*3]*5
    
    decoders_copy = np.copy(decoders)
    
    encoders_copy[0][0] = conv_block(input_volume, filters = 3, repeat = 1 ,name = 'encoder_0')
    encoders_copy[0][1] = conv_block(encoders_copy[0][0], filters = 3, repeat = 1, name ='encoder_0_1' )
    encoders_copy[0][2] = MaxPool2D()(encoders_copy[0][1])
    
    for i in range(4):
        print(i)
        
        if i ==0:
            encoders_copy[i+1][0] =  conv_block(encoders_copy[i][2], filters = filters[i], repeat = 1,name ='encoder_1_{}'.format(i))
            encoders_copy[i+1][1] = conv_block(encoders_copy[i+1][0], filters = filters[i], repeat = 1,name ='encoder_1_{}'.format(i+1))
            encoders_copy[i+1][2] = MaxPool2D()(encoders_copy[i+1][1])
        
        
        if i>0:
            encoders_copy[i+1][0] = conv_block(encoders_copy[i][2], filters = filters[i+1], repeat = 1,name ='encoder_{}_{}'.format(i+1,i))
            encoders_copy[i+1][1] = conv_block(encoders_copy[i+1][0], filters = filters[i+1], repeat = 1,name ='encoder_{}_{}'.format(i+1, i+1))
        encoders_copy[i+1][2] = MaxPool2D()(encoders_copy[i+1][1])
        
    for i in range(5):
        if i ==0:
            decoders_copy[i][0] = UpSampling2D()(encoders_copy[4][2])
            decoders_copy[i][1] = conv_block(decoders_copy[i][0], filters = filters[-1],repeat = 1 , name ='decoder_{}'.format(i))
            decoders_copy[i][2] = conv_block(decoders_copy[i][1], filters = filters[-1],repeat = 1 , name ='decoder_{}_{}'.format(i,i+1))

        if i>0:
            print(i)
            decoders_copy[i][0] = UpSampling2D()(decoders_copy[i-1][2])
            decoders_copy[i][1] = concatenate([encoders_copy[-i+4][1],decoders_copy[i][0]])
            decoders_copy[i][2] = conv_block(decoders_copy[i][1], filters = filters[-i-1],repeat = 1, name = 'decoder_{}_{}'.format(i,i+1))
    
    model = tf.keras.models.Model(inputs = input_volume, outputs = decoders_copy.tolist())

    model.save('segnet_method_list.h5')
    
    tf.keras.utils.plot_model(model, 'monel.png', show_shapes = True)