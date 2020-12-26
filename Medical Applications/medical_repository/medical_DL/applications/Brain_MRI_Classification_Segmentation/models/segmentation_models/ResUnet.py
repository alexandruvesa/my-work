# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:23:26 2020

@author: Alex
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Input, UpSampling2D, Add, Activation, Concatenate, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model

class ResUnet:
    
    def __init__(self,input_shape = (256,256,3)):
        
        self.input_shape = input_shape
        self.model = self.build()
    
    def resblock(self,X,filters):
        X_copy = X
        
        X = Conv2D(filters, kernel_size = (1,1), kernel_initializer = 'he_normal')(X)
        X = BatchNormalization()(X)
        X = Activation('relu')(X)
        
        X = Conv2D(filters, kernel_size = (3,3),padding='same',kernel_initializer = 'he_normal')(X)
        X = BatchNormalization()(X)
        
        #Shortcut path
        X_copy = Conv2D(filters, kernel_size = (1,1), kernel_initializer = 'he_normal')(X_copy)
        X_copy = BatchNormalization()(X_copy)
        
        X = Add()([X, X_copy])
        X = Activation('relu')(X)
        
        return X
        
    def upsample_concat(self, x, skip):
        X = UpSampling2D((2,2))(x)
        merge = Concatenate()([X, skip])
        
        return merge
    
    def build(self):
        
        input_layer = Input(shape =(256,256,3))
        
        #Stage1
        conv_1 = Conv2D(16,3, activation = 'relu', padding='same', kernel_initializer='he_normal')(input_layer)
        conv_1 = BatchNormalization()(conv_1)
        conv_1 = Conv2D(16,3, activation = 'relu', padding='same', kernel_initializer='he_normal')(conv_1)
        conv_1 = BatchNormalization()(conv_1)  
        pool_1 = MaxPool2D((2,2))(conv_1)
        
        #Stage2
        conv_2 = self.resblock(pool_1, 32)
        pool_2 = MaxPool2D((2,2))(conv_2)
        
        #Stage3
        conv_3 = self.resblock(pool_2, 64)
        pool_3 = MaxPool2D((2,2))(conv_3)
        
        #Stage4
        conv_4 = self.resblock(pool_3, 128)
        pool_4 = MaxPool2D((2,2))(conv_4)
        
        #Stage5
        conv_5 = self.resblock(pool_4, 256)
        
        # Upsample Stage 1
        up_1 = self.upsample_concat(conv_5, conv_4)
        up_1 = self.resblock(up_1, 128)
        
        # Upsample Stage 2
        up_2 = self.upsample_concat(up_1, conv_3)
        up_2 = self.resblock(up_2, 64)
        
        # Upsample Stage 3
        up_3 = self.upsample_concat(up_2, conv_2)
        up_3 = self.resblock(up_3, 32)
        
        # Upsample Stage 4
        up_4 = self.upsample_concat(up_3, conv_1)
        up_4 = self.resblock(up_4, 16)
        
        # final output
        out = Conv2D(1, (1,1), kernel_initializer='he_normal', padding='same', activation='sigmoid')(up_4)
        
        seg_model = Model(input_layer, out)
        seg_model.summary()
        
        plot_model(seg_model,to_file = 'ResUnet.png', show_shapes=True)
        
        return seg_model
    
