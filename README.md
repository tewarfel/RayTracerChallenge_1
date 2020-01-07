# RayTracerChallenge_1
## Description
snapshot of in-progress development of Python 3 code for "The Ray Tracer Challenge" by Jamis Buck, 
published by Pragmatic Bookshelf at https://pragprog.com/book/jbtracer/the-ray-tracer-challenge .
I am using the python Behave module (a cucumber-like module for Python) to implement and run the 
.feature file tests.


## Overview
This is a first-pass implementation of the functions / structures using Python3 covering content through
the end of chapter 8. I have slightly modified the Gherkin feature test code to simplify parsing of matrix 
and element definitions to use this implementation; some tests that pass are ahead of chapter 8 and I have
left them in feature files.  Other tests included in the publisher-provided Gherkin .feature files from
later chapters have been removed, and future chapter .feature files have been omitted altogether.

I make no claims of optimality or clarity but am simply archiving the current state, primarily for my 
future reference, but also to share with anyone is interested.   

As stated in the book, the key data structures are 4-element floating-point vectors (representing 
3D directional vectors and 3D points in space), 3-element floating-point vectors (representing a color),
and 4x4 floating-point matrices representing 3D transform operations.

The 3 and 4-element floating-point vector data structures (named Vec3 and Vec4, respectively) are 
subclassed from the Python Collections "namedtuple" object.  This allows their data to be accessed 
either as a 1-D array or list of vector elements (e.g. vect1[0], vect1[1]), or by "vector.element" 
names (e.g. vect1.x, vect1.y).  The 4x4 float matrices are handled as Numpy Ndarrays.
This simplifies implementation of matrix/vector multiplication by allowing use of the numpy matmul(),
as well as simplifying vector/scalar operations.

The "putting it together" example at the end of chapter 7, augmented by the addition of shadows from
chapter 8 and changing the left wall color to blue, is the code in "first_render.py".  


## Methods
The Vec3 and Vec4 object classes have been augmented to track both total references used, as well 
as maximum references in use.

For the "putting it together" example (end of chapter 7) with shadow addition (from chapter 8),
I rendered the scene onto a 100 pixel wide by 50 pixel tall canvas.

System was a 2013 MacPro with 32GB RAM, 6-core 3.5GHz Intel Xeon E5 processor (Ivy Bridge), running 
macOS High Sierra, version 10.13.6.  Python version was 3.7.5 (from "homebrew" https://brew.sh/ ),
and development environment was Pycharm Professional 2019.3 (https://www.jetbrains.com/pycharm/ ) using
the yappi 1.2.3 profiler.  Program runs and renders as a single foreground thread.

## Results
*Without profiling or reference counting, execution time was **34 seconds**.

*Without profiling (but with Vec3/Vec4 reference counting), execution time was **36 seconds**.

*With profiling and Vec3/Vec4 reference counting, program execution time was **158 seconds**, 
but running time was **14 minutes**.


Call graph profile analysis (multiple runs) shows between 89-96% of time is spent 
in "namedtuple". 

Reference tracking showed that total Vec4 instances was **288,147** but that a maximum 
of only **18** were active at any one time.

Similarly, the total number of Vec3 instances was **33,381** but that a maximum of only **16**
were active at any one time.

## Thoughts
Finding a faster basis for the Vec3/Vec4 structures is probably the way to improve it.
I'm going to pass on that for now to add the additional features for planes, cubes, 
and triangles, and then revisit whether this still looks like the bottleneck.


