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
from Ipython.display import display
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from dataset import create_dataset


#Create dataset
brain_df = create_dataset()


def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0
    


    
brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))
patients_id = np.unique(brain_df.patient_id)

patients_id_train= patients_id[0:77]
patients_id_val = patients_id[0:16]
patients_id_test = patients_id[0:17]


train_df = brain_df[brain_df['patient_id'].isin(patients_id_train) ]
val_df = brain_df[brain_df['patient_id'].isin(patients_id_val) ]
test_df = brain_df[brain_df['patient_id'].isin(patients_id_test) ]
#Creating Test, Train, Val Set
brain_df_train = brain_df.drop(columns = 'patient_id')
brain_df_train['mask'] = brain_df_train['mask'].apply(lambda x: str(x))

train, test = train_test_split(brain_df_train, test_size=0.15)