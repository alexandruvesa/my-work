# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 23:15:16 2020
ResUnet
https://arxiv.org/pdf/1904.00592.pdf
@author: Alex
"""



import tensorflow as tf
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score
from applications.Brain_MRI_Classification_Segmentation.utils.create_dataset import create_dataset, create_test_set
from applications.Brain_MRI_Classification_Segmentation.models.classification_models.Resnet_modified import Resnet_modified
from applications.Brain_MRI_Classification_Segmentation.models.segmentation_models.ResUnet import ResUnet
from applications.Brain_MRI_Classification_Segmentation.generators.classification_generator import get_classification_generators
from applications.Brain_MRI_Classification_Segmentation.generators.DataGeneratorSegmentation import DataGeneratorSegmentation
from applications.Brain_MRI_Classification_Segmentation.utils.loss_functions import tversky, focal_tversky



physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0
    

def get_data_segmentation():
    

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
    
    
    train_data = DataGeneratorSegmentation(train_ids, train_mask )
    val_data = DataGeneratorSegmentation(val_ids, val_mask)
    
    return train_data, val_data

def get_data_classification():
    brain_df = create_dataset()
    brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))
    brain_df_train = brain_df.drop(columns=['patient_id'])
    brain_df_train['mask'] = brain_df_train['mask'].apply(lambda x: str(x))
    
    
    test_data = create_test_set(brain_df_train)
    train_generator, val_generator, test_generator = get_classification_generators(brain_df_train)

    return train_generator, val_generator, test_generator, test_data


def get_callbacks_classification_model():
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
        
    return callbacks


def get_callbacks_segmentation_model():
    
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


def train_classification_model(epochs = 1):
    model_clf = Resnet_modified()
    model_clf.compile(loss='categorical_crossentropy',
              optimizer = 'adam',
              metrics = ['accuracy'])
    
    
    train_generator, val_generator, test_generator, test_data = get_data_classification()
    callbacks = get_callbacks_classification_model()
    model_clf.fit(train_generator, 
              steps_per_epoch= train_generator.n // train_generator.batch_size, 
              epochs = epochs, 
              validation_data= val_generator, 
              validation_steps= val_generator.n // val_generator.batch_size, 
              callbacks = callbacks)
    
    
    prediction = model_clf.predict(test_generator)
    
    pred = np.argmax(prediction, axis=1)
    original = np.asarray(test_data['mask']).astype('int')
    accuracy = accuracy_score(original, pred)
    cm = confusion_matrix(original, pred)
    report = classification_report(original, pred, labels=[0,1])
    
    print(accuracy, cm , report)
    
    
def train_segmentation_model(epochs = 1):
    
    model = ResUnet()
    adam = tf.keras.optimizers.Adam(lr = 0.01, epsilon = 0.1)
    model.model.compile(optimizer = adam, 
                  loss = focal_tversky, 
                  metrics = [tversky]
                  )
    train_data, val_data = get_data_segmentation()
    callbacks = get_callbacks_segmentation_model()
    model.model.fit(train_data, 
                  epochs = 60, 
                  validation_data = val_data,
                  callbacks = callbacks
               
                  )

train_segmentation_model()
    

