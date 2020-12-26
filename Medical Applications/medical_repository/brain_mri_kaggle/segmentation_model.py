# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:37:38 2020

@author: Alex
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 16:11:47 2020

@author: 40737
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import cv2
from skimage import io

import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.keras import layers, optimizers
from tensorflow.keras.layers import Conv2D, BatchNormalization, Add, Activation, Concatenate, UpSampling2D,Input,InputLayer, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model
import tensorflow.keras.backend as K

import random
import glob
from sklearn.preprocessing import StandardScaler, normalize
#from Ipython.display import display
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from dataset import create_dataset
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score
from tensorflow.keras.utils  import get_custom_objects

def create_callbacks():
    earlystopping = EarlyStopping(monitor='val_loss', 
                              mode='min', 
                              verbose=1, 
                              patience=15
                             )
    checkpointer = ModelCheckpoint(filepath="ResUNet-segModel-weights.hdf5", 
                                   verbose=1, 
                                   save_best_only=True
                                  )
    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  mode='min',
                                  verbose=1,
                                  patience=10,
                                  min_delta=0.0001,
                                  factor=0.2
                                 )
    callbacks = [checkpointer, earlystopping, reduce_lr]
    
    return callbacks

def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0
    


def get_data():
    

    #Create dataset
    brain_df = create_dataset()
    brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))

    #Search for the mask    
    brain_df_mask = brain_df[brain_df['mask'] == 1]

    #Creating train, val , test
    
    x_train, x_val = train_test_split(brain_df_mask, test_size = 0.15)
    x_test, x_val =  train_test_split(x_val, test_size = 0.5)
    
    train_ids = list(x_train.image_path)
    train_mask = list(x_train.mask_path)
    
    val_ids = list(x_val.image_path)
    val_mask = list(x_val.mask_path)
    
    return train_ids, train_mask, val_ids, val_mask


class DataGeneratorSegmentation(tf.keras.utils.Sequence):
    def __init__(self, ids, mask, image_dir = './', batch_size = 16, img_h=256, img_w=256, shuffle=True):
        
        self.ids = ids
        self.mask = mask
        self.image_dir = image_dir
        self.batch_size = batch_size
        self.img_h = img_h
        self.img_w = img_w
        self.shuffle = shuffle
        self.on_epoch_end()
        
    def __len__(self):
        return int(np.floor(len(self.ids)) / self.batch_size)
    
    def __getitem__(self, index):
        
        #generate index of batch_size length
        indexes = self.indexes[index*self.batch_size : (index+1)*self.batch_size]
        
        list_ids = [self.ids[i] for i in indexes]
        list_mask = [self.mask[i] for i in indexes]
        
        X, y = self.__data_generation(list_ids, list_mask)
        
        return X,y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.ids))
        
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_ids, list_mask):
        
        X = np.empty((self.batch_size, self.img_h, self.img_w, 3))
        y = np.empty((self.batch_size, self.img_h, self.img_w, 1))
        
        for i in range(len(list_ids)):
            img_path =  str(list_ids[i])
            
            mask_path = str(list_mask[i])
            
            img = io.imread(img_path)
            mask = io.imread(mask_path)
            
            img = cv2.resize(img, (self.img_h, self.img_w))
            img = np.array(img, dtype = np.float64)
            
            mask = cv2.resize(mask, (self.img_h, self.img_w))
            mask = np.array(mask, dtype = np.float64)
            
            #Standardising
            img -= img.mean()
            img /=img.std()
            
            mask -= mask.mean()
            mask /=mask.std()
            
            #Add image to empty array
            X[i,] = img
            y[i,] = np.expand_dims(mask, axis=2)
            
        #Normalize y
        y = (y>0).astype(int)
        
        return X,y

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
        
        return seg_model


def get_generators():    

    train_ids, train_mask, val_ids, val_mask = get_data()
    train_data = DataGeneratorSegmentation(train_ids, train_mask )
    val_data = DataGeneratorSegmentation(val_ids, val_mask)
    
    return train_data, val_data



def tversky(y_true, y_pred):
    y_true_pos = K.flatten(y_true)
    y_pred_pos = K.flatten(y_pred)
    true_pos = K.sum(y_true_pos * y_pred_pos)
    false_neg = K.sum(y_true_pos * (1-y_pred_pos))
    false_pos = K.sum((1-y_true_pos)*y_pred_pos)
    alpha = 0.7
    return (true_pos + 1)/(true_pos + alpha*false_neg + (1-alpha)*false_pos + 1)


def focal_tversky(y_true,y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    
    pt_1 = tversky(y_true, y_pred)
    gamma = 0.75
    return K.pow((1-pt_1), gamma)





# adam = tf.keras.optimizers.Adam(lr = 0.01, epsilon = 0.1)

# model = ResUnet()

# model.model.compile(optimizer = adam, 
#                   loss = focal_tversky, 
#                   metrics = [tversky]
#                  )

# train_data, val_data = get_generators()

# callbacks = create_callbacks()

# h = model.model.fit(train_data, 
#                   epochs = 60, 
#                   validation_data = val_data,
#                   callbacks = callbacks
               
#                  )