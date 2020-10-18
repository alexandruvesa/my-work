# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 00:34:09 2020

@author: alexandru.vesa
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from sklearn import preprocessing
import pptk
import pandas as pd
from astropy.io import ascii
import h5py

path=r'C:\Users\alexandru.vesa\Downloads\Datasets\Semantic3D_Dataset\Semantic3D_Dataset_Big\bildstein_station1_xyz_intensity_rgb.txt'

pathL=r'C:\Users\alexandru.vesa\Downloads\Datasets\Semantic3D_Dataset\Semantic3D_Dataset_Big\bildstein_station1_xyz_intensity_rgb.labels'



def readPointClouds(filename):
    data=pd.read_csv(filename, sep=" ", header=None)
    
    xyz=data.iloc[:,:3]
    rgb=data.iloc[:,4:]
    
    return xyz, rgb


def save_h5(h5_filename, data, label, data_dtype='float32', label_dtype='float32'):
    h5_fout = h5py.File(h5_filename)
    h5_fout.create_dataset(
        'data', data=data,
        compression='gzip', compression_opts=4,
        dtype=data_dtype)
    h5_fout.create_dataset(
        'label', data=label,
        compression='gzip', compression_opts=1,
        dtype=label_dtype)
    h5_fout.close()


def load_h5(h5_filename):
    f = h5py.File(h5_filename)
    data = f['data'][:]
    label = f['label'][:]
    return (data, label)


def readLabel(filename):
    label= ascii.read(filename, format='basic',
          fast_reader={'parallel': True, 'use_fast_converter': True}) 

    #convert to list
    labelConverted=[ label[i][0] for i in range(len(label))]
    
    return labelConverted


xyz, rgb=readPointClouds(path)

h5_filename=r'C:\Users\alexandru.vesa\Desktop\Research\New_Personal_Program_DL_Programming\GitMy\my-work\3D_CNN\Semantic3d_Competition\test.hdf5'

save_h5(h5_filename, xyz, tC)


a,b= load_h5(h5_filename)
v = pptk.viewer(xyz,rgb/255)


test_Bag=r'C:\Users\alexandru.vesa\Downloads\Datasets\Seg_Prep\Motorbike.h5'
bag=load_h5(test_Bag)
bagView=pptk.viewer(bag[0])