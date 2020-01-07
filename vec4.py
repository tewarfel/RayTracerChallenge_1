import collections
import numpy as np


#cython: linetrace=True
#cython: language_level=3


class Vec4(collections.namedtuple('Vec4','x y z w')):
#    cpdef int active_count
#    cpdef int total_used
#    cpdef int max_active
    
    active_count = 0
    total_used=0
    max_active = 0
    
    def __init__(self, x,  y,  z, w):
        self.value = collections.namedtuple('Vec4', 'x y z w')(x, y, z, w)
        Vec4.active_count += 1
        Vec4.total_used += 1
        if Vec4.active_count > Vec4.max_active:
            Vec4.max_active = Vec4.active_count

    def __del__(self):
        Vec4.active_count -= 1
        
    
    def __add__(self, other):
        if isinstance(other, Vec4):
            return Vec4(self.value.x + other.x,
                        self.value.y + other.y,
                        self.value.z + other.z,
                        self.value.w + other.w)
        else:
            print("__add__ in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)

    def __mul__(self, other):
        if isinstance(other, int):
            return Vec4(self.value.x * other,
                        self.value.y * other,
                        self.value.z * other,
                        self.value.w * other)
        elif isinstance(other, float):
            return Vec4(self.value.x * other,
                        self.value.y * other,
                        self.value.z * other,
                        self.value.w * other)

        else:
            print("__mul__ in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert(False)

    def __rmul__(self, other):
        if isinstance(other, int):
            return Vec4(self.value.x * other,
                        self.value.y * other,
                        self.value.z * other,
                        self.value.w * other)
        elif isinstance(other, float):
            return Vec4(self.value.x * other,
                        self.value.y * other,
                        self.value.z * other,
                        self.value.w * other)
        else:
            print("__rmul__ in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert(False)


    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec4(self.value.x / other,
                        self.value.y / other,
                        self.value.z / other,
                        self.value.w / other)
        else:
            print("__truediv__ in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert(False)


    def __sub__(self, other):
        return Vec4(self.value.x - other.x,
                    self.value.y - other.y,
                    self.value.z - other.z,
                    self.value.w - other.w)


    def __neg__(self):
        return Vec4(-self.value.x,
                    -self.value.y,
                    -self.value.z,
                    -self.value.w)
    
    
    def mag_squared(self):
        x = self.value.x
        y = self.value.y
        z = self.value.z
        w = self.value.w
        return(((x*x) + (y*y)) + ((z*z) + (w*w)))
    
    
    def magnitude(self):
        return np.sqrt(self.mag_squared())
    
    def dot_prod(self, other):
        if isinstance(other, Vec4):
            return((self.value.x * other.x) + (self.value.y * other.y) + (self.value.z * other.z) + (self.value.w * other.w))
        else:
            print("illegal argument for dot-product")
            print("dot_prod in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert (False)

    def cross_prod(self, other):
        if isinstance(other, Vec4):
            return (Vec4((self.value.y * other.z) - (self.value.z * other.y),
                         (self.value.z * other.x) - (self.value.x * other.z),
                         (self.value.x * other.y) - (self.value.y * other.x),0))
        else:
            print("illegal argument for cross-product")
            print("cross_prod in Vec4 received a ", type(other), " for the other parameter.")
            print(other)
            assert(False)
        
    
def vec4(x, y,  z, w):
    return (Vec4(x, y, z, w))


def point(x, y, z):
    return (Vec4(x, y, z, 1))

def vector( x, y, z):
    return (Vec4(x, y, z, 0))


def is_vec4(k):
#    cdef int j
#    cdef int fsum
    klen = len(k)
    if klen == 4:
        fsum = 0
        for j in k[:3]:
            try:
                float(j)
                fsum += 1
            except ValueError:
                return False
        if fsum == 3:
            return True
    return False


def is_point(k):
    if is_vec4(k):
        if int(k[3]) == 1:
            return True
    return False


def is_vector(k):
    if is_vec4(k):
        if k[3] == 0:
            return True
    return False

