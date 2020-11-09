# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:46:54 2020

@author: alexandru.vesa
"""


'''
Singleton is a creational design pattern that lets you ensure that
a class has onyl one instance while providing a global acces point
to this instance'''

class _Tigger : 
    
    def __str__(self):
        return 'im the only one'
    
    def roar(self):
        return 'Grr !'
    
_instance = None

def Tigger():
    global _instance
    if _instance is None:
        _instance = _Tigger()
    return _instance


a= Tigger()
b=Tigger()

print(f'ID(a) = {id(a)}')
print(f'ID(b) = {id(b)}')
print(f'Are they the samge object?  {a is b } ')