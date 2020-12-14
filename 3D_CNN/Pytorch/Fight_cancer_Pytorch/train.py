# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:56:18 2020

@author: Alex
"""

import argparse
import datetime
import os 
import sys

import numpy as np

from torch.utils.tensorboard import SummaryWriter

import torch
import torch.nn as nn
from torch.optim import SGD, Adam
from torch.utils.data import DataLoader

from data_prep import LunaDataset
from model_pytorch import LunaModel

from logconf import logging


log = logging.getLogger(__name__)
# log.setLevel(logging.WARN)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


METRICS_LABEL_NDX = 0
METRICS_PRED_NDX = 1
METRICS_LOSS_NDX = 2
METRICS_SIZE = 3

class LunaTrainingApp:
    def __init__(self, sys_argv=None):
         if sys_argv is None:
             sys_argv = sys.argv[1:]
 
         parser = argparse.ArgumentParser()
         parser.add_argument('--num-workers',
             help='Number of worker processes for background data loading',
             default=8,
             type=int,
         )
         parser.add_argument('--batch-size',
             help='Batch size to use for training',
             default=32,
             type=int,
         )
         parser.add_argument('--epochs',
             help='Number of epochs to train for',
             default=1,
             type=int,
         )
 
         parser.add_argument('--tb-prefix',
             default='p2ch11',
             help="Data prefix to use for Tensorboard run. Defaults to chapter.",
         )
 
         parser.add_argument('comment',
             help="Comment suffix for Tensorboard run.",
             nargs='?',
             default='dwlpt',
         )
         self.cli_args = parser.parse_args(sys_argv)
         self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
 
         self.trn_writer = None
         self.val_writer = None
         self.totalTrainingSamples_count = 0
 
         self.use_cuda = torch.cuda.is_available()
         self.device = torch.device("cuda" if self.use_cuda else "cpu")
 
         self.model = self.initModel()
         self.optimizer = self.initOptimizer()

    def init_model(self):
        model = LunaModel()
        if self.use_cuda:
            log.info("Using Cuda; {} devices.".format(torch.cuda.device_count()))
        model = model.to(self.device)
        return model
    
    def init_optimizer(self):
        return SGD(self.model.parameters(), lr = 0.001, momentum=0.99)
    
    #initialize training_Data
    def init_train_dl(self):
        train_ds = LunaDataset(val_stride = 10, isValSet_bool=False)
        
        batch_size = self.cli_args.batch_size
        if self.use_cuda :
            batch_size*=torch.cuda.device_count()
            
        train_dl= DataLoader(train_ds,
                             batch_size=batch_size,
                             num_workers=self.cli_args.num_workers,
                             pin_memory = self.use_cuda)
        
        return train_dl
    
    
    #initialize validation_data
    def init_val_dl(self):
        val_ds = LunaDataset(
            val_stride=10,
            isValSet_bool=True,
        )

        batch_size = self.cli_args.batch_size
        if self.use_cuda:
            batch_size *= torch.cuda.device_count()

        val_dl = DataLoader(
            val_ds,
            batch_size=batch_size,
            num_workers=self.cli_args.num_workers,
            pin_memory=self.use_cuda,
        )

        return val_dl

    
        