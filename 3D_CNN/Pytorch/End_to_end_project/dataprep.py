# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 00:39:38 2020

@author: alexandru.vesa
"""

from collections import namedtuple
import functools
import glob
import os
import csv

candidates_path = r'C:\Users\alexandru.vesa\Downloads\Luna_dataset\candidates.csv'
annotations_path = r'C:\Users\alexandru.vesa\Downloads\Luna_dataset\annotations.csv'

CandidateInfoTuple = namedtuple(
    'CandidateInfoTuple',
    'isNodule_bool, diameter_mm, series_uid, center_xyz',
    )

@functools.lru_cache(1)
def getCandidateInfoList(requiredOnDisk_bool = True):
    mhd_list = glob.glob(r'C:\Users\alexandru.vesa\Downloads\Luna_dataset\subset*/*.mhd')
    presentOnDisk_set = {os.path.split(p)[-1][:-4] for p in mhd_list}
    
    diameter_dict = {}
    with open(annotations_path, 'r') as f:
        for row in list(csv.reader(f))[1:]:
            series_uid = row[0]
            annotationsCenter_xyz= tuple([float(x) for x in row[1:4]])
            annotationDiameter_mm = float(row[4])
            
            diameter_dict.setdefault(series_uid, []).append(
                (annotationsCenter_xyz, annotationDiameter_mm)
            )
            
    candidateInfo_list = []
    with open(candidates_path, 'r') as f:
        for row in list(csv.reader(f))[1:]:
            series_uid = row[0]
            
            if series_uid not in presentOnDisk_set and requiredOnDisk_bool:
                continue
            
            isNodule_bool = bool(int(row[4]))
            cadidateCenter_xyz = tuple([float(x) for x in row[1:4]])
            
            candidateDiameter_mm = 0.0
            
            for annotation_tup in diameter_dict.get(series_uid,[]):
                annotationsCenter_xyz, annotationDiameter_mm = annotation_tup
                for i in range(3):
                    delta_mm = abs(cadidateCenter_xyz[i] - annotationsCenter_xyz[i])
                    if delta_mm > annotationDiameter_mm / 4:
                        break
                    else:
                        candidateDiameter_mm = annotationDiameter_mm
                        break
            
            candidateInfo_list.append(CandidateInfoTuple(
                isNodule_bool,
                candidateDiameter_mm,
                series_uid,
                cadidateCenter_xyz,
                ))
            
            candidateInfo_list.sort(reverse = True)
            
    return candidateInfo_list

candidateInfo_list=getCandidateInfoList()