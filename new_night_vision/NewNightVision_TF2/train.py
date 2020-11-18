# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 00:06:57 2020

@author: alexandru.vesa
"""
import tensorflow 
from generator.csv_generator import CSVGenerator
from CNN.looses import smooth_l1, focal
from CNN.Network import create_final_model
from keras.optimizers import Adam

lr = 0.001

annotations = r'C:\Users\alexandru.vesa\Desktop\Research\New_Personal_Program_DL_Programming\GitMy\my-work\NewNightVision\test2.csv'
classes= r'C:\Users\alexandru.vesa\Desktop\Research\New_Personal_Program_DL_Programming\GitMy\my-work\NewNightVision\classes.txt'

#Create model

retina_detnet = create_final_model(nb_of_classes = 1)


retina_detnet.compile(
        loss={
            'regression'    : smooth_l1(),
            'classification': focal()
        },
        optimizer= Adam(lr=lr, clipnorm=0.001)
    )



train_generator = CSVGenerator(
            annotations, classes)


retina_detnet.fit_generator(train_generator, steps_per_epoch = 100, epochs = 1)