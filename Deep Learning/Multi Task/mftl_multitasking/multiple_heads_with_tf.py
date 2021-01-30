# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 12:40:17 2021

@author: alexandru.vesa
"""

import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, BatchNormalization, Flatten, Activation, Dropout
from tensorflow.keras.models import Model
from prepare_data import input_dataset
import cv2
import matplotlib.pyplot as plt
import numpy as np


config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

def base(input_layer):
  # Input layer
  #input_layer = tf.keras.layers.Input(shape = ( 40, 40, 3))
  #nput_layer = tf.reshape(vector, [-1, 40, 40, 3])

  # First convolutive layer
  conv1 = tf.keras.layers.Convolution2D( filters=16, kernel_size=[5, 5], padding="same", activation=tf.nn.relu)(input_layer)
  pool1 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv1)

  # Second convolutive layer
  conv2 = tf.keras.layers.Convolution2D (filters=48, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)(pool1)
  pool2 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv2)
  
  # Third convolutive layer
  conv3 = tf.keras.layers.Convolution2D(filters=64, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)(pool2)
  pool3 = tf.keras.layers.MaxPooling2D( pool_size=[2, 2], strides=2)(conv3)
  
  # Fourth convolutive layer
  conv4 = tf.keras.layers.Convolution2D( filters=64, kernel_size=[2, 2], padding="same", activation=tf.nn.relu)(pool3)
  
  # Dense Layer
  #flat = tf.reshape(conv4, [-1, 5 * 5 * 64])
  #dense = Dense( units=100, activation=tf.nn.relu)(flat)
  
  return conv4    

def nose_head(backbone):
    x = Conv2D(32, (3, 3), padding="same")(backbone)
    x = Activation("relu")(x)
    x = BatchNormalization(axis=-1)(x)
    x = MaxPooling2D(pool_size=(3, 3))(x)
    x = Dropout(0.25)(x)
    x = Flatten()(x)
    x = Dense(256)(x)
    x = Activation("relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(2)(x)
    x = Activation('softmax', name="nose")(x)
	# return the category prediction sub-network
    return x


def head_pose_head(backbone):

    x = Conv2D(64, (3, 3), padding="same")(backbone)
    x = Activation("relu")(x)
    x = BatchNormalization(axis=-1)(x)
    x = MaxPooling2D(pool_size=(3, 3))(x)
    x = Dropout(0.25)(x)
    x = Flatten()(x)
    x = Dense(128)(x)
    x = Activation("relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(2)(x)
    x = Activation('softmax', name="left_mouth")(x)
	# return the category prediction sub-network
    return x
    

def right_mouth(backbone):

    x = Conv2D(64, (3, 3), padding="same")(backbone)
    x = Activation("relu")(x)
    x = BatchNormalization(axis=-1)(x)
    x = MaxPooling2D(pool_size=(3, 3))(x)
    x = Dropout(0.25)(x)
    x = Flatten()(x)
    x = Dense(64)(x)
    x = Activation("relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(2)(x)
    x = Activation('softmax', name="right_mouth")(x)
	# return the category prediction sub-network
    return x

def final_model():
    input_layer = tf.keras.layers.Input(shape = ( 120, 120, 3))

    backbone = base(input_layer)
    nose = nose_head(backbone)
    head = head_pose_head(backbone)
    #right_mouths = right_mouth(backbone)
    
    model = Model(
			inputs=input_layer,
			outputs=[nose,head],
			name="test")

    
    return model

model = final_model()

#tf.keras.utils.plot_model(model, to_file='model.png')



losses = {
	"nose": "mean_squared_error",
	"left_mouth": "mean_squared_error",

}

#lossWeights = {"nose": 1.0, "left_mouth": 0.5,  "right_mouth":0.8}


optimizer = tf.keras.optimizers.Adam(lr = 0.001)

model.compile(optimizer = optimizer, loss = losses, metrics = ['accuracy'])

dataset = input_dataset()

dataset_eval = input_dataset(path = 'testing.txt' ,is_eval = True)

model.fit(dataset, epochs = 20)


prediction = model.predict(dataset)

predictiom_image_0_nose = prediction[0][1]
prediction_image_0_head = prediction[1][1]
#prediction_image_0_head = prediction[2][0]


path = r'E:\Alex Work\Datasets\MTFL\AFLW\0002-image04733.jpg'   
# image_string = tf.io.read_file(path)
# image_decoded = tf.image.decode_jpeg(image_string, channels=3) # Channels needed because some test images are b/w
# image_resized = tf.image.resize(image_decoded, [40, 40])
# image_resized = tf.cast(image_resized, dtype = tf.float32)
# image_resized = image_resized[:,:,1]
# image_resized =tf.reshape(image_resized, (40,40))
# image_shape = tf.cast(tf.shape(image_decoded), tf.float32)

image_resized = cv2.imread(path)
image_resized = cv2.cvtColor(image_resized, cv2.COLOR_RGB2GRAY)

#image_resized= image_resized[:,:,1]
image_resized = cv2.resize(image_resized,(120,120))
image_resized = np.reshape(image_resized, (120,120,1))
     
plt.imshow(image_resized)
plt.scatter(predictiom_image_0_nose[0]*120,predictiom_image_0_nose[1]*120,marker='x', color='red')
plt.scatter(prediction_image_0_head[0]*120, prediction_image_0_head[1]*120,marker='x', color='blue')
plt.scatter(prediction_image_0_head[0]*120, prediction_image_0_head[1]*120, marker='x',color='yellow')

plt.show()




