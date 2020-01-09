
import numpy as np
from memblock import *
from canvas import *
from shape import material, sphere, test_shape, default_world, point_light, glass_sphere, cube, cylinder, cone, group
from base import ray, refracted_color, intersection, intersections, reflected_color, cofactor, determinant, minor, submatrix, shearing, is_invertible, inverse, hit, EPSILON, equal, World, render, translation, magnitude, normalize, dot, cross, reflect, scaling, view_transform, intersection, intersections, prepare_computations,  world, camera, color, rotation_y, rotation_z, rotation_x


def ensure_context_has_tuple(context):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}


def ensure_context_has_dict(context):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
