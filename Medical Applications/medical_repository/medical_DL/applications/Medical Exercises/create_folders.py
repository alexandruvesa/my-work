# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 16:10:56 2021

@author: Alex
"""
import os
from tqdm import tqdm
import pydicom

def clean_text(string):
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_")
        
    return string.lower()

def create_folders( dicom_loc):
    dst_folder = r'E:\Alex Work\Datasets\rsna-pneumonia-detection-challenge\stage_2_train_images_sorted_thread'

   
    ds = pydicom.read_file(dicom_loc, force = True)
    # responses.append(pool.apply_async(get_data_from_DICOM, (ds,)))
    
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
    
    # uncompress files (using the gdcm package)
    #DICOM files may have image compression performed 
    #on them either during storage or during transfer via the DICOM receiver. 
    #For example, at our institution, all DICOMs have JPEG2000 compression
    try:
        ds.decompress()
    except:
        print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (patientID, studyDate, studyDescription, seriesDescription ))    
    
     # save files to a 4-tier nested folder structure
    if not os.path.exists(os.path.join(dst_folder, patientID)):
        os.makedirs(os.path.join(dst_folder, patientID))
       
    if not os.path.exists(os.path.join(dst_folder, patientID, studyDate)):
        os.makedirs(os.path.join(dst_folder, patientID, studyDate))
       
    if not os.path.exists(os.path.join(dst_folder, patientID, studyDate, studyDescription)):
        os.makedirs(os.path.join(dst_folder, patientID, studyDate, studyDescription))
       
    if not os.path.exists(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription)):
        os.makedirs(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription))
        print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription ))
       
    ds.save_as(os.path.join(dst_folder, patientID, studyDate, studyDescription, seriesDescription, fileName))

    #print('done.')
        