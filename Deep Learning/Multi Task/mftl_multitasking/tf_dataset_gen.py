# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 06:48:58 2021

@author: alexandru.vesa
"""
import pandas as pd
import os
import tensorflow as tf
import cv2
import numpy as np

DATA_PATH = r'C:\Users\alexandru.vesa\Desktop\Research\datasets\MTFL'


train_data = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")

train_data_features = train_data.copy()

train_data_dict = {name: np.array(value) 
                         for name, value in train_data_features.items()}

features_ds = tf.data.Dataset.from_tensor_slices(train_data_dict)

for example in features_ds:
    for name, value in example.items():
        print(name,value)
    break