# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:30:09 2021

@author: alexandru.vesa
"""



import pandas as pd
import os
import tensorflow as tf
import cv2

DATA_PATH = r'E:\Alex Work\Datasets\MTFL'


def prepare_data(path = 'training.txt'):
    

    train_data = pd.read_csv(os.path.join(DATA_PATH, path), sep=' ', header=None, skipinitialspace=True, nrows=10000)
    train_data.iloc[:, 0] = train_data.iloc[:, 0].apply(lambda s: s.replace('\\', '/'))
    train_data.iloc[:,0] = train_data.iloc[:,0].apply(lambda s: os.path.join(DATA_PATH,s))
    filenames = tf.constant(train_data.iloc[:,0].tolist())
    labels = tf.constant(train_data.iloc[:,1:].values)
    
    return filenames,labels

def parse_function(filename,label):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string, channels=3) # Channels needed because some test images are b/w
    image_resized = tf.image.resize(image_decoded, [40, 40])
    image_resized = tf.cast(image_resized, dtype = tf.float32)
    image_shape = tf.cast(tf.shape(image_decoded), tf.float32)
    label = tf.cast(label, dtype = tf.float32)

    label = tf.concat([label[0:5] / image_shape[0], label[5:10] / image_shape[1], label[10:]], axis=0)

    return {"x": image_resized}, label
    

def input_dataset(path = 'training.txt', is_eval = False):
    filenames,labels = prepare_data(path) 
    dataset = tf.data.Dataset.from_tensor_slices((filenames,labels))
    dataset = dataset.map(parse_function)
    
    if is_eval:
        dataset = dataset.batch(16)
    else:
        dataset = dataset.repeat().shuffle(1000).batch(16)
        
    return dataset