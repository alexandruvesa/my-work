# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 05:40:27 2021

@author: Alex
"""

"""
Useful definitions for layers used in this implementation:

Unpooling layer
During the pooling operation, create a matrix which record the location of the maximum value, 
unpool operation will insert the pooled value in the original place, with the remaining elements being set to zero.
Unpooling captures example-specific structures by tracing the original locations with strong activations back to image space.
As a result, it effectively reconstructs the detailed structure.

"""


from collections import OrderedDict
import torch
import torch.nn as nn
import torchvision.models as models

F = nn.functional
DEBUG = False

vgg16_dims = [
                    (64, 64, 'M'),                                # Stage - 1
                    (128, 128, 'M'),                              # Stage - 2
                    (256, 256, 256,'M'),                          # Stage - 3
                    (512, 512, 512, 'M'),                         # Stage - 4
                    (512, 512, 512, 'M')                          # Stage - 5
            ]

decoder_dims = [
                    ('U', 512, 512, 512),                         # Stage - 5
                    ('U', 512, 512, 512),                         # Stage - 4
                    ('U', 256, 256, 256),                         # Stage - 3
                    ('U', 128, 128),                              # Stage - 2
                    ('U', 64, 64)                                 # Stage - 1
                ]



class SegNet(nn.Module):
    def __init__(self, input_channels, output_channels):
        super(SegNet, self).__init__()
        
        self.input_channels = input_channels
        self.output_channels = output_channels
        
        self.num_channels = input_channels
        
        self.vgg16 = models.vgg16(pretrained = True)
        
        #Encoder layers
        
        self.encoder_conv_00 = self.conv_block(input_channels = self.input_channels, output_channels = 64,
                                          kernel_size = 3,
                                          padding = 1)
        
        self.encoder_conv_01 = self.conv_block(input_channels = 64 , output_channels = 64,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_02 = self.conv_block(input_channels = 64 , output_channels = 128,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_03 = self.conv_block(input_channels = 128 , output_channels = 128,
                                               kernel_size = 3,
                                               padding = 1)
        
        
        self.encoder_conv_04 = self.conv_block(input_channels = 128 , output_channels = 256,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_05 = self.conv_block(input_channels = 256 , output_channels = 256,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_06 = self.conv_block(input_channels = 256 , output_channels = 256,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_07 = self.conv_block(input_channels = 256 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_08 = self.conv_block(input_channels = 512 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
        
          
        self.encoder_conv_09 = self.conv_block(input_channels = 512 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
        
          
        self.encoder_conv_10 = self.conv_block(input_channels = 512 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
          
        self.encoder_conv_11 = self.conv_block(input_channels = 512 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
        
          
        self.encoder_conv_12 = self.conv_block(input_channels = 512 , output_channels = 512,
                                               kernel_size = 3,
                                               padding = 1)
        
          

        
        #self.init_vgg_weights()
        
        
    
        #Decoder layers
        
        
        
        self.decoder_convtr_12 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 512,
                                                               kernel_size = 3,
                                                               padding = 1)
                
        
        self.decoder_convtr_11 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 512,
                                                               kernel_size = 3,
                                                               padding = 1)
       
        self.decoder_convtr_10 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 512,
                                                               kernel_size = 3,
                                                               padding = 1)
                        
        self.decoder_convtr_09 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 512,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        self.decoder_convtr_08 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 512,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        self.decoder_convtr_07 = self.conv_transpose_2d_block(input_channels = 512, output_channels = 256,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        self.decoder_convtr_06 = self.conv_transpose_2d_block(input_channels = 256, output_channels = 256,
                                                               kernel_size = 3,
                                                               padding = 1)        
        
        self.decoder_convtr_05 = self.conv_transpose_2d_block(input_channels = 256, output_channels = 256,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        
        self.decoder_convtr_04 = self.conv_transpose_2d_block(input_channels = 256, output_channels = 128,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        
                
        self.decoder_convtr_03 = self.conv_transpose_2d_block(input_channels = 128, output_channels = 128,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        
                
        self.decoder_convtr_02 = self.conv_transpose_2d_block(input_channels = 128, output_channels = 64,
                                                               kernel_size = 3,
                                                               padding = 1)
        
                
        self.decoder_convtr_01 = self.conv_transpose_2d_block(input_channels = 64, output_channels = 64,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        
                
        self.decoder_convtr_00 = self.conv_transpose_2d_block(input_channels = 64, output_channels = self.output_channels,
                                                               kernel_size = 3,
                                                               padding = 1)
        
        
    
        
    #Use Sequential to couple layers to form a single block. Clean code, reusable purpose    
    def conv_block(self,input_channels = None, output_channels = None, *args, **kwargs):
        return nn.Sequential(
            nn.Conv2d(input_channels, output_channels, *args, **kwargs),
            nn.BatchNorm2d(output_channels),
            nn.ReLU())
            
    def conv_transpose_2d_block(self, input_channels = None, output_channels = None, *args, **kwargs):
        return nn.Sequential(
            nn.ConvTranspose2d(in_channels = input_channels, out_channels = output_channels,*args,**kwargs),
            nn.BatchNorm2d(output_channels),
            nn.ReLU())
        
    
    
    def forward(self, input_img):
        
        #Encoder stage_1
        dim_0 = input_img.size()
        x_00 = self.encoder_conv_00(input_img)
        x_01 = self.encoder_conv_01(x_00)
        #Retain indices from the where are the values resulted from MaxPooling
        x_0 , indices_0 = F.max_pool2d(x_01, kernel_size = 2, stride=2, return_indices = True)
        
        #Encoder stage_2
        dim_1 = x_0.size()
        x_02 = self.encoder_conv_02(x_0)
        x_03 = self.encoder_conv_03(x_02)
        x_1, indices_1 = F.max_pool2d(x_03, kernel_size = 2, stride =2 ,return_indices = True)
        
        #Encoder stage_3
        dim_2 = x_1.size()
        x_04 = self.encoder_conv_04(x_1)
        x_05 = self.encoder_conv_05(x_04)
        x_06 = self.encoder_conv_06(x_05)
        x2, indices_2 = F.max_pool2d(x_06, kernel_size = 2 , stride = 2, return_indices = True)
        
        #Encoder stage_4
        dim_3 = x2.size()
        x_07 = self.encoder_conv_07(x2)
        x_08 = self.encoder_conv_08(x_07)
        x_09 = self.encoder_conv_09(x_08)
        x3, indices_3 = F.max_pool2d(x_09, kernel_size = 2 , stride = 2, return_indices = True)
        
        #Encoder stage_5
        dim_4 = x3.size()
        x_10 = self.encoder_conv_10(x3)
        x_11 = self.encoder_conv_11(x_10)
        x_12 = self.encoder_conv_12(x_11)
        x4, indices_4 = F.max_pool2d(x_12, kernel_size = 2 , stride = 2, return_indices = True)
        
        
        #Decoder stage_5
        x_12d = F.max_unpool2d(x4,indices_4, kernel_size = 2, stride =2, output_size=dim_4)
        x_11d = self.decoder_convtr_12(x_12d)
        x_10d = self.decoder_convtr_11(x_11d)
        x_9d= self.decoder_convtr_10(x_10d)
        dim_4d = x_9d.size()
        
        #Decoder stage_4
        x_8d = F.max_unpool2d(x_9d,indices_3, kernel_size = 2, stride =2, output_size=dim_3)
        x_7d = self.decoder_convtr_09(x_8d)
        x_6d = self.decoder_convtr_08(x_7d)
        x_5d= self.decoder_convtr_07(x_6d)
        dim_3d = x_5d.size()
        
        
        #Decoder stage_3
        x_4d = F.max_unpool2d(x_5d,indices_2, kernel_size = 2, stride =2, output_size=dim_2)
        x_3d = self.decoder_convtr_06(x_4d)
        x_2d = self.decoder_convtr_05(x_3d)
        x_1d= self.decoder_convtr_04(x_2d)
        dim_2d = x_1d.size()
        
        #Decode state12
        x_0d = F.max_unpool2d(x_1d,indices_1, kernel_size = 2, stride =2, output_size=dim_1)
        x_00d = self.decoder_convtr_03(x_0d)
        x_01d = self.decoder_convtr_02(x_00d)
        dim_1d = x_01d.size()
        
        
        #Decode stage_1
        x_00d = F.max_unpool2d(x_01d, indices_0, kernel_size=2,stride = 2, output_size = dim_0)
        x_001d=self.decoder_convtr_01(x_00d)
        x_002d=self.decoder_convtr_00(x_001d)
        
        x_softmax = F.softmax(x_002d, dim=1)
        
        
        
        if DEBUG:
            print("dim_0: {}".format(dim_0))
            print("dim_1: {}".format(dim_1))
            print("dim_2: {}".format(dim_2))
            print("dim_3: {}".format(dim_3))
            print("dim_4: {}".format(dim_4))

            print("dim_4d: {}".format(dim_4d))
            print("dim_3d: {}".format(dim_3d))
            print("dim_2d: {}".format(dim_2d))
            print("dim_1d: {}".format(dim_1d))


        return x_00d, x_softmax

     
model = SegNet(3, 3) 
x= torch.rand(1,3,256,256)
y = model(x)
import torchviz
torchviz.make_dot(y,params = dict(model.named_parameters()))     
        