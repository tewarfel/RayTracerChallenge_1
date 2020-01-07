from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np


valid_test_matrices = ["m"]
parse_test_matrix = TypeBuilder.make_choice(valid_test_matrices)
register_type(TestMatrix=parse_test_matrix)

valid_vec4_extensions = ["x", "y", "z", "w"]
parse_vec4_extension = TypeBuilder.make_choice(valid_vec4_extensions)
register_type(Vec4Ext=parse_vec4_extension)

valid_test_variables = ["origin", "direction", "m"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_test_rays = ["r", "r2"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)

valid_ray_elements = ["origin", "direction"]
parse_ray_element = TypeBuilder.make_choice(valid_ray_elements)
register_type(RayElement=parse_ray_element)

@given(u'{item:TestVariable} ← point({x:g}, {y:g}, {z:g})')
def step_impl_generic_point(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.point(float(x), float(y), float(z))


@given(u'{item:TestVariable} ← vector({x:g}, {y:g}, {z:g})')
def step_impl_generic_vector(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), float(y), float(z))



@given("{item:TestMatrix} ← translation({x:g}, {y:g}, {z:g})")
def step_impl_generic_translation_matrix(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.translation(float(x), float(y), float(z))



@given("{item:TestMatrix} ← scaling({x:g}, {y:g}, {z:g})")
def step_impl_generic_scaling_matrix(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.scaling(float(x), float(y), float(z))



@given("{item:TestRay} ← ray(point({px}, {py}, {pz}), vector({vx}, {vy}, {vz}))")
def step_impl_generic_ray_full(context, item, px, py, pz, vx, vy, vz):
    pt = base.point(float(px), float(py), float(pz))
    vc = base.vector(float(vx), float(vy), float(vz))
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.ray(pt, vc)



@when("{item:TestRay} ← ray({origin}, {direction})")
def step_impl_generic_ray_implied(context, item, origin, direction):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    assert(origin in context.tuple.keys())
    assert(direction in context.tuple.keys())
    origin_pt = context.tuple[str(origin)]
    dir_vector = context.tuple[str(direction)]
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.ray(origin_pt, dir_vector)


@when("{ray2:TestRay} ← transform({ray1:TestRay}, {m:TestMatrix})")
def step_impl_generic_ray_implied(context, ray2, ray1, m):
    assert(m in context.dict.keys())
    assert(ray1 in context.dict.keys())
    original_ray = context.dict[str(ray1)]
    transform_matrix = context.dict[str(m)]
    context.dict[str(ray2)] = base.transform(original_ray, transform_matrix)



@then("{item:TestRay}.{element:RayElement} = point({x}, {y}, {z})")
def step_impl_ray_element_point(context, item, element, x, y, z):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = base.point(float(x), float(y), float(z))
    assert(base.equal(thing, vec4_value))



@then("{item:TestRay}.{element:RayElement} = vector({x}, {y}, {z})")
def step_impl_ray_element_vector(context, item, element, x, y, z):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = base.vector(float(x), float(y), float(z))
    assert(base.equal(thing, vec4_value))



@then("{item:TestRay}.{element:RayElement} = {value:RayElement}")
def step_impl_ray_element(context, item, element, value):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = context.tuple[str(value)]
    assert(base.equal(thing, vec4_value))



@then("position({item:TestRay}, {t}) = point({x}, {y}, {z})")
def step_impl_eval_ray_position(context, item, t, x, y, z):
    assert (item in context.dict.keys())
    ray = context.dict[str(item)]
    ray_position = ray.position(float(eval(t)))
    test_point = base.point(float(x), float(y), float(z))
    assert (base.equal(ray_position, test_point))
