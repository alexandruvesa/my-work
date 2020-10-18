# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:08:03 2020

@author: alexandru.vesa
"""

import sys
from collections import defaultdict
import itertools as it


#Find the duplicates in the string
string = "aaaaaanncsscs"
duplicates = len(set(string))


#Calculate the sum of the first 1000 numbers
suma = sum ( i for i in range(1001))
#Calculate the memory
sys.getsizeof(suma)


#default dict
dictionary = { "Alex" : [40,20] , "Ionut" : [10,20]}
studentGrade = defaultdict(list, dictionary)

def setGradeBest(name, score):
    studentGrade[name].append(score)
    
setGradeBest('Ion', 200)


#Use itertools to get pow of numbers
powers = list(map(pow, range(1000000), it.repeat(0)))