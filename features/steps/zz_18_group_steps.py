from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light
from base import equal, intersect_world, shade_hit, is_shadowed, color_at, World, render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *


valid_test_objects = ["g", "s", "s1", "s2", "s3"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)


valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)


valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)


@given("{item:TestObject} ← group()")
def step_basic_group_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = group()


@given("{nml:TestVariable} ← normalize(vector({x:g}, {y:g}, {z:g}))")
def step_group_given_local_normal_is_vector(context, nml, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[str(nml)] =  vector(np.float32(x), np.float32(y), np.float32(z)).normalize()


@given("{r:TestRay} ← ray(point({x:g}, {y:g}, {z:g}), {item:TestVariable})")
def step_group_given_test_ray(context, r, x, y, z, item):
    ensure_context_has_dict(context)
    context.dict[str(r)] =  ray(point(np.float32(x), np.float32(y), np.float32(z)), context.tuple[str(item)])


@given("add_child({g:TestObject}, {s:TestObject})")
def step_group_given_add_child(context, g, s):
    assert (s in context.dict.keys())
    assert (g in context.dict.keys())
    context.dict[str(g)].add_child(context.dict[str(s)])


@given("set_transform({g:TestObject}, scaling({x:g}, {y:g}, {z:g}))")
def step_group_given_set_transform_scaling(context, g, x,y,z):
    assert (g in context.dict.keys())
    context.dict[str(g)].set_transform(scaling(np.float32(x), np.float32(y), np.float32(z)))


@when("{nml:TestVariable} ← local_normal_at({item1:TestObject}, point({x:g}, {y:g}, {z:g}))")
def step_group_local_normal(context, nml, item1, x, y, z):
    assert (item1 in context.dict.keys())
    ensure_context_has_tuple(context)
    context.tuple[str(nml)] = context.dict[str(item1)].local_normal_at(point(np.float32(x), np.float32(y), np.float32(z)))

@when("{list:ListName} ← local_intersect({item:TestObject}, {r:TestRay})")
def step_group_intersect_list_is_local_intersect(context, list, item, r):
    assert(item in context.dict.keys())
    assert(r in context.dict.keys())
    context.dict[str(list)] = context.dict[str(item)].local_intersect(context.dict[str(r)])

@when("{list:ListName} ← intersect({item:TestObject}, {r:TestRay})")
def step_group_intersect_list_is_group_intersect(context, list, item, r):
    assert(item in context.dict.keys())
    assert(r in context.dict.keys())
    context.dict[str(list)] = context.dict[str(item)].intersect(context.dict[str(r)])


@when("add_child({g:TestObject}, {s:TestObject})")
def step_group_when_add_child(context, g, s):
    assert(s in context.dict.keys())
    assert(g in context.dict.keys())
    context.dict[str(g)].add_child(context.dict[str(s)])
    
    
@then("{s:TestObject}.transform = identity_matrix")
def step_group_default_transform_is_identity(context, s):
    assert (s in context.dict.keys())
    default_transform = np.identity(4, dtype=np.float32)
    assert(np.array_equal(context.dict[str(s)].transform, default_transform))

@then("{s:TestObject} is empty")
def step_group_default_members_is_empty(context, s):
    assert (s in context.dict.keys())
    members = context.dict[str(s)].members
    assert(len(members)==0)


@then("{s:TestObject} is not empty")
def step_group_default_members_is_not_empty(context, s):
    assert (s in context.dict.keys())
    members = context.dict[str(s)].members
    assert(len(members)!=0)


@then("{g:TestObject} includes {s:TestObject}")
def step_group_contains_member(context, g, s):
    assert (g in context.dict.keys())
    assert (s in context.dict.keys())
    assert(context.dict[str(s)] in context.dict[str(g)].members)

@then("{s:TestObject}.parent = {g:TestObject}")
def step_group_contains_member(context, s, g):
    assert (g in context.dict.keys())
    assert (s in context.dict.keys())
    assert(context.dict[str(s)].parent == context.dict[str(g)])



