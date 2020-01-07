from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np


valid_test_objects = ["light"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["intensity", "position"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_light_elements = ["position", "intensity"]
parse_light_element = TypeBuilder.make_choice(valid_light_elements)
register_type(LightElement=parse_light_element)


@given("{item:TestVariable} ← color({r:g}, {g:g}, {b:g})")
def step_impl_color_assign(context, item, r, g, b):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.color(float(r), float(g), float(b))


@given("{item:TestVariable} ← point({x:g}, {y:g}, {z:g})")
def step_impl_point_assign(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.point(float(x), float(y), float(z))


@when("{item:TestObject} ← point_light({position_val}, {intensity_val})")
def step_impl_generic_translation_matrix(context, item, position_val, intensity_val):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    assert(position_val in context.tuple.keys())
    assert(intensity_val in context.tuple.keys())
    real_position = context.tuple[str(position_val)]
    real_intensity = context.tuple[str(intensity_val)]
    context.dict[item] = base.point_light(real_position, real_intensity)


@then("position({item:TestRay}, {t}) = point({x}, {y}, {z})")
def step_impl_eval_ray_position(context, item, t, x, y, z):
    assert (item in context.dict.keys())
    ray = context.dict[str(item)]
    ray_position = ray.position(float(eval(t)))
    test_point = base.point(float(x), float(y), float(z))
    assert (base.equal(ray_position, test_point))


@then("{item:TestObject}.{element:LightElement} = {item2:TestVariable}")
def step_impl_ray_intersect_list_count(context, item, element, item2):
    assert(item in context.dict.keys())
    assert(item2 in context.tuple.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    local_object = eval(local_object_str)
    value = context.tuple[str(item2)]
    assert(base.equal(local_object, value))

