# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 11:05:00 2020

@author: alexandru.vesa
"""


# === abstract shape classes ===
class Shape2DInterface:
    def draw(self): pass

class Shape3DInterface:
    def build(self): pass

# === concrete shpe classes ===
class Circle(Shape2DInterface):
    def draw(self):
        print("Circle.draw")
        
class Square(Shape2DInterface):
    def draw(self):
        print("Square.draw")
        
class Cube(Shape3DInterface):
    def draw(self):
        print("Cube.draw")
        
# === Abstract shape factory ===
class ShapeFactoryInterface:
    def getShape(sides): pass

# ===Concrete shape factories ===
class Shape2DFactory(ShapeFactoryInterface):
    @staticmethod
    def getShape(sides):
        if sides == 1:
            return Circle()
        if sides ==4:
            return Square
        assert 0, "Bad 2D shape creation: shape not defined for " +sides +'sides'
        
        
a = Shape2DFactory()
