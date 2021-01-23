# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:59:03 2021

@author: alexandru.vesa
"""
import pandas as pd
import os
import tensorflow as tf
import cv2

from prepare_data import input_dataset,prepare_data
from single_head import single_head_cnn_model
from single_head_tf2 import single_head_cnn_model_tf2


single_task_classifier = tf.estimator.Estimator(
    model_fn=single_head_cnn_model_tf2)


single_task_classifier.train(input_fn=lambda: input_dataset(), steps=2000)


