# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:44:48 2020

@author: Alex
"""


from keras_preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


def get_classification_generators(df):
    
    
    datagen = ImageDataGenerator(rescale = 1./255,validation_split =0.1 )
    
    train, test = train_test_split(df, test_size=0.15)
    
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
    
    
    return train_generator, val_generator, test_generator


    