# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:45:41 2020

@author: alexandru.vesa
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:30:47 2020

@author: alexandru.vesa
"""
import tensorflow
import tensorflow as tf
import os
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense,Flatten, Conv2D,MaxPooling2D,Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import binary_crossentropy , sparse_categorical_crossentropy
import functools
from functools import reduce
import numpy as np

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
#x_train, x_test = x_train, x_test 
x_train=x_train/255
x_test=x_test/255
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
#y_train = tensorflow.keras.utils.to_categorical(y_train, 10)
#y_test = tensorflow.keras.utils.to_categorical(y_test, 10)
#x_train=tf.cast(x_train, tf.float32)
#x_test=tf.cast(x_test, tf.float32)
logs_base_dir = os.path.join(os.getcwd(), 'testCompose2')

input_shape = (28, 28, 1)

def compose(F):
    #calcul = lambda *F: reduce(lambda f, g: lambda x: f(g(x)), F)
    if F:
        composition = reduce(lambda f, g: lambda x: f(g(x)), F)
    else:
        print("error")
    
    return composition



def createModel():
    layer0=Input(shape=input_shape)
    layer1= Conv2D(16, kernel_size=(3, 3), activation="relu")(layer0)
    layer2= MaxPooling2D(pool_size=(2, 2))(layer1)
    layer3= Conv2D(16, kernel_size=(3, 3), activation="relu")(layer2)
    layer4=MaxPooling2D(pool_size=(2, 2))(layer3)
    layer5=Flatten()(layer4)
    layer6=Dense(10, activation='softmax')(layer5)
    
    return Model(inputs=layer0, outputs=layer6)




class GradCallback( tf.keras.callbacks.TensorBoard):
    def __init__(self, model_logs,X_train,y_train):
        super(GradCallback, self).__init__(log_dir=model_logs,
                                           histogram_freq=1,
                                           write_graph=True,
                                           update_freq='epoch',
                                           profile_batch = 100)
        
        self.X_train=X_train
        self.y_train=y_train
        
        
    def compose(self,F):
        #calcul = lambda *F: reduce(lambda f, g: lambda x: f(g(x)), F)
        if F:
            composition = reduce(lambda f, g: lambda x: f(g(x)), F)
        else:
            print("error")
        
        return composition
    
    def on_epoch_end(self, epoch, logs={}):
        super().on_epoch_end(epoch, logs)
        
        model=self.model
    
        #Create a list of all layers 
        listLayers=[layer for layer in model.layers]
        
        #Invert the list because when we compose all layers we need the last layer to be the first
        listInverted=list(reversed(listLayers))
        
        with tf.GradientTape(persistent=True, watch_accessed_variables=True) as tape:
            #track all the weights
            tape.watch(model.trainable_weights)
            #Form a function as f1(f2(f3(f4(x))))
            loss= sparse_categorical_crossentropy(y_train, compose(listInverted)(x_train))

            #loss= sparse_categorical_crossentropy(self.y_train, self.compose(listInverted)(x_train))
        
        grads_all_layers=[tape.gradient(loss,listInverted[i].trainable_weights) for i in range(len(listInverted))]
        
        #Check what list is empty because we calculated the gradients for all layers, and for exampple
        #Flatten or MaxPool does not have parameters so , no gradients there
        
        #Obtained a list with all the layers for which we have gradients
        grads_filtered_layers=[l for l in grads_all_layers if l] 
        
        tf.summary.experimental.set_step(epoch)
        
        #curr_grad=[]
        with self._get_writer('train').as_default():
            curr_grad=0
            #for i, g in enumerate(grads):
            for i in range(len(grads_filtered_layers)):
                curr_grad=grads_filtered_layers[i][0]
                
                mean=tf.reduce_mean(tf.abs(curr_grad))
                tf.summary.scalar('grad_mean_layer_{}'.format(i+1),mean)
                tf.summary.histogram('grad_histogram_layer_{}'.format(i+1),curr_grad)
                
        self._get_writer('train').flush()

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logs_base_dir,histogram_freq=1,write_grads=True)
gradient_callback=GradCallback(logs_base_dir,x_train, y_train)

model = createModel()

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=2,validation_data=(x_test, y_test), 
          callbacks=[tensorboard_callback,gradient_callback])