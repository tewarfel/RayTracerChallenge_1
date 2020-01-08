import collections
import math
import numpy as np


#cython: linetrace=True
#cython: language_level=3

from vec4 import *



    
class Vec3(collections.namedtuple('Vec3','red green blue')):
#    cdef int active_count
#    cdef int total_used
#    cdef int max_active
#    cdef float EPSILON
    
    active_count = 0
    total_used = 0
    max_active = 0

    EPSILON = 0.00005
    
    def __init__(self, r, g, b):
        self.value = collections.namedtuple('Vec3', 'red green blue')(r, g, b)
        Vec3.active_count += 1
        Vec3.total_used += 1
        if Vec3.active_count > Vec3.max_active:
            Vec3.max_active = Vec3.active_count

        
    def __del__(self):
        Vec3.active_count -= 1


    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.value.red + other.red,
                        self.value.green + other.green,
                        self.value.blue + other.blue)
        else:
            print("__add__ in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)


    def __mul__(self, other):
        if isinstance(other, int):
            return Vec3(self.value.red * other,
                        self.value.green * other,
                        self.value.blue * other)
        elif isinstance(other, float):
            return Vec3(self.value.red * other,
                        self.value.green * other,
                        self.value.blue * other)
        elif str(type(other))=="<class 'vec3.Vec3'>":
            return Vec3(self.value.red * other.red,
                        self.value.green * other.green,
                        self.value.blue * other.blue)
        else:
            print("__mul__ in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)


    def __rmul__(self, other):
        if isinstance(other, int):
            return Vec3(self.value.red * other,
                        self.value.green * other,
                        self.value.blue * other)
        elif isinstance(other, float):
            return Vec3(self.value.red * other,
                        self.value.green * other,
                        self.value.blue * other)
        elif str(type(other))=="<class 'vec3.Vec3'>":
            return Vec3(self.value.red * other.red,
                        self.value.green * other.green,
                        self.value.blue * other.blue)
        else:
            print("__rmul__ in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(self.value.red / other,
                        self.value.green / other,
                        self.value.blue / other)
                                                           
        else:
            print("__truediv__ in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)

    def __sub__(self, other):
        return Vec3(self.value.red - other.red,
                    self.value.green - other.green,
                    self.value.blue - other.blue)
                                                         

    def __neg__(self):
        return Vec3(-self.value.red,
                    -self.value.green,
                    -self.value.blue)

    def __eq__(self, other):
        if str(type(other))=="<class 'vec3.Vec3'>":
            for i1 in range(3):
                n = self.value[i1]
                m = other[i1]
                delta = (n - m) if n > m else (m - n)
                if delta > Vec3.EPSILON:
                    return False
            return True
        else:
            print("other is not a Vec3.")
        return False

    def mag_squared(self):
#        cdef float x, y, z
        x = self.value.red
        y = self.value.green
        z = self.value.blue
        return (((x * x) + (y * y)) + ((z * z)))

    def magnitude(self):
        return np.sqrt(self.mag_squared())

    def dot_prod(self, other):
        if isinstance(other, Vec4):
            return ((self.value.red * other.red) + (self.value.green * other.green) + (self.value.blue * other.blue))
            
        else:
            print("illegal argument for dot-product")
            print("dot_prod in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)

    def cross_prod(self, other):
        if isinstance(other, Vec4):
            return (Vec3((self.value.green * other.blue) - (self.value.blue * other.green),
                         (self.value.blue * other.red) - (self.value.red * other.blue),
                         (self.value.red * other.green) - (self.value.green * other.red)))
        else:
            print("illegal argument for cross-product")
            print("cross_prod in Vec3 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)


def vec3(x, y, z):
    return (Vec3(x, y, z))

def color(red,  green, blue):
    return (Vec3(red, green, blue))

