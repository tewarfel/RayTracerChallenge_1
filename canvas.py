import collections
import math

import numpy as np

import cv2

#cython: linetrace=True
#cython: language_level=3

from vec4 import *
from vec3 import *


class Canvas:
    def __init__(self, width, height, background, data):
        assert (height > 0)
        assert (width > 0)
        self.width = width
        self.height = height
        self.background = background
        self.data = data


    def write_pixel(self, x, y, color_value):
        xi = int(x + 0.5)
        yi = int(y + 0.5)
        if (xi > -1) and (xi < self.width) and (yi > -1) and (yi < self.height):
            self.data[0, yi, xi] = color_value.red
            self.data[1, yi, xi] = color_value.green
            self.data[2, yi, xi] = color_value.blue

    def pixel_at(self, x, y):
        xi = int(x + 0.5)
        yi = int(y + 0.5)
        r = self.data[0, xi, yi]
        g = self.data[1, xi, yi]
        b = self.data[2, xi, yi]
        return(color(r,g,b))
        
    def write_image(self, filename):
        output_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for i in range(3):
           output_array[:,:,2-i] = np.clip((self.data[i,:,:] * 255), 0, 255)
        #cv2.imwrite(filename, output_array[::-1,:])
        cv2.imwrite(filename, output_array)

def canvas(width, height, background = None):
    if background is None:
        background = color(0,0,0)
    width = int(width)
    height = int(height)
    data = np.ndarray((3, height, width), dtype=np.float32)
    data[0, :, :] = background.red
    data[1, :, :] = background.green
    data[2, :, :] = background.blue
    return Canvas(width, height, background, data)


def write_pixel(canvas, x, y, color_value):
    return canvas.write_pixel(x, y, color_value)

def write_image(canvas, filename):
    return canvas.write_image(filename)
    
def pixel_at(canvas, x, y):
    return canvas.pixel_at(x, y)

