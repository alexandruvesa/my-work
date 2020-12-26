# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 23:24:50 2020

@author: 40737
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
from tensorflow.keras.layers import *
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

physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

#Create dataset
brain_df = create_dataset()


def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0
    


    
brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))


brain_df_train = brain_df.drop(columns=['patient_id'])
brain_df_train['mask'] = brain_df_train['mask'].apply(lambda x: str(x))
#Create unique dataset without same id pacient in any of dataset
# patients_id = np.unique(brain_df.patient_id)

# patients_id_train= patients_id[0:77]
# patients_id_val = patients_id[0:16]
# patients_id_test = patients_id[0:17]


# train_df = brain_df[brain_df['patient_id'].isin(patients_id_train) ]
# val_df = brain_df[brain_df['patient_id'].isin(patients_id_val) ]
# test_df = brain_df[brain_df['patient_id'].isin(patients_id_test) ]

# train_df = train_df.drop(columns = 'patient_id')
# val_df = val_df.drop(columns = 'patient_id')
# test_df = test_df.drop(columns = 'patient_id')

# train_df['mask'] =train_df['mask'].apply(lambda x: str(x))
# val_df['mask'] =val_df['mask'].apply(lambda x: str(x))
# test_df['mask'] =test_df['mask'].apply(lambda x: str(x))

datagen = ImageDataGenerator(rescale = 1./255,validation_split =0.1 )

train, test = train_test_split(brain_df_train, test_size=0.15)

train_generator = datagen.flow_from_dataframe(train,
                                              directory = '/',
                                              x_col = 'image_path',
                                              y_col = 'mask',
                                              subset = 'training',
                                              class_mode = 'categorical',
                                              batch_size = 16,
                                              shuffle=True,
                                              target_size = (256,256))

val_generator = datagen.flow_from_dataframe(train,
                                              directory = '/',
                                              x_col = 'image_path',
                                              y_col = 'mask',      
                                              subset='validation',
                                              class_mode = 'categorical',
                                              batch_size = 16,
                                              shuffle=True,
                                              target_size = (256,256))


test_generator = datagen.flow_from_dataframe(test,
                                              directory = '/',
                                              x_col = 'image_path',
                                              y_col = 'mask',                                            
                                              class_mode = 'categorical',
                                              batch_size = 16,
                                              shuffle=True,
                                              target_size = (256,256))


classification_model = ResNet50(weights='imagenet', include_top=False, input_tensor=Input(shape=(256,256,3)))

for layer in classification_model.layers:
    layers.trainable = False
    
head = classification_model.output
head = AveragePooling2D(pool_size=(4,4))(head)
head = Flatten(name='Flatten')(head)
head = Dense(256 , activation='relu')(head)
head = Dropout(0.3)(head)
head = Dense(2, activation = 'softmax')(head)

model = Model(classification_model.input, head)
model.compile(loss='categorical_crossentropy',
              optimizer = 'adam',
              metrics = ['accuracy'])


earlystopping = EarlyStopping(monitor='val_loss', 
                              mode='min', 
                              verbose=1, 
                              patience=15
                             )
checkpointer = ModelCheckpoint(filepath="clf-resnet-weights.hdf5", 
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


h = model.fit(train_generator, 
              steps_per_epoch= train_generator.n // train_generator.batch_size, 
              epochs = 30, 
              validation_data= val_generator, 
              validation_steps= val_generator.n // val_generator.batch_size, 
              callbacks=[checkpointer, earlystopping])

prediction = model.predict(test_generator)

pred = np.argmax(prediction, axis=1)
original = np.asarray(test_df['mask']).astype('int')
accuracy = accuracy_score(original, pred)
cm = confusion_matrix(original, pred)
report = classification_report(original, pred, labels=[0,1])