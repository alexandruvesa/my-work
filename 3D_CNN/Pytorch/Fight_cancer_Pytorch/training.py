# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 15:28:44 2020

@author: 40737
"""
import sys
import argparse
import datetime
import parse
import torch
from data_prep import LunaDataset

class LunaTrainingApp:
    def __init__(self, sys_argv=None):
        if sys_argv is None :
            sys_argv = sys.argv[1:]
            
        parser = argparse.ArgumentParser()
        parser.add_argument("--num-workers",
                            help = 'number of worker process for background data loading',
                            default =8,
                            type = int,
                            )
        
        self.cli_args = parse.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        
        self.model = self.initModel()
        self.optimizer = self.initOptimizer()
        
        def initModel(self):
            model = LunaModel()
            if self.use_cuda:
                log.info("Using Cuda; {} devices.".format(torch.cuda.device_count()))
                if torch.cuda.device_count() > 1:
                    model = nn.DataParallel(model)
                model = model.to(self.device)
            return model
        
        def initOptimizer(self):
            return SGD(self.model.parameters(), lr=0.001, momentum = 0.99)
        
        def initTrainDl(self):
            train_ds = LunaDataset(
                val_stride = 10,
                isValSet_bool = False,)
            
            batch_size = self.cli_args.batch_size
            if self.use_cuda:
                batch_size *= torch.cuda.device_count()
            
            train_dl = DataLoader(
                train_ds,
                batch_size = batch_size,
                num_workers = self.cli_args.num_workers,
                pin_memory = self.use_cuda,)
            
            return train_dl
        
 