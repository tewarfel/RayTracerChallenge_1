from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light
from base import equal, intersect_world, shade_hit, is_shadowed, color_at, World, render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *


valid_test_objects = ["cyl"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["direction", "normal", "n"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_light_elements = ["position", "intensity"]
parse_light_element = TypeBuilder.make_choice(valid_light_elements)
register_type(LightElement=parse_light_element)

valid_material_elements = ["color", "ambient", "diffuse", "specular", "shininess", "reflective", "transparency", "refractive_index"]
parse_material_element = TypeBuilder.make_choice(valid_material_elements)
register_type(MaterialElement=parse_material_element)

valid_world_elements = ["light", "objects"]
parse_world_element = TypeBuilder.make_choice(valid_world_elements)
register_type(WorldElement = parse_world_element)


valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)


valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)


@given("{item:TestObject} ← cylinder()")
def step_basic_cylinder_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = cylinder()


@given("{nml:TestVariable} ← normalize(vector({x:g}, {y:g}, {z:g}))")
def step_cylinder_given_local_normal_is_vector(context, nml, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[str(nml)] =  vector(np.float32(x), np.float32(y), np.float32(z)).normalize()


@given("{r:TestRay} ← ray(point({x:g}, {y:g}, {z:g}), {item:TestVariable})")
def step_cylinder_given_test_ray(context, r, x, y, z, item):
    ensure_context_has_dict(context)
    context.dict[str(r)] =  ray(point(np.float32(x), np.float32(y), np.float32(z)), context.tuple[str(item)])


@given("{item:TestObject}.minimum ← {value:g}")
def step_cylinder_set_minimum(context, item, value):
    context.dict[str(item)].minimum = np.float32(value)


@given("{item:TestObject}.maximum ← {value:g}")
def step_cylinder_set_maximum(context, item, value):
    context.dict[str(item)].maximum = np.float32(value)


@given("{s:TestObject}.closed ← true")
def step_cylinder_set_closed_is_true(context, s):
    assert (s in context.dict.keys())
    context.dict[str(s)].closed = True


@when("{nml:TestVariable} ← local_normal_at({item1:TestObject}, point({x:g}, {y:g}, {z:g}))")
def step_cylinder_local_normal(context, nml, item1, x, y, z):
    assert (item1 in context.dict.keys())
    ensure_context_has_tuple(context)
    context.tuple[str(nml)] = context.dict[str(item1)].local_normal_at(point(np.float32(x), np.float32(y), np.float32(z)))

@when("{list:ListName} ← local_intersect({item:TestObject}, {r:TestRay})")
def step_cylinder_intersect_list_is_local_intersect(context, list, item, r):
    assert(item in context.dict.keys())
    assert(r in context.dict.keys())
    context.dict[str(list)] = context.dict[str(item)].local_intersect(context.dict[str(r)])





@then("{s:TestObject}.minimum = -infinity")
def step_cylinder_default_minimum_is_neg_inf(context, s):
    assert (s in context.dict.keys())
    cylinder_minimum = context.dict[str(s)].minimum
    assert (cylinder_minimum <= -1.0e8)


@then("{s:TestObject}.maximum = infinity")
def step_cylinder_default_maximum_is_inf(context, s):
    assert (s in context.dict.keys())
    cylinder_maximum = context.dict[str(s)].maximum
    assert (cylinder_maximum >= 1.0e8)


@then("{list:ListName}.count = 0")
def step_cylinder_intersect_count_is_zero(context, list):
    assert(list in context.dict.keys())
    listlen = len(context.dict[str(list)])
    assert(listlen == 0)


@then("{s:TestObject}.closed = false")
def step_cylinder_default_closed_is_false(context, s):
    assert (s in context.dict.keys())
    cylinder_closed_state = context.dict[str(s)].closed
    assert (cylinder_closed_state == False)