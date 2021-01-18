# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import namedtuple
import functools
import glob
import os
import csv
import SimpleITK as sitk
import numpy as np
from util import XyzTuple, irc2xyz,xyz2irc
import torch
import torch.cuda
from torch.utils.data import Dataset
import copy

annotations_path = r'E:\Alex Work\Datasets\Luna Dataset\annotations.csv'
candidates_path = r'E:\Alex Work\Datasets\Luna Dataset\candidates.csv'
luna_subsets = r'E:\Alex Work\Datasets\Luna Dataset'

CandidateInfoTuple = namedtuple('CandidateInfoTuple', 'isNodule_bool , diameter_mm, series_uid, center_xyz' )

@functools.lru_cache(1)
def getCandidateInfoList(requireOnDisk_bool = True):
    mhd_list = glob.glob(luna_subsets + "\\"+ "subset*/*.mhd")
    presentOnDisk_set = {os.path.split(p)[-1][:-4] for p in mhd_list}
    
    """
    After we get our candidate information, we want to merge in the diameter information from
    annotations.csv
    """
    diameter_dict = {}
    with open(annotations_path, 'r') as f:
        for row in list(csv.reader(f))[1:]:
            series_uid = row[0]
            annotationCenter_xyz = tuple([float(x) for x in row[1:4]])
            annotationDiameter_mm = float(row[4])
            
            diameter_dict.setdefault(series_uid, []).append((
                annotationCenter_xyz, annotationDiameter_mm))
            
    candidate_info_list = []
    with open(candidates_path,'r') as f:
        for row in list(csv.reader(f))[1:]:
            series_uid = row[0]
            
            if series_uid not in presentOnDisk_set and requireOnDisk_bool:
                continue
            
            isNodule_bool = bool(int(row[4]))
            candidateCenter_xyz = tuple([float(4) for x in row[1:4]])
            
            candidateDiameter_mm = 0.0
            for annotation_tup in diameter_dict.get(series_uid, []):
                annotationCenter_xyz , annotationDiameter_mm = annotation_tup
                for i in range(3):
                    delta_mm = abs(candidateCenter_xyz[i] - annotationCenter_xyz[i])
                    if delta_mm > annotationDiameter_mm / 4:
                        break
                else:
                    candidateDiameter_mm = annotationDiameter_mm
                    break
                        
                candidate_info_list.append(CandidateInfoTuple(isNodule_bool, candidateDiameter_mm, series_uid, candidateCenter_xyz))
    candidate_info_list.sort(reverse = True)
    return candidate_info_list


class Ct:
    def __init__(self, series_uid):
        mhd_path = glob.glob(luna_subsets + "\\"+ "subset*/{}.mhd".format(series_uid))[0]
        
        ct_mhd = sitk.ReadImage(mhd_path)
        self.ct_a = np.array(sitk.GetArrayFromImage(ct_mhd), dtype=np.float32)
        self.ct_a.clip(-1000,1000,self.ct_a)
        #self.hu_a = ct_a
        self.origin_xyz = XyzTuple(*ct_mhd.GetOrigin())
        self.vxSize_xyz = XyzTuple(*ct_mhd.GetSpacing())
        self.direction_a = np.array (ct_mhd.GetDirection()).reshape(3,3)
        
        
    def getRawCandidate(self, center_xyz, width_irc):
        center_irc = xyz2irc(
            center_xyz,
            self.origin_xyz,
            self.vxSize_xyz,
            self.direction_a,
            )
        
        slice_list = []
        for axis, center_val in enumerate(center_irc):
            start_ndx = int(round(center_val - width_irc[axis]/2))
            end_ndx = int(start_ndx + width_irc[axis])
            slice_list.append(slice(start_ndx, end_ndx))
            
        ct_chunk = self.ct_a[tuple(slice_list)]
        return ct_chunk, center_irc
    
@functools.lru_cache(1, typed=True)
def getCt(series_uid):
    return Ct(series_uid)

def getCtRawCandidate(series_uid, center_xyz, width_irc):
    ct = getCt(series_uid)
    ct_chunk, center_irc = ct.getRawCandidate(center_xyz, width_irc)
    return ct_chunk, center_irc


class LunaDataset(Dataset):
    def __init__(self, val_stride =0, isValSet_bool = None, series_uid=None):
        self.candidate_info_list = copy.copy(getCandidateInfoList())
        
        if series_uid:
            self.candidate_info_list = [x for x in self.candidate_info_list if x.series_uid == series_uid]
        
        if isValSet_bool :
            assert val_stride >0
            self.candidate_info_list = self.candidate_info_list[::val_stride]
        elif val_stride > 0:
            del self.candidate_info_list[::val_stride]
        
    def __len__(self):
        return len(self.candidate_info_list)
    
    def __getitem__(self, ndx):
        candidate_info_tup = self.candidate_info_list[ndx]
        width_irc = (32,48,48)
        candidate_a, center_irc = getCtRawCandidate(candidate_info_tup.series_uid, candidate_info_tup.center_xyz, width_irc)
        print(candidate_a)
        candidate_t = torch.from_numpy(candidate_a)
        candidate_t = candidate_t.to(torch.float32)
        candidate_t =candidate_t.unsqueeze(0)
        
        pos_t = torch.tensor([
            not candidate_info_tup.isNodule_bool,
            candidate_info_tup.isNodule_bool],
            dtype = torch.long,)
        
        return (candidate_t, pos_t, candidate_info_tup.series_uid, torch.tensor(center_irc))
    
lista = getCandidateInfoList()



for i in range(140):
    plt.imshow(ct_a[i])
    plt.show()