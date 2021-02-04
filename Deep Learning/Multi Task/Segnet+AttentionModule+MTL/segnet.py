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
    
    if repeat ==2 :
        layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
        layer = BatchNormalization()(layer)
        layer = ReLU(name = name)(layer)
        
        layer = Conv2D(filters, kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (layer)
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


def segnet(input_volume, filters):
    
    encoder_1 = conv_block(input_volume, filters = 3,repeat = 2)
    encoder_1_pool = MaxPool2D()(encoder_1)

    encoder_2 = conv_block(encoder_1_pool, filters = filters[0], repeat = 2)
    encoder_2_pool = MaxPool2D()(encoder_2)

    encoder_3 = conv_block(encoder_2_pool, filters =filters[1], repeat=3)   
    encoder_3_pool = MaxPool2D()(encoder_3)
    
    encoder_4 = conv_block(encoder_3_pool,filters = filters[2], repeat=3)
    encoder_4_pool = MaxPool2D()(encoder_4)

    encoder_5 = conv_block(encoder_4_pool, filters =filters[3], repeat=3)
    encoder_5_pool = MaxPool2D()( encoder_5)
    
    
    decoder_1 = UpSampling2D(size=(2,2))(encoder_5_pool)
    decoder_1 = conv_block(decoder_1, filters = filters[3], repeat = 3)
    
    decoder_2 = UpSampling2D()(decoder_1)
    decoder_2 = concatenate([encoder_4,decoder_2])
    decoder_2 = conv_block (decoder_2,filters=filters[2], repeat =3)
    
    decoder_3 = UpSampling2D()(decoder_2)
    decoder_3 = concatenate([encoder_3,decoder_3])
    decoder_3 = conv_block (decoder_3, filters = filters[1], repeat = 3)
    
    decoder_4 = UpSampling2D()(decoder_3)
    decoder_4 = concatenate([decoder_4,encoder_2])
    decoder_4 = conv_block(decoder_4, filters = filters[0], repeat = 2)
    
    decoder_5 = UpSampling2D()(decoder_4)
    decoder_5 = concatenate([decoder_5,encoder_1])
    decoder_5 = conv_block(decoder_5, filters = 3, repeat = 2)
    
    decoder_5 = Conv2D(filters = 192, kernel_size = (1,1), strides =  (1,1) ,kernel_initializer='he_normal',padding = 'same', use_bias = False) (decoder_5)
    
    block_mtl_1 = attention_module(encoder_1, 3)
    block_mtl_1 = Multiply()([block_mtl_1,encoder_1])
    block_mtl_1 = attention_module_part_max_pooling(block_mtl_1, filters[1],kernel = 3)
    block_mtl_1 = concatenate([block_mtl_1, encoder_2])
    
    block_mtl_1 = UpSampling2D()(block_mtl_1)
    
    concat = concatenate([block_mtl_1, decoder_5])
    
    
    return concat
     

def attention_module(x,filters, kernel = 1, padding = 'same', strides = (1,1), name = None,is_use_bias = False):
    layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
    layer = BatchNormalization()(layer)
    layer = ReLU(name = name)(layer)
    layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
    layer = BatchNormalization()(layer)
    layer = tf.keras.activations.sigmoid(layer)
    
    return layer

def attention_module_part_max_pooling(x,filters, kernel = 3, padding = 'same', strides = (1,1), name = None,is_use_bias = False):
    layer = Conv2D(filters , kernel, strides =  strides,kernel_initializer='he_normal',padding = padding, use_bias = is_use_bias) (x)
    layer = ReLU(name = name)(layer)
    layer = MaxPool2D()(layer)
    
    return layer
    
    
    
input_volume = tf.keras.layers.Input(shape = (256,256,3))

    
#     encoder_1, encoder_2, encoder_3,encoder_4, encoder_5, decoder_5, decoder_4, decoder_3, decoder_2, decoder_1 = segnet(input_volume,filters)
    
#     block_1_mtl = 

# #input_volume = tf.keras.layers.Input(shape = (256,256,3))
segnet = segnet(input_volume, filters)
# #decoder = decoder_block(filters,encoder)

model = tf.keras.models.Model(inputs = input_volume, outputs = segnet)

model.save('segnet_1_mtl_blck.h5')
        
# #tf.keras.utils.plot_model(model, to_file = 'check_model.png', show_shapes = True)