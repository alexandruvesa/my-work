# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:55:57 2021

@author: Alex
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 01:45:43 2021

@author: Alex
"""
from multiprocessing import Process, Lock
import os
import pydicom
from tqdm import tqdm
import multiprocessing
from multiprocessing.pool import Pool, ThreadPool
import matplotlib.pyplot as plt
from create_folders import create_folders
import threading

def clean_text(string):
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_")
        
    return string.lower()


def plot_image(dataset, figsize=(10,10)):
    plt.figure(figsize=figsize)
    plt.imshow(dataset.pixel_array, cmap = plt.cm.bone)
    plt.show()
    

def get_data_from_DICOM(ds):
    
    attributes = []
    patientID = clean_text(ds.get("PatientID","NA"))
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
   
    # generate new, standardized file name
    modality = ds.get("Modality","NA")
    studyInstanceUID = ds.get("StudyInstanceUID","NA")
    seriesInstanceUID = ds.get("SeriesInstanceUID","NA")
    instanceNumber = str(ds.get("InstanceNumber","0"))
    fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"
    
    attributes.extend([patientID,studyDate,studyDescription,seriesDescription,modality,studyInstanceUID,seriesInstanceUID,
                      instanceNumber,fileName])
    
    return attributes


# def create_folders(ds,dst_folder,patientID,studyDate,studyDescription,seriesDescription,fileName):
#      # save files to a 4-tier nested folder structure
#     if not os.path.exists(os.path.join(dst_folder, patientID)):
#         os.makedirs(os.path.join(dst_folder, patientID))
       
#     if not os.path.exists(os.path.join(dst_folder, patientID, studyDate)):
#         os.makedirs(os.path.join(dst_folder, patientID, studyDate))
       
#     if not os.path.exists(os.path.join(dst_folder, patientID, studyDate, studyDescription)):
#         os.makedirs(os.path.join(dst_folder, patientID, studyDate, studyDescription))
       
#     if not os.path.exists(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription)):
#         os.makedirs(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription))
#         print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription ))
       
#     ds.save_as(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription, fileName))
    
    #print('done.')
        
    

src_folder = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_train_images'
dst_folder = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_train_images_sorted_thread'

def read_file(file):
    pydicom.read_file(file,force=True)

def sort_files(src_folder, dst_folder):
    
    unsortedList = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if ".dcm" in file:
                unsortedList.append(os.path.join(root,file))
    print('%s files found.' % len(unsortedList))
    
    unsortedList1 = unsortedList[0:1000]
    #for dicom_loc in tqdm(unsortedList):
    threads = []
    for dicom_loc in tqdm(unsortedList1):
        t = threading.Thread(target=create_folders, args=([dicom_loc]))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
        
 

                




#ds = pydicom.read_file(dicom_loc, force = True)
    
    
    # pool = ThreadPool(multiprocessing.cpu_count())
    
    # #responses = []
    
    create_folders(unsortedList)
    # pool.map_async(create_folders,[unsortedList])
    # pool.close()
  
