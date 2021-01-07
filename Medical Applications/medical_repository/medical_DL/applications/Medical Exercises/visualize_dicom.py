# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 23:26:36 2021

@author: Alex
"""

import pydicom
import os
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib import pyplot as plt
import cv2
import seaborn as sns
from tqdm import tqdm
import multiprocessing
from multiprocessing.pool import Pool, ThreadPool


def show_dcm_info(dataset,file_path):
    print("Filename........:", file_path)
    print("Storage type...:", dataset.SOPClassUID)
    print()
    
    
    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patient's name......:", display_name)
    print("Patient id..........:", dataset.PatientID)
    print("Patient's Age.......:", dataset.PatientAge)
    print("Patient's Sex.......:", dataset.PatientSex)
    print("Modality............:", dataset.Modality)
    print("Body Part Examined..:", dataset.BodyPartExamined)
    print("View Position.......:", dataset.ViewPosition)
    
    if 'PixelData' in dataset:
        rows = int(dataset.Rows)
        cols = int(dataset.Columns)
        print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
            rows=rows, cols=cols, size=len(dataset.PixelData)))
        if 'PixelSpacing' in dataset:
            print("Pixel spacing....:", dataset.PixelSpacing)
            
            
def plot_image(dataset, figsize=(10,10)):
    plt.figure(figsize=figsize)
    plt.imshow(dataset.pixel_array, cmap = plt.cm.bone)
    plt.show()
    
    
directory = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge'
train_directory = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_train_images'
i = 1
num_to_plot = 5
for file_name in os.listdir(os.path.join(directory,'stage_2_train_images')):
    file_path = os.path.join(os.path.join(directory, 'stage_2_train_images'), file_name)
    dataset = pydicom.dcmread(file_path)
    show_dcm_info(dataset, file_path)
    plot_image(dataset)
    
    if i >=num_to_plot:
        break
    i+=1
    
    

def process_DICOM(dataset):
    _id = dataset.PatientID
    _age = dataset.PatientAge
    _sex = dataset.PatientSex
    _mean = np.mean(dataset.pixel_array)
    _max = np.max(dataset.pixel_array)
    _min = np.min(dataset.pixel_array)
    
    return _id, _age, _sex, _min, _max, _mean
    
    
def create_dataframe_from_DICOM():
    training_df = pd.DataFrame()
    
    ids = []
    ages = []
    sexs = []
    img_avg_lums = []
    img_max_lums = []
    img_min_lums = []
    
    pool = ThreadPool(multiprocessing.cpu_count())
    
    responses = []
    
    for file_name in tqdm(os.listdir(train_directory)):
        file_path = os.path.join(train_directory, file_name)
        dataset = pydicom.dcmread(file_path)
        
        responses.append(pool.apply_async(process_DICOM, (dataset,)))
    
    pool.close()
    pool.join()
    
    for element in tqdm(responses):
        _id, _age, _sex, _min, _max, _mean = element.get()
        ids.append(_id)
        ages.append(_age)
        sexs.append(_sex)
        img_min_lums.append(_min)
        img_max_lums.append(_max)
        img_avg_lums.append(_mean)
        
    training_df['patientId'] = pd.Series(ids)
    training_df['patient_age'] = pd.Series(ages, dtype = 'int')
    training_df['sex'] = pd.Series(sexs)
    
    sex_map = {'F':0, 'M':1}
    training_df['sex'] = training_df['sex'].replace(sex_map).astype('int')
    
    class_df = pd.read_csv(r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_detailed_class_info.csv')
    
    training_df = pd.merge(left = training_df, right = class_df, left_on = 'patientId', right_on = 'patientId')
    
    training_df.to_csv('training_df.csv', index=False)

    
      

   