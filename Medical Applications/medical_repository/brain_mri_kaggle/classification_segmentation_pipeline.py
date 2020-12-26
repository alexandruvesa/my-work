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
from tensorflow.keras.models import load_model
from segmentation_model import ResUnet
from segmentation_model import focal_tversky, tversky

def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0

#Load models
model_clf = load_model('clf-resnet-weights.hdf5')
model_segmentation = tf.keras.models.load_model('ResUNet-segModel-weights.hdf5', custom_objects={'focal_tversky': focal_tversky,"tversky" :tversky})


brain_df = create_dataset()
brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))


brain_df_train = brain_df.drop(columns=['patient_id'])
brain_df_train['mask'] = brain_df_train['mask'].apply(lambda x: str(x))
train, test = train_test_split(brain_df_train, test_size=0.15)

#Create pipeline

def prediction(test, model , model_seg):
    
    #Store results
    mask, image_id, has_mask = [], [], []
    
    for i in test.image_path:
        
        img = io.imread(i)
        #normalizing
        img = img * 1./255
        #reshaping
        img = cv2.resize(img, (256,256))
        img = np.array(img, dtype=np.float64)
        img = np.reshape(img, (1,256,256,3))
        
        #making prediction for tumor in image
        is_defect = model.predict(img)
        if np.argmax(is_defect) ==0:
            image_id.append(i)
            has_mask.append(0)
            mask.append('No mask :')
            continue
        X = np.empty((1,256,256,3))
        # read the image
        img = io.imread(i)
        #resizing the image and coverting them to array of type float64
        img = cv2.resize(img, (256,256))
        img = np.array(img, dtype=np.float64)
        
        # standardising the image
        img -= img.mean()
        img /= img.std()
        #converting the shape of image from 256,256,3 to 1,256,256,3
        X[0,] = img
        
        #make prediction of mask
        predict = model_seg.predict(X)
        
        # if sum of predicted mask is 0 then there is not tumour
        if predict.round().astype(int).sum()==0:
            print(i)
            print(predict.round().astype(int).sum())
            image_id.append(i)
            has_mask.append(0)
            mask.append('No mask :)')
        else:
        #if the sum of pixel values are more than 0, then there is tumour
            image_id.append(i)
            has_mask.append(1)
            mask.append(predict)
            
    return pd.DataFrame({'image_path': image_id,'predicted_mask': mask,'has_mask': has_mask})


def visualize_prediction(df_pred):
    count = 0
    fig, axs = plt.subplots(15,5, figsize=(30,70))
    
    for i in range(len(df_pred)):
        if df_pred.has_mask[i] == 1 and count<15:
            #Read MRI images
            img = io.imread(df_pred.image_path[i])
            img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)
            axs[count][0].imshow(img)
            axs[count][0].title.set_text('Brain MRI')
            
            #Read original mask
            mask = io.imread(df_pred.mask_path[i])
            axs[count][1].imshow(mask)
            axs[count][1].title.set_text('Original Mask')
            
            #read predicted mask
            pred = np.array(df_pred.predicted_mask[i]).squeeze().round()
            axs[count][2].imshow(pred)
            axs[count][2].title.set_text('AI predicted mask')
            
            #overlay original mask with MRI
            img[mask==255] = (255,0,0)
            axs[count][3].imshow(img)
            axs[count][3].title.set_text('Brain MRI with original mask (Ground Truth)')
            
            #overlay predicted mask and MRI
            img_ = io.imread(df_pred.image_path[i])
            img_ = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
            img_[pred==1] = (0,255,150)
            axs[count][4].imshow(img_)
            axs[count][4].title.set_text('MRI with AI PREDICTED MASK')
            
            count +=1
        if (count==15):
            break

    fig.tight_layout()    
    
    
    

df_pred = prediction(test, model_clf, model_segmentation)        
df_pred = test.merge(df_pred, on='image_path')    
visualize_prediction(df_pred)