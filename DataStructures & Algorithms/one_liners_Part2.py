# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:07:36 2021

@author: Alex
"""

import numpy as np


a = np.array([[0,1,2,3],
              [4,5,6,7],
              [8,9,10,11],
              [12,13,14,15]])


b = a[2,:]



X = np.array([[1,0,0],
              [0,2,2],
              [3,0,0]])

print(np.nonzero(X))



#Find the cities with above average pollution peaks from a set of data
X = np.array(
    [[42,40,41,43,44,43],
     [30,31,29,29,29,30],
     [8,13,31,11,11,9],
     [11,11,12,13,11,12]])

cities = np.array(["Hong Knong", "New York", "Berlin", "Romania"])

polluted = set(cities[np.nonzero(X > np.average(X))[0]])



inst = np.array([[232,'@tata'],
                 [133,"ion"]])


superstars = inst[inst[:,0].astype(float)>100]



tmp = np.array([1,2,3,4,3,4,4,5,3,3,4,3,4,6,6,5,5,5,4,5,5])

tmp_indexed = tmp[6::7]

np.where(tmp = tmp_indexed)



sat_scores = np.array([1100, 1256, 1543, 1043,989, 1412, 1343])
students = np.array(["John", "Bob", "joe", "jane", "frank", "carl","alex"])

top_students = students[np.argsort(sat_scores)][:-4:-1]



books = np.array([["Coffee Break Numpy", 4.6],
                  ["Lord of the Rings", 5.0],
                  ["Harry Potter", 4.3],
                  ['Winnie', 3.9],
                  ['Clown', 2.2],
                  ['Coffee Break Python', 4.7]])

filter_books = lambda x,y : x[x[:,1].astype(float)>y]



basket = np.array([[0, 1, 1, 0],
[0, 0, 0, 1],
[1, 1, 0, 0],
[0, 1, 1, 1],
[1, 1, 1, 0],
[0, 1, 1, 0],
[1, 1, 0, 1],
[1, 1, 1, 1]])

columns_ebook = basket[:,2:]
logical_op = np.all(columns_ebook, axis = 1)













## Data: row is customer shopping basket
## row = [course 1, course 2, ebook 1, ebook 2]
## value 1 indicates that an item was bought.
basket = np.array(
[[0, 1, 1, 0],
[0, 0, 0, 1],
[1, 1, 0, 0],
[0, 1, 1, 1],
[1, 1, 1, 0],
[0, 1, 1, 0],
[1, 1, 0, 1],
[1, 1, 1, 1]])


