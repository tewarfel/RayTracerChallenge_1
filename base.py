import collections
import math
import numpy as np


#cython: linetrace=True
#cython: language_level=3

#from vec4 import *
#from vec3 import *

from memblock import *

from rotations import *
from canvas import *


#from shape import material, Shape, Sphere, sphere, glass_sphere, set_transform, intersect, normal_at, reflect


def magnitude(v):
    if isinstance(v, (Vec4)):
        return(v.magnitude())
    else:
        return(np.abs(v))
    
    
def normalize(v):
    return v.normalize()
    
#    if isinstance(v, (Vec4)):
#        mag = v.magnitude()
#        if mag == 0:
#            return(v)
#        else:
#            return (Vec4(v.x / mag, v.y / mag, v.z / mag, v.w))
#    else:
#        print("v was ", v)
#        print("v type is ", type(v))
#        assert(False)


def dot(a,b):
    return(a.dot_prod(b))
#    if isinstance(a, (Vec4)):
#        if isinstance(b, (Vec4)):
#            return a.dot_prod(b)
#    print("both parts of dot must be Vec4")
#    assert(False)


def cross(a,b):
    return(a.cross_prod(b))
#    if isinstance(a, (Vec4)):
#        if isinstance(b, (Vec4)):
#            return a.cross_prod(b)
#    print("both parts of cross_product must be Vec4")
#    assert(False)
    

def reflect(incoming, nml):
    return incoming - (nml * 2 * dot(incoming, nml))


EPSILON = 0.000065

def equal(a, b):
    if isinstance(a, int):
        a = np.float32(a)
        
    if isinstance(b, int):
        b = np.float32(b)
        
    if isinstance(a,(float, np.float32, np.float64)) and \
          isinstance(b,(float, np.float32, np.float64)):
        delta = (a - b) if a>b else (b - a)
        return True if delta < EPSILON else False
     
    elif ((str(type(a)) == "<class 'memblock.Vec4'>") and (str(type(b)) == "<class 'memblock.Vec4'>") or
          (str(type(a)) == "<class 'memblock.Vec3'>") and (str(type(b)) == "<class 'memblock.Vec3'>")):
        return a.__eq__(b)
#        for i1 in range(len(a)):
#            n = a[i1]
#            m = b[i1]
#            delta = (n - m) if n > m else (m - n)
#            if delta > EPSILON:
#                return False
#        return True
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
    elif type(a) == np.ndarray and type(b) == Vec4:
        return (b.__eq__(a))
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
        [ox,oy,oz,ow]=self.origin
        new_origin = Vec4(np.matmul(transformation_matrix, np.array([ox,oy,oz,ow],dtype=np.float32)))
        [ox,oy,oz,ow] = self.direction
        new_direction = Vec4(np.matmul(transformation_matrix, np.array([ox,oy,oz,ow], dtype=np.float32)))
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






black = color(0, 0, 0)


def lighting(material, object, light, point, eye_vec, normal_vec, in_shadow=False):
    ""
    current_color = material.pattern.pattern_at_shape(object, point) if material.pattern is not None else material.color
    effective_color = current_color * light.intensity
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




class Pattern(object):
    def __init__(self, transform=None):
        if transform is None:
            self.transform = np.identity(4, dtype=float)
            self.inverse_transform = np.identity(4, dtype=float)
        else:
            self.transform = transform
            self.inverse_transform = inverse(transform)


    def pattern_at_shape(self, a_shape, a_world_pt):
        if not is_point(a_world_pt):
            print("in Pattern::pattern_at_shape, pt is not a point: ", a_world_pt)
            assert(False)
        [ox,oy,oz,ow]=a_world_pt
        shape_pt = np.matmul(a_shape.inverse_transform, np.array([ox,oy,oz,ow], dtype=np.float32))
        pattern_pt = np.matmul(self.inverse_transform, shape_pt)
        return self.pattern_at(point(pattern_pt[0], pattern_pt[1], pattern_pt[2]))

    # dummy pattern for tests
    def pattern_at(self, pt):
        return(color(pt.x, pt.y, pt.z))

    def set_transform(self, t):
        self.transform = t
        self.inverse_transform = inverse(t)


def test_pattern(transform=None):
    return Pattern(transform)


class Stripe_Pattern(Pattern):
    def __init__(self, color1, color2, transform=None):
        have_error = False
        if not is_vec3(color1):
            print("in Stripe_Pattern, color1 is not Vec3: ", color1)
            have_error = True
        if not is_vec3(color2):
            have_error = True
            print("in Stripe_Pattern, color2 is not Vec3: ",color2)
        if have_error:
            assert(False)
            
        super().__init__(transform)
        self.a = color1
        self.b = color2

    def pattern_at(self, pt):
        if not is_point(pt):
            print("in Stripe_Pattern::color, pt is not a point: ", pt)
            assert(False)
        return self.a if (math.floor(pt.x) % 2 == 0) else self.b
      
        
def stripe_pattern(color1, color2, transform=None):
    return Stripe_Pattern(color1, color2, transform)


def stripe_at(a_pattern, a_pt):
    return a_pattern.stripe_at(a_pt)


def stripe_at_object(a_pattern, an_object, a_world_point):
    object_pt = np.matmul(an_object.inverse_transform, a_world_point)
    pattern_pt = np.matmul(a_pattern.inverse_transform, object_pt)
    return a_pattern.stripe_at(point(pattern_pt[0], pattern_pt[1], pattern_pt[2]))


class Gradient_Pattern(Pattern):
    def __init__(self, color1, color2, transform=None):
        have_error = False
        if not is_vec3(color1):
            have_error = True
        if not is_vec3(color2):
            have_error = True
            print("in Gradient_Pattern, color2 is not Vec3: ", color2)
        if have_error:
            assert (False)
        
        super().__init__(transform)
        self.a = color1
        self.b = color2
        self.range = color2-color1
    
    def pattern_at(self, pt):
        if not is_point(pt):
            print("in Gradient_Pattern::color, pt is not a point: ", pt)
            assert (False)
        return self.a + (self.range * np.float32(pt.x - math.floor(pt.x)))
    
    
def gradient_pattern(color1, color2, transform=None):
    return Gradient_Pattern(color1, color2, transform)


class Ring_Pattern(Pattern):
    def __init__(self, color1, color2, transform=None):
        have_error = False
        if not is_vec3(color1):
            have_error = True
        if not is_vec3(color2):
            have_error = True
            print("in Ring_Pattern, color2 is not Vec3: ", color2)
        if have_error:
            assert (False)
        
        super().__init__(transform)
        self.a = color1
        self.b = color2
    
    def pattern_at(self, pt):
        if not is_point(pt):
            print("in Ring_Pattern::color, pt is not a point: ", pt)
            assert (False)
        t = math.floor(math.sqrt((pt.x * pt.x) + (pt.z*pt.z))) % 2
        return self.a if t==0 else self.b


def ring_pattern(color1, color2, transform=None):
    return Ring_Pattern(color1, color2, transform)


class Checkers_Pattern(Pattern):
    def __init__(self, color1, color2, transform=None):
        have_error = False
        if not is_vec3(color1):
            have_error = True
        if not is_vec3(color2):
            have_error = True
            print("in Checkers_Pattern, color2 is not Vec3: ", color2)
        if have_error:
            assert (False)
        
        super().__init__(transform)
        self.a = color1
        self.b = color2
    
    def pattern_at(self, pt):
        if not is_point(pt):
            print("in Checkers_Pattern::color, pt is not a point: ", pt)
            assert (False)
        t = (math.floor(pt.x) + math.floor(pt.y) + math.floor(pt.z)) % 2
        return self.a if t == 0 else self.b


def checkers_pattern(color1, color2, transform=None):
    return Checkers_Pattern(color1, color2, transform)



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
                
        self.t = np.float32(hit_intersection.t)
        self.object = hit_intersection.object
        self.point = position(src_ray, self.t)
        self.eye_vector = -src_ray.direction
        self.normal_vector = self.object.normal_at(self.point)
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
def shade_hit(world, comps, remaining=5):
    shadowed = is_shadowed(world, comps.over_point)
    surface = lighting(comps.object.material, comps.object, world.light[0], comps.over_point, comps.eye_vector, comps.normal_vector, in_shadow=shadowed)
    reflected = reflected_color(world, comps, remaining)
    refracted = refracted_color(world, comps, remaining)
    this_material = comps.object.material
    if (this_material.reflective > 0) and (this_material.transparency > 0):
        reflectance = schlick(comps)
        return surface + (reflected * reflectance) + (refracted * (1 - reflectance))
    else:
        return surface + reflected + refracted


def hit(intersection_list):
    for possible_hit in intersection_list:
        if possible_hit.t >=0:
            return possible_hit
    return None


def color_at(world, src_ray, remaining):
    intersection_list = world.intersect(src_ray)
    if len(intersection_list) == 0:
        return black
    found_hit = False
    for hit in intersection_list:
        if hit.t >= 0:
            found_hit = True
            return (shade_hit(world, prepare_computations(hit, src_ray), remaining))

    # if we get here, there were negative hits, but none visible
    return black

    

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
        
        pixel = np.matmul(self.inverse_transform, np.array([world_x, world_y, -1, 1], dtype=np.float32))
        origin = np.matmul(self.inverse_transform, np.array([0, 0, 0, 1], dtype=np.float32))
        direction = normalize(vector(pixel[0]-origin[0], pixel[1]-origin[1], pixel[2]-origin[2]))
        return ray(point(origin[0], origin[1], origin[2]), direction)


def camera(hsize, vsize, field_of_view):
    return Camera(hsize, vsize, field_of_view)


def ray_for_pixel(camera, px, py):
    return camera.ray_for_pixel(px, py)


def render(camera, world, max_bounce=5):
    image = canvas(camera.hsize, camera.vsize)
    for y in range(camera.vsize):
        for x in range(camera.hsize):
            this_ray = camera.ray_for_pixel(x, y)
            pixel_color = color_at(world, this_ray, max_bounce)
            image.write_pixel(x, y, pixel_color)
    return(image)


def reflected_color(a_world, comps, remaining):
    if comps.object.material.reflective == 0:
        return black
    
    if remaining < 1:
        return black
    
    reflect_ray = ray(comps.over_point, comps.reflect_vector)
    temp_color = color_at(a_world, reflect_ray, remaining-1)
    return (temp_color * comps.object.material.reflective)


def refracted_color(a_world, comps, remaining):
    if comps.object.material.transparency == 0:
        return black
    if remaining < 1:
        return black
    n_ratio = np.float32(comps.n1 / comps.n2)
    cos_i = dot(comps.eye_vector, comps.normal_vector)
    sin2_t = (n_ratio * n_ratio) * (1 - (cos_i * cos_i))
    if sin2_t > 1:
        return black
    
    cos_t = np.float32(math.sqrt(1.0 - sin2_t))
    sin2_t = np.float32(sin2_t)
    
    # direction of the refracted ray
    direction_vector = comps.normal_vector * (n_ratio * cos_i - cos_t) - (comps.eye_vector * n_ratio)
    
    # create the refracted ray
    refract_ray = ray(comps.under_point, direction_vector)

    # Find the color of the refracted ray, making sure to multiply by the transparency value to account for any opacity
    return (color_at(a_world, refract_ray, remaining-1) * comps.object.material.transparency)
    
    
def schlick(comps):
    cos_a = dot(comps.eye_vector, comps.normal_vector)
    
    if comps.n1 > comps.n2:
        n = comps.n1 / comps.n2
        sin2t = (n*n) * (1.0 - (cos_a * cos_a))
        if sin2t > 1.0:
            return 1.0
        
        cos_t = math.sqrt(1.0 - sin2t)
        cos_a = cos_t
    r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2))
    r02 = (r0*r0)
    
    return r02 + (1-r02) * math.pow((1-cos_a), 5)


