from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
from base import equal
import numpy as np
from shape import material, sphere, test_shape, point_light, plane
from base import render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *

valid_test_planes = ["p"]
parse_test_plane = TypeBuilder.make_choice(valid_test_planes)
register_type(TestPlane=parse_test_plane)

valid_test_objects = ["m"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)

valid_test_variables = ["n1", "n2", "n3"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)

valid_intersection_elements = ["t", "object"]
parse_intersection_element = TypeBuilder.make_choice(valid_intersection_elements)
register_type(IntersectionElement=parse_intersection_element)




@given("{item:TestPlane} ← plane()")
def step_impl_basic_plane(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = plane()


@when("{item_n:TestVariable} ← local_normal_at({item_plane:TestPlane}, point({x:g}, {y:g}, {z:g}))")
def step_when_local_normal_at_on_plane(context, item_n, item_plane, x, y, z):
    assert(item_plane in context.dict.keys())
    ensure_context_has_tuple(context)
    test_plane = context.dict[str(item_plane)]
    test_point = point(float(x), float(y), float(z))
    context.tuple[str(item_n)] = test_plane.local_normal_at(test_point)


@when("{intersect_list:ListName} ← local_intersect({item_plane:TestPlane}, {item_ray:TestRay})")
def step_when_intersect_list_is_local_intersect_on_plane(context, intersect_list, item_plane, item_ray):
    assert(item_plane in context.dict.keys())
    assert(item_ray in context.dict.keys())
    ensure_context_has_dict(context)
    test_plane = context.dict[str(item_plane)]
    test_ray = context.dict[str(item_ray)]
    context.dict[str(intersect_list)] = test_plane.local_intersect(test_ray)


@then("{item_n:TestVariable} = vector({x:g}, {y:g}, {z:g})")
def step_then_variable_equals_vector_value(context, item_n, x, y, z):
    assert(item_n in context.tuple.keys())
    local_vector = context.tuple[str(item_n)]
    test_vector = vector(float(x), float(y), float(z))
    assert(equal(local_vector, test_vector))


@then("{intersect_list:ListName} is empty")
def step_impl_intersect_list_is_empty(context, intersect_list):
    assert(intersect_list in context.dict.keys())
    local_value = context.dict[str(intersect_list)]
    assert(len(local_value) == 0)


    