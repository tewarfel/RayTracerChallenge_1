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

from base import inverse, transform, dot, Intersection, normalize, World, scaling, EPSILON, equal



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
        self.parent = None
        self.name = "base class"

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
        
        
    def old_normal_at(self, pt):
        [ox,oy,oz,ow] = pt
        local_point = Vec4(np.matmul(self.inverse_transform, np.array([ox,oy,oz,ow], dtype=np.float32)))
        [ox,oy,oz,ow] = self.local_normal_at(local_point)
        wn = np.matmul(np.transpose(self.inverse_transform), np.array([ox,oy,oz,ow], dtype=np.float32))
        m = math.sqrt((wn[0]*wn[0]) + (wn[1]*wn[1]) + (wn[2]*wn[2]))
        s = 1.0 / m
        return vector(s*wn[0], s*wn[1], s*wn[2])


    def world_to_object(self, point):
        if self.parent is None:
            return Vec4(np.matmul(self.inverse_transform, point, dtype=np.float32))
        else:
            return np.matmul(self.inverse_transform, self.parent.world_to_object(point), dtype=np.float32)


    def normal_to_world(self, normal_vector):
        transformed_normal = Vec4(np.matmul(np.transpose(self.inverse_transform), normal_vector, dtype=np.float32))
        transformed_normal[3] = 0
        normalized_transform = transformed_normal.normalize()
        if self.parent is None:
            return normalized_transform
        else:
            return self.parent.normal_to_world(normalized_transform)


    def normal_at(self, world_point):
        return self.normal_to_world( self.local_normal_at( self.world_to_object(world_point) ))
        
        
        
    #    [ox,oy,oz,ow] = pt
    #    local_point = Vec4(np.matmul(self.inverse_transform, np.array([ox,oy,oz,ow], dtype=np.float32)))
    #    [ox,oy,oz,ow] = self.local_normal_at(local_point)
    #    wn = np.matmul(np.transpose(self.inverse_transform), np.array([ox,oy,oz,ow], dtype=np.float32))
    #    m = math.sqrt((wn[0]*wn[0]) + (wn[1]*wn[1]) + (wn[2]*wn[2]))
    #    s = 1.0 / m
    #    return vector(s*wn[0], s*wn[1], s*wn[2])



    def local_normal_at(self, local_pt):
        return(vector(local_pt[0], local_pt[1], local_pt[2]))
    
def test_shape():
    return Shape()


class Sphere(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Sphere.scount
        self.name = "Sphere"

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
        self.instance_id = Plane.scount
        self.name = "Plane"
    
    def local_intersect(self, local_ray):
        if abs(local_ray.direction.y) < EPSILON:
            return()
            
        t = np.float32(-local_ray.origin.y / local_ray.direction.y)
        return ([Intersection(t, self)])
    
    def local_normal_at(self, local_pt):
        return vector(0, 1, 0)


def plane(plane_material=None, plane_transform=None):
    return Plane(plane_material, plane_transform)


class Cube(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Cube.scount
        self.name = "Cube"
    
    def check_axis(self, origin, direction):
        tmin_numerator = (-1 - origin)
        tmax_numerator = (1 - origin)
        
        if abs(direction) >= EPSILON:
            tmin = (tmin_numerator / direction)
            tmax = (tmax_numerator / direction)
        else:
            tmin = tmin_numerator * 1.0e12
            tmax = tmax_numerator * 1.0e12
        if tmin > tmax:
            return(tmax, tmin)
        else:
            return(tmin, tmax)

    
    def local_intersect(self, local_ray):
        xtmin, xtmax = self.check_axis(local_ray.origin.x, local_ray.direction.x)
        ytmin, ytmax = self.check_axis(local_ray.origin.y, local_ray.direction.y)
        ztmin, ztmax = self.check_axis(local_ray.origin.z, local_ray.direction.z)

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)
        
        if tmin>tmax:
            return []
        return [Intersection(tmin, self), Intersection(tmax, self)]

    
    def local_normal_at(self, local_pt):
        maxc = max(np.abs(local_pt.x), np.abs(local_pt.y), np.abs(local_pt.z))
        if maxc == np.abs(local_pt.x):
            return(vector(local_pt.x, 0, 0))
        elif maxc == np.abs(local_pt.y):
            return vector(0, local_pt.y, 0)
        return vector(0, 0, local_pt.z)

def cube(cube_material=None, cube_transform=None):
    return Cube(cube_material, cube_transform)


class Cylinder(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Cylinder.scount
        self.minimum = -1.0e10
        self.maximum = 1.0e10
        self.closed = False
        self.name = "Cylinder"
    
    def check_axis(self, origin, direction):
        tmin_numerator = (-1 - origin)
        tmax_numerator = (1 - origin)
        
        if abs(direction) >= EPSILON:
            tmin = (tmin_numerator / direction)
            tmax = (tmax_numerator / direction)
        else:
            tmin = tmin_numerator * 1.0e12
            tmax = tmax_numerator * 1.0e12
        if tmin > tmax:
            return (tmax, tmin)
        else:
            return (tmin, tmax)
    
    def check_cap(self, local_ray, t):
        x = local_ray.origin.x + (t * local_ray.direction.x)
        z = local_ray.origin.z + (t * local_ray.direction.z)
        return ((x*x) + (z*z)) <= 1
    
    
    def intersect_caps(self, local_ray):
        xs = []
        if self.closed==True and not equal(local_ray.direction.y, 0):
            #check for an intersection with the lower end cap by intersecting the ray with the plane at y=cyl.minimum
            t = (self.minimum - local_ray.origin.y) / local_ray.direction.y
            if self.check_cap(local_ray, t):
                xs.append(Intersection(t, self))
                #print("--intersected a cap")
                
            #check for an intersection with the upper end cap by intersecting the ray with the plane at y=cyl.maximum
            t = (self.maximum - local_ray.origin.y) / local_ray.direction.y
            if self.check_cap(local_ray, t):
                xs.append(Intersection(t, self))
                #print("--intersected a cap")
        return xs
    
    
    def local_intersect(self, local_ray):
        xs = []
        dx = local_ray.direction.x
        dz = local_ray.direction.z
        
        a = (dx*dx)+(dz*dz)
        if a > (EPSILON):
            e2 = (EPSILON / 2) if self.closed else 0
            #print("--ray not parallel to Y axis")
            rx = local_ray.origin.x
            rz = local_ray.origin.z
         
            b = np.float32(2 * ((rx * dx) + (rz * dz)))
            c = np.float32((rx*rx) + (rz*rz) - 1)
            disc = (b*b) - (4*a*c)
            if disc >= 0:
                #print("-- ray may intersect wall of cylinder")
                ds = np.float32(math.sqrt(disc))
                scale_factor = np.float32(1.0/(2 * a))
                t0 = -scale_factor * (ds+b)
                t1 = scale_factor * (ds-b)
                if t0 > t1:
                    temp = t0
                    t0 = t1
                    t1 = temp
                y0 = local_ray.origin.y + (t0 * local_ray.direction.y)
                #print("self.min, y0, self.max, y0: ", self.minimum, y0, self.maximum)
                if (self.minimum - e2) < y0 and y0 < (self.maximum + e2):
                    xs.append(Intersection(np.float32(t0), self))
                    #print("-- ray intersects wall of cylinder")
                   
                y1 = local_ray.origin.y + (t1 * local_ray.direction.y)
                #print("self.min, y1, self.max, y1: ", self.minimum, y1, self.maximum)
                if (self.minimum-e2) < y1  and y1 < (self.maximum + e2):
                    xs.append(Intersection(np.float32(t1), self))
                    #print("-- ray intersects wall of cylinder")
            #else:
                #print("-- ray will NOT intersect wall of cylinder")

        #else:
            #print("-- ray IS parallel to Y axis")
        cap_intersects = self.intersect_caps(local_ray)
        for item in cap_intersects:
            xs.append(item)
            
        return xs
    
    
    def local_normal_at(self, local_pt):
        # assume that local point _is_ on border of cylinder
        x = local_pt.x
        z = local_pt.z
        
        if not self.closed:
            # then point must be on the wall of cylinder
            return vector(x, 0, z)
        
        else:
            # need to figure out if we point is on wall or on edge
            # is it an end?
            y = local_pt.y
            if equal(y, self.minimum):
                # lower end
                return vector(0, -1, 0)
            elif equal(y, self.maximum):
                return vector(0, 1, 0)
            else:
                # assert(equal((x*x)+(z*z), 1))
                # assume is on wall
                return vector(x, 0, z)
            

def cylinder(cylinder_material=None, cylinder_transform=None):
    return Cylinder(cylinder_material, cylinder_transform)


class Cone(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Cone.scount
        self.minimum = -1.0e10
        self.maximum = 1.0e10
        self.closed = False
        self.name = "Cone"
    
    def check_axis(self, origin, direction):
        tmin_numerator = (-1 - origin)
        tmax_numerator = (1 - origin)
        
        if abs(direction) >= EPSILON:
            tmin = (tmin_numerator / direction)
            tmax = (tmax_numerator / direction)
        else:
            tmin = tmin_numerator * 1.0e12
            tmax = tmax_numerator * 1.0e12
        if tmin > tmax:
            return (tmax, tmin)
        else:
            return (tmin, tmax)
    
    def check_cap(self, local_ray, t):
        x = local_ray.origin.x + (t * local_ray.direction.x)
        y = local_ray.origin.y + (t * local_ray.direction.y)
        z = local_ray.origin.z + (t * local_ray.direction.z)
        return ((x * x) + (z * z)) <= (y*y)
    
    def intersect_caps(self, local_ray):
        xs = []
        if self.closed == True and not equal(local_ray.direction.y, 0):
            # check for an intersection with the lower end cap by intersecting the ray with the plane at y=cyl.minimum
            t = (self.minimum - local_ray.origin.y) / local_ray.direction.y
            if self.check_cap(local_ray, t):
                xs.append(Intersection(t, self))

            # check for an intersection with the upper end cap by intersecting the ray with the plane at y=cyl.maximum
            t = (self.maximum - local_ray.origin.y) / local_ray.direction.y
            if self.check_cap(local_ray, t):
                xs.append(Intersection(t, self))

        return xs
    
    def local_intersect(self, local_ray):
        xs = []
        [dx, dy, dz, dw] = local_ray.direction
        [ox, oy, oz, ow] = local_ray.origin
        
        a = (dx * dx) + (dz * dz) - (dy*dy)
        b = 2 * ((ox*dx) + (oz*dz) - (oy*dy))
        c = ((ox*ox) + (oz*oz) - (oy*oy))
        if math.fabs(a) > (EPSILON):
            # a is not zero
            e2 = (EPSILON / 2) if self.closed else 0

            disc = (b * b) - (4 * a * c)

            if (disc + EPSILON) >=0:
                if disc<0:
                    disc=0
                ds = np.float32(math.sqrt(disc))
                scale_factor = np.float32(1.0 / (2 * a))
                t0 = -scale_factor * (ds + b)
                t1 = scale_factor * (ds - b)
                if t0 > t1:
                    temp = t0
                    t0 = t1
                    t1 = temp
                y0 = local_ray.origin.y + (t0 * local_ray.direction.y)
                if (self.minimum - e2) < y0 and y0 < (self.maximum + e2):
                    xs.append(Intersection(np.float32(t0), self))

                
                y1 = local_ray.origin.y + (t1 * local_ray.direction.y)
                if (self.minimum - e2) < y1 and y1 < (self.maximum + e2):
                    xs.append(Intersection(np.float32(t1), self))



        else:
            # a is approximately zero
            if math.fabs(b) > EPSILON:
                # b is non-zero
                t = np.float32(-c / (2*b))
                xs.append(Intersection(t, self))

        if self.closed:
            cap_intersects = self.intersect_caps(local_ray)
            for item in cap_intersects:
                xs.append(item)

        return xs
    
    def local_normal_at(self, local_pt):
        x = local_pt.x
        y = local_pt.y
        z = local_pt.z
        dist2 = ((x*x) + (z*z))
        
        if dist2 < 1:
            if y >= (self.maximum - EPSILON):
                return vector(0,1,0)
            elif y<= (self.minimum + EPSILON):
                return vector(0, -1, 0)
 
        new_y = math.sqrt(dist2)
        if y > 0:
            new_y = -new_y
        return vector(x, new_y, z)
        
        


def cone(cone_material=None, cone_transform=None):
    return Cone(cone_material, cone_transform)


class Group(Shape):
    def __init__(self, shape_material=None, shape_transform=None):
        super().__init__(shape_material, shape_transform)
        self.origin = point(0, 0, 0)
        self.instance_id = Group.scount
        self.name = "Group"
        self.members = []

    def check_axis(self, origin, direction):
        tmin_numerator = (-1 - origin)
        tmax_numerator = (1 - origin)
    
        if abs(direction) >= EPSILON:
            tmin = (tmin_numerator / direction)
            tmax = (tmax_numerator / direction)
        else:
            tmin = tmin_numerator * 1.0e12
            tmax = tmax_numerator * 1.0e12
        if tmin > tmax:
            return (tmax, tmin)
        else:
            return (tmin, tmax)


    def local_intersect(self, local_ray):
        xs=[]
        for member in self.members:
            found = member.intersect(local_ray)
            for i in found:
                if i not in xs:
                    xs.append(i)

        sorted_by_t = sorted(xs, key=lambda tup: tup.__dict__['t'])
        xs = None
        return sorted_by_t



    def local_normal_at(self, local_pt):
        maxc = max(np.abs(local_pt.x), np.abs(local_pt.y), np.abs(local_pt.z))
        if maxc == np.abs(local_pt.x):
            return (vector(local_pt.x, 0, 0))
        elif maxc == np.abs(local_pt.y):
            return vector(0, local_pt.y, 0)
        return vector(0, 0, local_pt.z)

    
    def add_child(self, other):
        other.parent=self
        self.members.append(other)


def group(group_material=None, group_transform=None):
    return Group(group_material, group_transform)


def set_transform(s, t):
    s.set_transform(t)
    

def intersect(shape, src_ray):
    return shape.intersect(src_ray)


def world_to_object(a_shape, a_point):
    transformed_point = world_to_object(a_shape.parent, a_point) if a_shape.parent is not None else a_point
    return np.matmul(a_shape.inverse_transform, transformed_point, dtype=np.float32)


def normal_to_world(a_shape, a_normal):
    return a_shape.normal_to_world(a_normal)
    

def normal_at(shape, world_point):
     return shape.normal_at(world_point)
#    local_point = world_to_object(shape, world_point)
#    local_normal = shape.local_normal_at(local_point)
#    return normal_to_world(shape, local_normal)


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