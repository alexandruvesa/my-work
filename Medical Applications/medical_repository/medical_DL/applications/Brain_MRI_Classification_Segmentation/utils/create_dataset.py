import os
import numpy as np
import pandas as pd
import glob
from sklearn.model_selection import train_test_split


#data = pd.read_csv('C:/Alex Work/Research/Datasets/kaggle_3/data.csv')


def create_dataset():
    data_map = []
    for sub_dir_path in glob.glob("E:/Alex Work/Datasets/Kaggle Brain MRI/kaggle_3m/"+"*"):
        try:
            dir_name = sub_dir_path.split('/')[-1]
            for filename_name in os.listdir(sub_dir_path):
                image_path = sub_dir_path + '/' + filename_name
                data_map.extend([dir_name, image_path])
        except Exception as e:
            print (e)
            
    patient_id = [data_map[i].split("\\")[-1] for i in range(len(data_map))]
    patient_id_new = [patient_id[i] for i in range(len(patient_id)) if i%2==0]
          
            
    df = pd.DataFrame( {"patient_id" : patient_id_new,
                      "path": data_map[1::2]})
    
    df_imgs = df[~df['path'].str.contains('mask')]
    df_mask = df[df['path'].str.contains('mask')]
    
    
    #Data Sorting
    imgs = sorted(df_imgs['path'].values, key=lambda x : (int(x.split('_')[-1].split('.')[0])))
    masks = sorted(df_mask['path'].values, key=lambda x : (int(x.split('_')[-2].split('.')[0])))
    
    
    brain_df = pd.DataFrame({"patient_id": df_imgs.patient_id.values,
                             "image_path": imgs,
                             "mask_path":masks})

    return brain_df


def create_test_set(df):
    _, test = train_test_split(df, test_size=0.15)
    return test