# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:53:12 2020

@author: alexandru.vesa
"""
import cv2
import pandas as pd
import numpy as np
import keras
from AnchorsGen import anchor_targets_bbox,anchors_for_shape,guess_shapes


class DataGenerator:

    def __init__(self, path_to_csv):
        #self.config = config
        self.path_to_csv = path_to_csv

        # read data
        self.df = pd.read_csv(path_to_csv)
        self.df['ImageName'] = self.df.Frame.apply(
            lambda x: x.split("_TimeStamp")[0].split("\\")[-1])

        # create annotation
        self.df['outbox_2'] = self.df['xmax'] - self.df['xmin'] + 1.0  # width
        self.df['outbox_3'] = self.df['ymax'] - self.df['ymin'] + 1.0  # height
        self.df['outbox_0'] = self.df['xmin'] + 0.5 * self.df['outbox_2']
        self.df['outbox_1'] = self.df['ymin'] + 0.5 * self.df['outbox_3']
        self.df['category'] = np.where(
            self.df["Label"].values == "PedestrianNV", 0, 1)

        # create groups
        column_csv = ['ImageName', 'category', 'xmin', 'ymin', 'xmax',
                      'ymax', 'Frame', 'outbox_0', 'outbox_1', 'outbox_2', 'outbox_3']
        self.dfGrup = self.df[column_csv].groupby(['ImageName'])
        self.grup_v = np.unique(self.df['ImageName'].values)

    def get_len_img(self):
        return len(self.grup_v)

    def read_img(self, img_name):
        img = cv2.imread(img_name).astype(np.float32, copy=False)
        img=cv2.resize(img, (1280,768))
        # print(img_name)
        return img

    def getAnnotations(self, x):
        return x[["outbox_0", "outbox_1", "outbox_2", "outbox_3", "category"]].values.tolist()

    # return images and annotations

    def getData(self, list_numbers):
        img = self.getInfoImageGroups(list_numbers)
        annotations = self.getInfoAnnotationsGroups(list_numbers)

        return img, annotations

    def getDataWithImages(self, list_numbers):
        img = self.getInfoImageGroups(list_numbers)
        annotations = self.getInfoAnnotationsGroups(list_numbers)
        name_imgs = self.grup_v[list_numbers]

        return img, annotations, name_imgs

    def getInfoImageGroups(self, list_numbers):
        l_group = list(map(lambda x: self.dfGrup.get_group(
            x), self.grup_v[list_numbers]))
        list_img = list(map(lambda dfx: dfx["Frame"].iloc[0], l_group))
        return np.asarray(list(map(self.read_img, list_img)))

    def getInfoAnnotationsGroups(self, list_numbers):
        l_group = list(map(lambda x: self.dfGrup.get_group(
            x), self.grup_v[list_numbers]))
        return list(map(lambda x: self.getAnnotations(x), l_group))
    
    
    
def compute_inputs(image_group):
        """ Compute inputs for the network using an image_group.
        """
        # get the max image shape
        batch_size =4
        max_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))

        # construct an image batch object
        image_batch = np.zeros((batch_size,) + max_shape, dtype=keras.backend.floatx())

        # copy all images to the upper left part of the image batch object
        for image_index, image in enumerate(image_group):
            image_batch[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image

        if keras.backend.image_data_format() == 'channels_first':
            image_batch = image_batch.transpose((0, 3, 1, 2))

        return image_batch
    
 
    
def generate_anchors(image_shape):
        anchor_params = None
        pyramid_levels = None
        
        compute_shapes = guess_shapes

        return anchors_for_shape(image_shape, anchor_params=anchor_params, pyramid_levels=pyramid_levels, shapes_callback=compute_shapes) 
   
 
def compute_targets(image_group, annotations_group):
        """ Compute target outputs for the network using images and their annotations.
        """
        # get the max image shape
        max_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))
        anchors   = generate_anchors(max_shape)

        batches = anchor_targets_bbox(
            anchors,
            image_group,
            annotations_group,
           2
        )

        return list(batches)   
    
def transform_annotations(boxes):
    annotations = {'labels': np.empty((0,)), 'bboxes': np.empty((0, 4))}
    
    for i in range(len(boxes)):

        annotations['labels'] = np.concatenate((annotations['labels'], annotations[i][-1])
        annotations['bboxes'] = np.concatenate((annotations['bboxes'], [[annotations[0]
                float(annot['x1']),
                float(annot['y1']),
                float(annot['x2']),
                float(annot['y2']),
            ]]))
    
   
lista = [1,2,3,4]
path = r'C:\Users\alexandru.vesa\Desktop\Research\New_Personal_Program_DL_Programming\NewNightVision\img_train.csv'
dg = DataGenerator( path)
imgs, annotations  = dg.getData(lista)


image_batch = compute_inputs(imgs)

annotations2 = annotations[0] *4
batches = compute_targets(imgs, annotations2)
