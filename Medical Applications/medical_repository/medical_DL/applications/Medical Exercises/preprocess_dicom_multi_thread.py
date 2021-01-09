# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 02:16:37 2021

@author: Alex
"""

import pydicom
import cv2
import sys
from multiprocessing import Pool
from functools import partial
import os
from process_dicom_files import process_dicom_files
from timeit import default_timer as timer


src_folder = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_train_images'

def get_dicom_files():
    
    unsortedList = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if ".dcm" in file:
                unsortedList.append(os.path.join(root,file))
    return unsortedList



if __name__ == '__main__':

    dicom_lists = get_dicom_files()[0:1000]
    
        
    for n_processes in range(1,16):
        start = timer()
        with Pool(n_processes) as p:
            p.map(partial(process_dicom_files, ), dicom_lists)
            
        print('Took %.4f seconds with %i process(es).' % (timer() - start, n_processes))