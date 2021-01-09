# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 02:26:57 2021

@author: Alex
"""

import pydicom
import cv2
import os

OUTPUT_PATH = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\dicom_preprocess_multi_thread'
THRESH_METHOD = cv2.ADAPTIVE_THRESH_GAUSSIAN_C

def process_dicom_files(name):
    dicom = pydicom.dcmread(name)
    dicom = dicom.pixel_array
    thresh_im = cv2.adaptiveThreshold(dicom, 255, THRESH_METHOD, cv2.THRESH_BINARY, 11,2)
    
    name = name.split("\\")[-1].replace('.dcm', '.png')
    cv2.imwrite(os.path.join(OUTPUT_PATH,name), thresh_im)