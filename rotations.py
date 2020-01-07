import collections
import math

import numpy as np

import cv2

#cython: linetrace=True
#cython: language_level=3

from vec4 import *
from vec3 import *
from canvas import *


# decorator function for memoizing rotation matrices of particular angles
def memoize_rotation_x(f):
    memory = {}
    # This inner function has access to memory
    # and 'f'
    def inner(angle):
        if angle not in memory:
            memory[angle] = f(angle)
        return memory[angle]
    return inner


#@memoize_rotation_x
def rotation_x(angle):
    sine_theta = np.sin(angle)
    cosine_theta = np.cos(angle)
    m = np.identity(4, float)
    m[1,1:3] = [cosine_theta, -sine_theta]
    m[2,1:3] = [sine_theta, cosine_theta]
    return m


def memoize_rotation_y(f):
    memory = {}
    # This inner function has access to memory
    # and 'f'
    def inner(angle):
        if angle not in memory:
            memory[angle] = f(angle)
        return memory[angle]
    return inner

#@memoize_rotation_y
def rotation_y(angle):
    sine_theta = np.sin(angle)
    cosine_theta = np.cos(angle)
    m = np.identity(4, float)
    m[0,0] = cosine_theta
    m[0, 2] = sine_theta
    m[2, 0] = -sine_theta
    m[2, 2] = cosine_theta
    return m


def memoize_rotation_z(f):
    memory = {}
    # This inner function has access to memory
    # and 'f'
    def inner(angle):
        if angle not in memory:
            memory[angle] = f(angle)
        return memory[angle]
    return inner

#memoize_rotation_z
def rotation_z(angle):
    sine_theta = np.sin(angle)
    cosine_theta = np.cos(angle)
    m = np.identity(4, float)
    m[0,0:2] = [cosine_theta, -sine_theta]
    m[1,0:2] = [sine_theta, cosine_theta]
    return m

