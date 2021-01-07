# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:20:04 2020

@author: Alex
"""

import torch
import torch.nn as nn
from torchvision import models

class MRNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.pretrained_model = models.alexnet(pretrained=True)
        self.pooling_layer = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Linear(256,2)
        
        
    def forward(self, x):
        x = torch.squeeze(x, dim=0) #remove the first dimension and remain with (s,256,256,3)
        features = self.pretrained_model.features(x)
        pooled_features = self.pooling_layer (features)
        pooled_features = pooled_features.view(pooled_features.size(0),-1)
        flattened_features = torch.max(pooled_features, 0 , keepdim = True)[0]
        output = self.classifier(flattened_features)
        
        return output