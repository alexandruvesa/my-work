# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:30:47 2020

@author: alexandru.vesa
"""
import tensorflow
import tensorflow as tf
import os
from tensorflow.keras.layers import Dense,Flatten, Conv2D,MaxPooling2D,Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import binary_crossentropy , sparse_categorical_crossentropy
import functools
from functools import reduce

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train, x_test 

#x_train=tf.cast(x_train, tf.float32)
#x_test=tf.cast(x_test, tf.float32)
logs_base_dir = os.path.join(os.getcwd(), 'logs5')


def compose(F):
    #calcul = lambda *F: reduce(lambda f, g: lambda x: f(g(x)), F)
    if F:
        calcul = reduce(lambda f, g: lambda x: f(g(x)), F)
    else:
        print("error")
    
    return calcul

def SequentialModel():
    

    model =  Sequential()
    layer0=Flatten(input_shape=(28,28))
    model.add(layer0)
    layer1=Dense(8, input_dim=10, activation='relu')
    model.add(layer1)
    
    layer2=Dense(16, activation='relu')
    model.add(layer2)
    
    layer3=Dense(10, activation='softmax')
    model.add(layer3)
    
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    
    
    return model

input_shape = (28, 28, 1)

def CreateMultipleLayers():
    layer0=Input(shape=input_shape)
    layer1= Conv2D(32, kernel_size=(3, 3), activation="relu"),
    layer2= MaxPooling2D(pool_size=(2, 2))
    layer3= Conv2D(64, kernel_size=(3, 3), activation="relu"),
    layer4=MaxPooling2D(pool_size=(2, 2))
    layer5=Flatten()
    layer6=Dense(10, activation='softmax')
    
    lista_layere=[layer0, layer1, layer2, layer3, layer4, layer5, layer6]
    lista_noua=list(reversed(lista_layere))
    return compose(layer1, layer2, layer3, layer4, layer5, layer6)

def createModelWithCompose():
    body = CreateMultipleLayers(inputs)




class GradCallback( tf.keras.callbacks.TensorBoard):
    def __init__(self, model_logs,X_train,y_train):
        super(GradCallback, self).__init__(log_dir=model_logs,
                                           histogram_freq=1,
                                           write_graph=True,
                                           update_freq='epoch',
                                           profile_batch = 100000000)
        
        self.X_train=X_train
        self.y_train=y_train
    def on_epoch_end(self, epoch, logs={}):
        super().on_epoch_end(epoch, logs)
        
        model=self.model
        layer0=model.layers[0]
        layer1=model.layers[1]
        layer2=model.layers[2]
        layer3=model.layers[3]
        
        

        with tf.GradientTape(persistent=True, watch_accessed_variables=True) as tape:
            #track all the weights
            tape.watch(model.trainable_weights)
            loss= sparse_categorical_crossentropy(self.y_train, layer3(layer2(layer1(layer0(self.X_train)))))
        grads=[]
        #We have 3 layers with weights for every neuron
        #So we want to calculate the derivative of loss with respect of
        #every weights layer
        
        gradient_layer1=tape.gradient(loss, layer1.trainable_weights)
        grads.append(gradient_layer1)
        gradient_layer2=tape.gradient(loss,layer2.trainable_weights)
        grads.append(gradient_layer2)
        gradient_layer3=tape.gradient(loss,layer3.trainable_weights)
        grads.append(gradient_layer3)
        
        tf.summary.experimental.set_step(epoch)
        
        
        with self._get_writer('train').as_default():
            for i, g in enumerate(grads):
                curr_grad=g[0]
                
                mean=tf.reduce_mean(tf.abs(curr_grad))
                tf.summary.scalar('grad_mean_layer_{}'.format(i+1),mean)
                tf.summary.histogram('grad_histogram_layer_{}'.format(i+1),curr_grad)
                
        self._get_writer('train').flush()

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logs_base_dir,histogram_freq=1,write_grads=True)
gradient_callback=GradCallback(logs_base_dir,x_train, y_train)



model.fit(x_train, y_train, epochs=10,validation_data=(x_test, y_test), 
          callbacks=[tensorboard_callback,gradient_callback])