# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:40:09 2020

@author: Alex
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Input, UpSampling2D, Add, Activation, Concatenate, MaxPool2D, AveragePooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import layers


def Resnet_modified(input_shape = (256,256,3), classes = 2):

    classification_model = ResNet50(weights='imagenet', include_top=False, input_tensor=Input(shape=input_shape))
    
    for layer in classification_model.layers:
        layers.trainable = False
        
    head = classification_model.output
    head = AveragePooling2D(pool_size=(4,4))(head)
    head = Flatten(name='Flatten')(head)
    head = Dense(256 , activation='relu')(head)
    head = Dropout(0.3)(head)
    head = Dense(classes, activation = 'softmax')(head)
    
    model = Model(classification_model.input, head)
    
    plot_model(model,to_file = 'Resnet_modified.png', show_shapes=True)
    
    return model
