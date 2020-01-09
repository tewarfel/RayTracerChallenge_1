from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light
from base import equal, intersect_world, shade_hit, is_shadowed, color_at, World, render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *


valid_test_objects = ["c"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["normal", "color", "p"]
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


@given("{item:TestObject} ← cube()")
def step_basic_cube_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = cube()


@when("{list:ListName} ← local_intersect({item1:TestObject}, {ray1:TestRay})")
def step_cube_local_intersect(context, list, item1, ray1):
    assert(item1 in context.dict.keys())
    assert(ray1 in context.dict.keys())
    cube_object = context.dict[str(item1)]
    ray_object = context.dict[str(ray1)]
    context.dict[str(list)] = cube_object.local_intersect(ray_object)


@when("{nml:TestVariable} ← local_normal_at({item1:TestObject}, {pt:TestVariable})")
def step_cube_local_normal(context, nml, item1, pt):
    assert (item1 in context.dict.keys())
    assert (pt in context.tuple.keys())
    cube_object = context.dict[str(item1)]
    test_point = context.tuple[str(pt)]
    context.tuple[str(nml)] = cube_object.local_normal_at(test_point)


@then("{nml:TestVariable} = vector({x:g}, {y:g}, {z:g})")
def step_cube_local_normal_is_vector(context, nml, x, y, z):
    assert (nml in context.tuple.keys())
    cube_normal = context.tuple[str(nml)]
    test_vector = vector(np.float32(x), np.float32(y), np.float32(z))
    assert(equal(cube_normal, test_vector))
  
