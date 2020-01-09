
import numpy as np
cimport numpy as np

DTYPE = np.float32
ctypedef np.float32_t DTYPE_T


cdef class MemBlock():
    cdef public np.ndarray block
    cdef readonly int width
    cdef readonly int num_vectors
    cdef readonly str vector_name
    cdef public np.ndarray freelist
    cdef  int next_allocation
    
    def __init__(self, int vector_width, int num_vectors, str name):
        self.block = np.zeros((num_vectors, vector_width), dtype=DTYPE)
        self.width = vector_width
        self.num_vectors = num_vectors
        self.vector_name = name
        self.freelist=np.ones((num_vectors), dtype=np.uint8)
        self.next_allocation = 0
        print("\n** Creating MemBlock names ", name, " with ", num_vectors, " vectors, each ", vector_width, " floats wide.")
        print()
        
    # this code is single-thread only
    cpdef public int allocate_vector(self):
        cdef int i
        i = self.next_allocation
        if self.freelist[i]:
             self.freelist[i] = 0  # needs to be atomic test ==1 and set=0 for multithread
             self.next_allocation = (i + 1) % self.num_vectors
             return i
        else:
            i += 1
            if i==self.num_vectors:
                i=0
                
            while i<self.num_vectors:
                if self.freelist[i]:
                    self.freelist[i] = 0  # needs to be atomic test ==1 and set=0 for multithread
                    self.next_allocation = (i + 1) % self.num_vectors
                    return i
                i += 1
                
            # one more pass before giving up
            i=0
            while i<self.num_vectors:
                if self.freelist[i]:
                    self.freelist[i] = 0  # needs to be atomic test ==1 and set=0 for multithread
                    self.next_allocation = (i + 1) % self.num_vectors
                    return i
                i += 1
        print("Error - exhausted pre-allocated vector storage for ", self.vector_name,".")
        print("Used all ", self.num_vectors, " vector slots.")
        quit(1)
        
        
    # this code is single-thread only
    cpdef public void free_vector(self, int vector_index):
        # needs to be atomic test ==0 and set=1 for multithread
        self.freelist[vector_index]=1


    
    
class Vec4():
    memblock = MemBlock(4, 512, "Vec4")
    #cdef int index
    
    def __init__(self, *args):
       # print("in __init__: ", type(self))
       # print("Args in __init__:", args)
        cdef int index
        index = Vec4.memblock.allocate_vector()
        self.index = index
       # print("assigning new Vec4 as index ", index)
        if len(args) == Vec4.memblock.width:
            Vec4.memblock.block[index, :] = args[0:Vec4.memblock.width]
        else:
            Vec4.memblock.block[index] = args[0]
        
    def __del__(self):
       # print("in __del__: ", type(self))
        Vec4.memblock.free_vector(self.index)

    def get_x(self):
        return Vec4.memblock.block[self.index, 0]

    def set_x(self, DTYPE_T value):
        Vec4.memblock.block[self.index, 0] = value

    x = property(get_x, set_x)

    def get_y(self):
        return Vec4.memblock.block[self.index, 1]

    def set_y(self, DTYPE_T value):
        Vec4.memblock.block[self.index, 1] = value

    y = property(get_y, set_y)

    def get_z(self):
        return Vec4.memblock.block[self.index, 2]

    def set_z(self,  DTYPE_T value):
        Vec4.memblock.block[self.index, 2] = value

    z = property(get_z, set_z)

    def get_w(self):
        return Vec4.memblock.block[self.index, 3]

    def set_w(self, DTYPE_T value):
        Vec4.memblock.block[self.index, 3] = value

    w = property(get_w, set_w)

    def __getitem__(self, int item):
        return Vec4.memblock.block[self.index, item]
    
    def __setitem__(self, int key, DTYPE_T value):
        Vec4.memblock.block[self.index, key] = value

    def __get__(self, instance, owner):
        print("in Vec4 __get__")
        return Vec4.memblock.block[self.index, :]
    
    def __set__(self, instance, DTYPE_T value):
        print("in Vec4 __set__")
        Vec4.memblock.block[self.value] = value


    def __repr__(self):
      #  print("\nin Vec4 __repr__\n")
        return str(Vec4.memblock.block[self.index, :])


    def __copy__(self):
       # print("in Vec4 __copy__")
        return Vec4(Vec4.memblock.block[self.index, :])


    def copy(self):
       # print("in Vec4 copy")
        return Vec4(Vec4.memblock.block[self.index, :])


    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vec4(Vec4.memblock.block[self.index, :] + (other * np.ones((Vec4.memblock.width), dtype=np.float32)))
        else:
            return Vec4(Vec4.memblock.block[self.index, :] + Vec4.memblock.block[other.index, :])


    def __mul__(self, other):
        other_type = type(other)
      #  print("in Vec4 __mul__, type of other is ", other_type)

        if other_type==int or other_type==float or other_type==np.float32:
            return Vec4(Vec4.memblock.block[self.index, :] * other)
        elif other_type==Vec4:
            return Vec4(Vec4.memblock.block[self.index, :] *
                        Vec4.memblock.block[other.index, :])
        else:
            print("unhandled type ", other)
            print("                 shape of other is ", other.shape)
            print("                 len of other is ", len(other))
            quit(1)


    def __rmul__(self, other):
        other_type = type(other)
        if other_type==int or other_type==float or other_type==np.float32:
            return Vec4(Vec4.memblock.block[self.index, :] * other)
        elif other_type==Vec4:
            return Vec4(Vec4.memblock.block[self.index, :] *
                        Vec4.memblock.block[other.index, :])
        else:
            print("unhandled type ", other)
            print("                 shape of other is ", other.shape)
            print("                 len of other is ", len(other))
            quit(1)


    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec4(Vec4.memblock.block[self.index, :] * (1.0/other))


    def __neg__(self):
        return Vec4(-Vec4.memblock.block[self.index, :])

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vec4(Vec4.memblock.block[self.index, :] - (other * np.ones((Vec4.memblock.width), dtype=np.float32)))
        else:
            return Vec4(Vec4.memblock.block[self.index, :] - Vec4.memblock.block[other.index, :])


    def mag_squared(self):
        return np.sum(Vec4.memblock.block[self.index, :] *
                      Vec4.memblock.block[self.index, :])


    def magnitude(self):
        return np.sqrt(np.sum(Vec4.memblock.block[self.index, :] *
                              Vec4.memblock.block[self.index, :]))

    def dot_prod(self, other):
        return np.sum(Vec4.memblock.block[self.index, :] *
                      Vec4.memblock.block[other.index, :])

    def cross_prod(self, other):
        [sx,sy,sz,sw] = Vec4.memblock.block[self.index, :]
        [ox,oy,oz,ow] = Vec4.memblock.block[other.index, :]
        return Vec4((sy*oz)-(sz*oy), (sz*ox)-(sx*oz), (sx*oy)-(sy*ox), 0)

    def is_vec4(self):
        return True

    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vec4(Vec4.memblock.block[self.index, :])
        else:
            s = 1.0/m
            [x,y,z,w] = Vec4.memblock.block[self.index, :]
            return Vec4(s*x, s*y, s*z, w)
        

    def get_classname(self):
        return Vec4.memblock.vector_name


def point(DTYPE_T x, DTYPE_T y, DTYPE_T z):
    return(Vec4(x, y, z, 1))


def vector(DTYPE_T x, DTYPE_T y, DTYPE_T z):
    return(Vec4(x, y, z, 0))


def is_vec4(k):
    try:
        if k.is_vec4():
            return True
        else:
            return False
    except:
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



class Vec3():
    memblock = MemBlock(3, 512, "Vec3")
    
    def __init__(self, *args):
        index = Vec3.memblock.allocate_vector()
        self.index = index

        if len(args) == Vec3.memblock.width:
            Vec3.memblock.block[index, :] = args[0:Vec3.memblock.width]
        else:
            Vec3.memblock.block[index] = args[0]
    
    def __del__(self):
        Vec3.memblock.free_vector(self.index)
    
    def get_red(self):
        return Vec3.memblock.block[self.index, 0]
    
    def set_red(self, value):
        Vec3.memblock.block[self.index, 0] = value
    
    red = property(get_red, set_red)
    
    def get_green(self):
        return Vec3.memblock.block[self.index, 1]
    
    def set_green(self, value):
        Vec3.memblock.block[self.index, 1] = value
    
    green = property(get_green, set_green)
    
    def get_blue(self):
        return Vec3.memblock.block[self.index, 2]
    
    def set_blue(self, value):
        Vec3.memblock.block[self.index, 2] = value
    
    blue = property(get_blue, set_blue)
    
    def __getitem__(self, item):
        return Vec3.memblock.block[self.index, item]
    
    def __setitem__(self, key, value):
        Vec3.memblock.block[self.index, key] = value
    
    def __get__(self, instance, owner):
        print("in Vec3 __get__")
        return Vec3.memblock.block[self.index, :]
    
    def __set__(self, instance, value):
        print("in Vec3 __set__")
        Vec3.memblock.block[self.value] = value
    
    def __repr__(self):
        return str(Vec3.memblock.block[self.index, :])
    
    def __copy__(self):
        return Vec3(Vec3.memblock.block[self.index, :])
    
    def copy(self):
        return Vec3(Vec3.memblock.block[self.index, :])
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(Vec3.memblock.block[self.index, :] + (other * np.ones((Vec3.memblock.width), dtype=np.float32)))
        else:
            return Vec3(Vec3.memblock.block[self.index, :] + Vec3.memblock.block[other.index, :])
    
    def __mul__(self, other):
        other_type = type(other)
        
        if other_type == int or other_type == float or other_type==np.float32:
            return Vec3(Vec3.memblock.block[self.index, :] * other)
        elif other_type == Vec3:
            return Vec3(Vec3.memblock.block[self.index, :] *
                        Vec3.memblock.block[other.index, :])
        else:
            print("unhandled type ", other)
            print("                 shape of other is ", other.shape)
            print("                 len of other is ", len(other))
            quit(1)
    
    def __rmul__(self, other):
        other_type = type(other)
        if other_type == int or other_type == float:
            return Vec3(Vec3.memblock.block[self.index, :] * other)
        elif other_type == Vec3:
            return Vec3(Vec3.memblock.block[self.index, :] *
                        Vec3.memblock.block[other.index, :])
        else:
            print("unhandled type ", other)
            print("                 shape of other is ", other.shape)
            print("                 len of other is ", len(other))
            quit(1)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(Vec3.memblock.block[self.index, :] * (1.0 / other))
    
    def __neg__(self):
        return Vec3(-Vec3.memblock.block[self.index, :])
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(Vec3.memblock.block[self.index, :] - (other * np.ones((Vec3.memblock.width), dtype=np.float32)))
        else:
            return Vec3(Vec3.memblock.block[self.index, :] - Vec3.memblock.block[other.index, :])
    
    def mag_squared(self):
        return np.sum(Vec3.memblock.block[self.index, :] *
                      Vec3.memblock.block[self.index, :])
    
    def magnitude(self):
        return np.sqrt(np.sum(Vec3.memblock.block[self.index, :] *
                              Vec3.memblock.block[self.index, :]))
    
    def dot_prod(self, other):
        return np.sum(Vec3.memblock.block[self.index, :] *
                      Vec3.memblock.block[other.index, :])

    def cross_prod(self, other):
        [sx, sy, sz] = Vec3.memblock.block[self.index, :]
        [ox, oy, oz] = Vec3.memblock.block[other.index, :]
        return Vec3((sy * oz) - (sz * oy), (sz * ox) - (sx * oz), (sx * oy) - (sy * ox))

    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vec3(Vec3.memblock.block[self.index, :])
        else:
            s = 1.0 / m
            [r, g, b] = Vec3.memblock.block[self.index, :]
            return Vec3(s * r, s * g, s * b)

    def is_vec3(self):
        return True
    
    def get_classname(self):
        return Vec3.memblock.vector_name


cpdef color(DTYPE_T red, DTYPE_T green, DTYPE_T blue):
    return (Vec3(red, green, blue))


def is_vec3(k):
    try:
        if k.is_vec3():
            return True
        else:
            return False
    except:
        return False




def test_main():
    print("Exercising classes.")
    a = Vec4(0,1,2,3)
    print("a.x is ", a.x)
    print("a.y is ", a.y)
    print("a.z is ", a.z)
    print("a.w is ", a.w)
    print(a[0], a[1], a[2], a[3])
    print()
    print("a itself is ", a)
    print()

    b = a
    c = a.copy()
    print("b is ", b)
    print("c is ", c)
    a.x = 99
    print("setting a[0]=99, now ")
    print("a is ", a)
    print("b is ", b)
    print("c is ", c)

    d=Vec4(2,-2, 3, -3)
    print()
    print()
    
    print("d is type ", type(d))
    print("d is ", d)
    print()
    
    e = c+d
    print("e type is ", type(e))
    print("e is ", e)
    print()
    
    f = float(2) * a
    print("f type is ", type(f))
    print("f is ", f)
    print()
    
    g = a * 2
    print("g type is ", type(g))
    print("g is ", g)
    print()

    h = a*a
    print("h type is ", type(h))
    print("h is ", h)
    print()
    
    
    print()
    print()
    print()
    
if __name__ == "__main__":
    test_main()