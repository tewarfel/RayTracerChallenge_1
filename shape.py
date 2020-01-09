import collections
import math
import numpy as np


#cython: linetrace=True
#cython: language_level=3

from memblock import *
#from vec4 import *
#from vec3 import *
from rotations import *
from canvas import *

from base import inverse, transform, dot, Intersection, normalize, World, scaling, EPSILON



class Material(object):
    def __init__(self, material_color, ambient, diffuse, specular, shininess, reflective, transparency,
                 refractive_index, pattern):
        if type(material_color) == Vec3:
           self.color = material_color
        elif type(material_color) == tuple:
           self.color = color(material_color[0], material_color[1], material_color[2])
        else:
            print("unknown color type ", material_color)
            print(type(material_color))
            quit(1)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflective = reflective
        self.transparency = transparency
        self.refractive_index = refractive_index
        self.pattern = pattern

    def __eq__(self, other):
       # if (type(other) != Material) and (type(other) != self.__class__):
       #     print("Error - can only compare a material to another material")
       #     print("type is ", type(other))
       #     print(Material)
       #     print(self.__class__)
       #     assert(False)
        for element in self.__dict__.keys():
            if self.__dict__[element] != other.__dict__[element]:
                return False
        return True


def material(material_color=color(1.0, 1.0, 1.0), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0,
             reflective=0.0, transparency=0.0, refractive_index=1.0, pattern=None):
    return Material(material_color, ambient, diffuse, specular, shininess, reflective, transparency, refractive_index, pattern)




class Shape(object):
    scount = 0
    
    def __init__(self, shape_material=None, shape_transform=None):
        self.origin = point(0, 0, 0)
        
        Shape.scount += 1
        self.instance_id = Shape.scount
        self.saved_ray = None

        if shape_material is None:
            self.material = Material(material_color=color(1.0, 1.0, 1.0), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0,
             reflective=0.0, transparency=0.0, refractive_index=1.0, pattern=None)
        else:
            self.material = shape_material

        if shape_transform is None:
            self.transform = np.identity(4, dtype=float)
            self.inverse_transform = np.identity(4, dtype=float)
        else:
            self.transform = shape_transform
            self.inverse_transform = inverse(shape_transform)

    
    def intersect(self, src_ray):
        local_ray = transform(src_ray, self.inverse_transform)
        return self.local_intersect(local_ray)

    def local_intersect(self, local_ray):
        self.saved_ray = local_ray
        return None

    def set_transform(self, t):
        assert(t.shape == (4, 4))
        self.transform = t
        self.inverse_transform = inverse(t)
        
        
    def normal_at(self, pt):
        [ox,oy,oz,ow] = pt
        local_point = Vec4(np.matmul(self.inverse_transform, np.array([ox,oy,oz,ow], dtype=np.float32)))
        [ox,oy,oz,ow] = self.local_normal_at(local_point)
        wn = np.matmul(np.transpose(self.inverse_transform), np.array([ox,oy,oz,ow], dtype=np.float32))
        m = math.sqrt((wn[0]*wn[0]) + (wn[1]*wn[1]) + (wn[2]*wn[2]))
        s = 1.0 / m
        return vector(s*wn[0], s*wn[1], s*wn[2])

    def local_normal_at(self, local_pt):
        return(vector(local_pt[0], local_pt[1], local_pt[2]))
    
def test_shape():
    return Shape()


class Sphere(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Sphere.scount


    def local_intersect(self, local_ray):
        sphere_to_ray = local_ray.origin - self.origin
        a2 = 2 * dot(local_ray.direction, local_ray.direction)
        b = 2 * dot(local_ray.direction, sphere_to_ray)
        c = dot(sphere_to_ray, sphere_to_ray) - 1
        
        discriminant = (b * b) - (2 * a2 * c)
        if discriminant < 0:
            return ()
        else:
            scale_value = 1.0 / a2
            v = scale_value * np.sqrt(discriminant)
            w = scale_value * b
            t1 = np.float32(-(v + w))
            t2 = np.float32(v - w)
            return (Intersection(t1, self), Intersection(t2, self))
    
    def local_normal_at(self, local_pt):
        obj_nml = local_pt - point(0, 0, 0)  # np.matmul(self.inverse_transform, self.origin)
        return normalize(vector(obj_nml[0], obj_nml[1], obj_nml[2]))


def sphere(sphere_material=None, sphere_transform=None):
    return Sphere(sphere_material, sphere_transform)

def glass_sphere(sphere_material = material(transparency=1.0, refractive_index=1.5), sphere_transform = np.identity(4, dtype=float)):
    return Sphere(sphere_material, sphere_transform)



class Plane(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Sphere.scount
    
    def local_intersect(self, local_ray):
        if abs(local_ray.direction.y) < EPSILON:
            return()
            
        t = np.float32(-local_ray.origin.y / local_ray.direction.y)
        return ([Intersection(t, self)])
    
    def local_normal_at(self, local_pt):
        return vector(0, 1, 0)


def plane(plane_material=None, plane_transform=None):
    return Plane(plane_material, plane_transform)

def set_transform(s, t):
    s.set_transform(t)
    

def intersect(shape, src_ray):
    return shape.intersect(src_ray)


def normal_at(shape, pt):
    return shape.normal_at(pt)


class Point_Light(object):
    # scount = 0
    
    def __init__(self, light_position, light_intensity):
        self.position = light_position
        self.intensity = light_intensity
    
    # Point_Light.scount += 1
    # self.instance_id = Point_Light.scount


def point_light(light_position, light_intensity):
    return Point_Light(light_position, light_intensity)




def default_world():
    new_world = World()
    new_world.light.append(point_light(point(-10.0, 10.0, -10.0), color(1.0, 1.0, 1.0)))
    new_world.objects.append(sphere(sphere_material=material(material_color=color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)))
    new_world.objects.append(sphere(sphere_transform=scaling(0.5, 0.5, 0.5)))
    return new_world