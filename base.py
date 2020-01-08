import collections
import math
import numpy as np


#cython: linetrace=True
#cython: language_level=3

from vec4 import *
from vec3 import *
from rotations import *
from canvas import *


def magnitude(v):
    if isinstance(v, (Vec4)):
        return(v.magnitude())
    else:
        return(np.abs(v))
    
    
def normalize(v):
    if isinstance(v, (Vec4)):
        mag = v.magnitude()
        if mag == 0:
            return(v)
        else:
            return (Vec4(v.x / mag, v.y / mag, v.z / mag, v.w))
    else:
        print("v was ", v)
        print("v type is ", type(v))
        assert(False)


def dot(a,b):
    if isinstance(a, (Vec4)):
        if isinstance(b, (Vec4)):
            return a.dot_prod(b)
    print("both parts of dot must be Vec4")
    assert(False)


def cross(a,b):
    if isinstance(a, (Vec4)):
        if isinstance(b, (Vec4)):
            return a.cross_prod(b)
    print("both parts of cross_product must be Vec4")
    assert(False)
    


EPSILON = 0.00005

def equal(a, b):
#    cdef int i1
#    cdef int height, width, i, j
#    cdef float n, m, delta, t
    

    if isinstance(a, int):
        a = float(a)
        
    if isinstance(b, int):
        b = float(b)
        
    if isinstance(a,float) and isinstance(b,float):
        delta = (a - b) if a>b else (b - a)
        return True if delta < EPSILON else False
     
    elif ((str(type(a)) == "<class 'vec4.Vec4'>") and (str(type(b)) == "<class 'vec4.Vec4'>") or
          (str(type(a)) == "<class 'vec3.Vec3'>") and (str(type(b)) == "<class 'vec3.Vec3'>")):

        for i1 in range(len(a)):
            n = a[i1]
            m = b[i1]
            delta = (n - m) if n > m else (m - n)
            if delta > EPSILON:
                return False
        return True
    elif (type(a) == np.ndarray) and (type(b) == np.ndarray):
        if np.array_equal(a,b):
            return True
        else:
            if len(a.shape) == 2:

                height, width = a.shape
                if (b.shape[0] != height) or (b.shape[1] != width):
                    return False

                for j in range(height):
                    for i in range(width):
                        n = a[j, i]
                        m = b[j, i]
                        delta = (n - m) if n > m else (m - n)
                        if delta > EPSILON:
                            return False
                return True
            elif len(a.shape) == 1:
                width = a.shape[0]
                for j in range(width):
                    n = a[j]
                    m = b[j]
                    delta = (n-m) if n>m else (m-n)
                    if delta > EPSILON:
                        return False
                return True
            else:
                print("undefined comparison between shape ", a.shape, " and ", b.shape)
                assert(False)
    elif ((str(type(a)) == "<class 'base.Intersection'>") and (str(type(b)) == "float")):
        t = a.t
        delta = (t - b) if t > b else (b - t)
        if delta > EPSILON:
            return False
        return True

    else:
        print("Undefined case for equal")
        print("a type is ", type(a), "  b type is ", type(b))
        return False
    
 
    


def determinant(m):
    if isinstance(m, np.ndarray):
        return np.linalg.det(m)
    else:
        print("unknown determinant implementation for type ", type(m))
        assert(False)


def submatrix(m, row, column):
    row = int(row)
    column = int(column)
    if isinstance(m, np.ndarray):
        height, width = m.shape
        assert((row >= 0) and (row < height))
        assert((column >= 0) and (column < width))

        # create intermediate array minus the specified column
        temp = np.hstack((m[:,:column], m[:,column+1:]))
        
        # create final array minus the specified row
        return(np.vstack((temp[:row, :], temp[row+1:, :])))
        
    else:
        print("unknown submatrix implementation for type ", type(m))
        assert (False)


def minor(m, row, column):
    row = int(row)
    column = int(column)
    if isinstance(m, np.ndarray):
        height, width = m.shape
        assert((row >= 0) and (row < height))
        assert((column >= 0) and (column < width))
        return determinant(submatrix(m, row, column))
    else:
        print("unknown minor implementation for type ", type(m))
        assert (False)


def cofactor(m, row, column):
    row = int(row)
    column = int(column)
    if isinstance(m, np.ndarray):
        height, width = m.shape
        assert ((row >= 0) and (row < height))
        assert ((column >= 0) and (column < width))
        # create intermediate array minus the specified column
        temp = np.hstack((m[:, :column], m[:, column + 1:]))

        # create final array minus the specified row
        m_minor = np.linalg.det(np.vstack((temp[:row, :], temp[row + 1:, :])))
        return m_minor if ((row + column) % 2) == 0 else (-m_minor)
        
    else:
        print("unknown minor implementation for type ", type(m))
        assert (False)



def is_invertible(m):
    if isinstance(m, np.ndarray):
        return not equal(np.linalg.det(m),0)
    else:
        print("unknown minor implementation for type ", type(m))
        assert (False)


def inverse(m):
    if isinstance(m, np.ndarray):
        return np.linalg.inv(m)
    else:
        print("unknown inverse implementation for type ", type(m))
        assert (False)


def translation(x, y, z):
    m = np.identity(4, float)
    m[:,3] = np.transpose(np.array([x, y, z, 1.0], dtype=float))
    return m


def scaling(x, y, z):
    m = np.identity(4, float)
    m[0,0] = x
    m[1,1] = y
    m[2,2] = z
    return m


def shearing(xy, xz, yx, yz, zx, zy):
    m = np.identity(4, float)
    m[0,1:3] = [xy, xz]
    m[1,0] = yx
    m[1,2] = yz
    m[2,0:2] =[zx, zy]
    return m

def view_transform(pt_from, pt_to, vec_up):
    fwd = normalize(pt_to - pt_from)
    upn = normalize(vec_up)
    left = cross(fwd, upn)
    true_up = cross(left, fwd)
    orientation = np.identity(4, dtype=float)
    orientation[0, 0:3] = np.array([left.x, left.y, left.z])
    orientation[1, 0:3] = np.array([true_up.x, true_up.y, true_up.z])
    orientation[2, 0:3] = np.array([-fwd.x, -fwd.y, -fwd.z])
    return np.matmul(orientation, translation(-pt_from.x, -pt_from.y, -pt_from.z))
    
    
    
class Ray(object):
    def __init__(self, origin_point, direction_vector):
        self.origin = origin_point
        self.direction = direction_vector
        
        
    def position(self, t):
        return self.origin + (self.direction * t)
 
    
    def transform(self, transformation_matrix):
        new_origin = np.matmul(transformation_matrix, self.origin)
        new_origin = Vec4(new_origin[0], new_origin[1], new_origin[2], new_origin[3])
        new_direction = np.matmul(transformation_matrix, self.direction)
        new_direction = Vec4(new_direction[0], new_direction[1], new_direction[2], new_direction[3])
        return Ray(new_origin, new_direction)



def ray(origin_pt, direction):
    return Ray(origin_pt, direction)


def position(src_ray, t):
    return src_ray.position(t)


def transform(src_ray, transform_matrix):
    return src_ray.transform(transform_matrix)
    




class Intersection(object):
    def __init__(self, t, intersected_object):
        self.t = t
        self.object = intersected_object


def intersection(t, object):
    return Intersection(t, object)





class Material(object):
    def __init__(self, material_color, ambient, diffuse, specular, shininess, reflective, transparency,
                 refractive_index):
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

    def __eq__(self, other):
        if type(other) != Material:
            print("Error - can only compare a material to another material")
            assert(False)
        for element in self.__dict__.keys():
            if self.__dict__[element] != other.__dict__[element]:
                return False
        return True


def material(material_color=color(1.0, 1.0, 1.0), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0,
             reflective=0.0, transparency=0.0, refractive_index=1.0):
    return Material(material_color, ambient, diffuse, specular, shininess, reflective, transparency, refractive_index)






class Sphere(object):
    scount = 0
    
    def __init__(self, sphere_material=None, sphere_transform=None):
        self.origin = point(0, 0, 0)

        Sphere.scount += 1
        self.instance_id = Sphere.scount
        if sphere_material is None:
            self.material = material()
        else:
            self.material = sphere_material

        if sphere_transform is None:
            self.transform = np.identity(4, dtype=float)
            self.inverse_transform = np.identity(4, dtype=float)
        else:
            self.transform = sphere_transform
            self.inverse_transform = inverse(sphere_transform)
        
        
    def intersect(self, src_ray):
        ray2 = transform(src_ray, self.inverse_transform)
        sphere_to_ray = ray2.origin - self.origin
        a2 = 2 * dot(ray2.direction, ray2.direction)
        b = 2 * dot(ray2.direction, sphere_to_ray)
        c = dot(sphere_to_ray, sphere_to_ray) - 1
        
        discriminant = (b * b) - (2 * a2 * c)
        if discriminant < 0:
            return ()
        else:
            scale_value = 1.0 / a2
            v = scale_value * np.sqrt(discriminant)
            w = scale_value * b
            t1 = -(v+w)
            t2 = v-w
            return(Intersection(t1, self), Intersection(t2, self))


    def set_transform(self, t):
        assert(t.shape == (4, 4))
        self.transform = t
        self.inverse_transform = inverse(t)
        
        
    def normal_at(self, pt):
        obj_point = np.matmul(self.inverse_transform, pt)
        obj_nml = obj_point - point(0,0,0) # np.matmul(self.inverse_transform, self.origin)
        wn = np.matmul(np.transpose(self.inverse_transform), obj_nml)
        return normalize(vector(wn[0], wn[1], wn[2]))

        
def sphere(sphere_material = None, sphere_transform = None):
    return Sphere(sphere_material, sphere_transform)

def glass_sphere(sphere_material = material(transparency=1.0, refractive_index=1.5), sphere_transform = np.identity(4, dtype=float)):
    return Sphere(sphere_material, sphere_transform)


def set_transform(s, t):
    s.set_transform(t)
    

def intersect(src_sphere, src_ray):
    return src_sphere.intersect(src_ray)


def normal_at(src_sphere, pt):
    return src_sphere.normal_at(pt)




def reflect(incoming, nml):
    return incoming - (nml * 2 * dot(incoming, nml))



class Point_Light(object):
    #scount = 0
    
    def __init__(self, light_position, light_intensity):
        self.position = light_position
        self.intensity = light_intensity
        
       # Point_Light.scount += 1
       # self.instance_id = Point_Light.scount
        
 
def point_light(light_position, light_intensity):
    return Point_Light(light_position, light_intensity)


black = color(0, 0, 0)

def lighting(material, light, point, eye_vec, normal_vec, in_shadow = False):
    effective_color = material.color * light.intensity
    light_vec = normalize(light.position - point)
    ambient = effective_color * material.ambient
    diffuse = black
    specular = black
    
    if not in_shadow:
        light_dot_normal = dot(light_vec, normal_vec)
        if light_dot_normal >= 0:
            diffuse = effective_color * material.diffuse * light_dot_normal
            reflect_vec = reflect(-light_vec, normal_vec)
            reflect_dot_eye = dot(reflect_vec, eye_vec)
            
            if reflect_dot_eye > 0:
                factor = math.pow(reflect_dot_eye, material.shininess)
                specular = light.intensity * material.specular * factor
        
    return (ambient + diffuse + specular)






class World(object):
    scount = 0
    
    def __init__(self):
        self.objects=[]
        self.light=[]
        
        World.scount += 1
        self.instance_id = World.scount
        
    
    def intersect(self, src_ray):
        hit_list = []
        for item in self.objects:
            hits = item.intersect(src_ray)
            if hits is not None:
                for each_one in hits:
                    hit_list.append(each_one)
        sorted_by_t = sorted(hit_list, key=lambda tup: tup.__dict__['t'])
        hit_list = None
        return(sorted_by_t)
        
        
def world():
    return World()


def default_world():
    new_world = World()
    new_world.light.append(point_light(point(-10.0, 10.0, -10.0), color(1.0, 1.0, 1.0)))

    new_world.objects.append(sphere(sphere_material=material(material_color=color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)))
    new_world.objects.append(sphere(sphere_transform=scaling(0.5, 0.5, 0.5)))
    return new_world


def intersect_world(w, r):
    return w.intersect(r)



class Computations(object):
    def __init__(self, hit_intersection, src_ray, full_intersection_list=None):
        if full_intersection_list is None:
            full_intersection_list = [hit_intersection]
        containers = []
        
        for i in full_intersection_list:
            if (hit_intersection.t == i.t) and (hit_intersection.object == i.object):
                if len(containers) == 0:
                    self.n1 = 1.0
                else:
                    self.n1 = containers[-1].material.refractive_index
                    
            if i.object in containers:
                containers.remove(i.object)
            else:
                containers.append(i.object)
             
            if (hit_intersection.t == i.t) and (hit_intersection.object == i.object):
                if len(containers) == 0:
                    self.n2 = 1.0
                else:
                    self.n2 = containers[-1].material.refractive_index
                break
                
        self.t = hit_intersection.t
        self.object = hit_intersection.object
        self.point = position(src_ray, self.t)
        self.eye_vector = -src_ray.direction
        self.normal_vector = normal_at(self.object, self.point)
        if dot(self.normal_vector, self.eye_vector) < 0:
            self.inside = True
            self.normal_vector = -self.normal_vector
        else:
            self.inside = False
        offset = (EPSILON * self.normal_vector)
        temp = (self.point + offset)
        self.over_point = Vec4(temp[0], temp[1], temp[2], temp[3])
        temp = (self.point - offset)
        self.under_point = Vec4(temp[0], temp[1], temp[2], temp[3])
        self.reflect_vector = reflect(src_ray.direction, self.normal_vector)



def prepare_computations(an_intersection, a_ray, full_intersection_list=None):
    if full_intersection_list is None:
        return Computations(an_intersection, a_ray)
    else:
        return Computations(an_intersection, a_ray, full_intersection_list)


# assuming a single light source for now
def is_shadowed(w, pt):
    v = w.light[0].position - pt
    distance = v.magnitude()
    direction = normalize(v)
    
    src_ray = ray(pt, direction)
    intersection_list = intersect_world(w, src_ray)
    h = hit(intersection_list)
    if h is not None:
        if h.t < distance:
            return True
    return False


# for now, just assume a single world light when shadowing.
def shade_hit(world, comps):
    shadowed = is_shadowed(world, comps.over_point)
    return lighting(comps.object.material, world.light[0], comps.over_point, comps.eye_vector, comps.normal_vector, in_shadow=shadowed)


def hit(intersection_list):
    for possible_hit in intersection_list:
        if possible_hit.t >=0:
            return possible_hit
    return None


def color_at(world, src_ray):
    intersection_list = world.intersect(src_ray)
    if len(intersection_list) == 0:
        return black
    found_hit = False
    for hit in intersection_list:
        if hit.t >= 0:
            found_hit = True
            return (shade_hit(world, prepare_computations(hit, src_ray)))

    # if we get here, there were negative hits, but none visible
    print("hit was at negative t - this shouldn't happen")
    assert(False)
    

def intersections(*arg):
    num_args = len(arg)
    for argument in arg:
        if (type(argument) != Intersection):
            print("invalid intersections() argument type")
            assert(False)
    raw_intersection_list = [argument for argument in arg]
    sorted_by_t = sorted(raw_intersection_list, key=lambda tup: tup.__dict__['t'])
    raw_intersection_list = None
    return(sorted_by_t)


class Camera(object):
    def __init__(self, hsize, vsize, field_of_view):
        self.hsize = int(hsize)
        self.vsize = int(vsize)
        self.field_of_view = field_of_view
        self.transform = np.identity(4, dtype=float)
        self.inverse_transform = np.identity(4, dtype=float)
        aspect_ratio = hsize / vsize
        half_view = math.tan(field_of_view / 2)
        if aspect_ratio >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect_ratio
        else:
            self.half_width = half_view * aspect_ratio
            self.half_height = half_view
            
        self.pixel_size = (self.half_width * 2) / self.hsize


    def set_transform(self, t):
        assert (t.shape == (4, 4))
        self.transform = t
        self.inverse_transform = inverse(t)


    def ray_for_pixel(self, px, py):
        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size
        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset
        pixel = np.matmul(self.inverse_transform, point(world_x, world_y, -1))
        origin = np.matmul(self.inverse_transform, point(0, 0, 0))
        direction = normalize(vector(pixel[0]-origin[0], pixel[1]-origin[1], pixel[2]-origin[2]))
        return ray(point(origin[0], origin[1], origin[2]), direction)


def camera(hsize, vsize, field_of_view):
    return Camera(hsize, vsize, field_of_view)


def ray_for_pixel(camera, px, py):
    return camera.ray_for_pixel(px, py)


def render(camera, world):
    image = canvas(camera.hsize, camera.vsize)
    for y in range(camera.vsize):
        for x in range(camera.hsize):
            this_ray = camera.ray_for_pixel(x, y)
            pixel_color = color_at(world, this_ray)
            image.write_pixel(x, y, pixel_color)
    return(image)
