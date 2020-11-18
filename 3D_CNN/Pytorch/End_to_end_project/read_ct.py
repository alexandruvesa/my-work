# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:54:51 2020

@author: alexandru.vesa
"""
import SimpleITK as sitk
import glob
import numpy as np
import collections
from util import xyz2irc


XyzTuple = collections.namedtuple('XyzTuple', ['x','y', 'z'])

class Ct:
    def __init__(self, series_uid):
        mhd_path = glob.glob(r'C:\Users\alexandru.vesa\Downloads\Luna_dataset\subset*/*/{}.mhd'.format(series_uid))

        ct_mhd = sitk.ReadImage(mhd_path)
        ct_a = np.array(sitk.GetArrayFromImage(ct_mhd), dtype = np.float32)
        ct_a.clip(-1000,1000,ct_a)
        self.origin_xyz = XyzTuple(*ct_mhd.GetOrigin())
        self.vxSize_xyz = XyzTuple(*ct_mhd.GetSpacing())
        self.direction_a = np.array(ct_mhd.GetDirection()).reshape(3, 3)
        
        
    def getRawCandidate(self, center_xyz, width_irc):
        center_irc = xyz2irc(
            center_xyz,
            self.origin_xyz,
            self.vxSize_xyz,
            self.direction_a)
        
        slice_list = []
        
        for axis, center_val in enumerate(center_irc):
            start_ndx = int(round(center_val - width_irc[axis]/2))
            end_ndx = int(start_ndx + width_irc[axis])
            slice_list.append(slice(start_ndx, end_ndx))
            
        ct_chunk = self.hu_a[tuple(slice_list)]
        return ct_chunk, center_irc
    
    def __len__(self):
        return len(self.candidateInfo_list)
    
    def __getitem__(self, ndx):
        candidateInfo_tup = self.candidateInfo_list[ndx]
        width_irc = (32,48,48)
        
        candidate_a, center_irc = getCtRawCandidate(
            candidateInfo_tup.series_uid,
            candidateInfo_tup.center_xyz,
            width_irc,)
        