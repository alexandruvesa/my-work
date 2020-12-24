# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 18:10:20 2020

@author: 40737
"""

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

from dataset import create_dataset


#Create dataset
brain_df = create_dataset()


def pos_neg_diagnosis(mask_path):
    value = np.max(cv2.imread(mask_path))
    if value > 0 :
        return 1
    else:
        return 0
    

def create_figure(brain_df):    

    #Create interactive plots
    fig = go.Figure([go.Bar(x=brain_df['mask'].value_counts().index,
                            y=brain_df['mask'].value_counts(),
                            width=[.4,.4])])
    
    fig.update_traces (marker_color = 'rgb(158,202,225)', marker_line_color=
                       'rgb(8,48,107)',
                       marker_line_width = 4, opacity = 0.4)
    
    fig.update_layout(title_text = "Mask Count Plot",
                      width = 700,
                      height=550,
                      yaxis=dict(
                          title_text="Count",
                      tickmode='array',
                      titlefont=dict(size=20)))
    
    fig.update_yaxes(automargin=True)
    fig.show()
    
def visualize_tumor(brain_df):
    for i in range(len(brain_df)):
        if cv2.imread(brain_df.mask_path[i]).max() >0:
            break
        
    plt.figure(figsize=(8,8))
    plt.subplot(1,2,1)
    plt.imshow(cv2.imread(brain_df.mask_path[i]))
    plt.title('tumor location')
    plt.subplot(1,2,2)
    plt.imshow(cv2.imread(brain_df.image_path[i]))    
    
brain_df['mask'] = brain_df['mask_path'].apply(lambda x : pos_neg_diagnosis(x))
