from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import os
import numpy

os.environ["CPPFLAGS"] = os.getenv("CPPFLAGS", "") + "-I" + numpy.get_include()

ext_modules=[
    Extension("memblock", ["memblock.pyx"])
]

setup(
    name = 'Render',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
)

