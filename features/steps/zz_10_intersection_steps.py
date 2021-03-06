from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light, glass_sphere
from base import hit, EPSILON, equal, World, render, translation, scaling, view_transform, intersection, intersections, prepare_computations,  world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *

valid_comps_elements = ["t", "object", "point", "eye_vector", "normal_vector", "inside", "under_point", "over_point"]
parse_comps_element = TypeBuilder.make_choice(valid_comps_elements)
register_type(CompsElement=parse_comps_element)

valid_intersection_elements = ["t", "object"]
parse_intersection_element = TypeBuilder.make_choice(valid_intersection_elements)
register_type(IntersectionElement=parse_intersection_element)


valid_equality_elements = ["<", ">"]
parse_equality_element = TypeBuilder.make_choice(valid_equality_elements)
register_type(TestEquality=parse_equality_element)

valid_test_objects = ["i", "comps", "i1", "i2", "i3", "i4"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_solids = ["s", "s2", "shape"]
parse_test_solid = TypeBuilder.make_choice(valid_test_solids)
register_type(TestSolid=parse_test_solid)

valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)

valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)


@given("{item:TestSolid} ← glass_sphere() with translation({x:g}, {y:g}, {z:g})")
def step_impl_glass_sphere_with_translate(context, item, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(item)] = glass_sphere(sphere_transform=translation(float(x), float(y), float(z)))


@given("{item:TestSolid} ← sphere()")
def step_impl_generic_solid_sphere(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = sphere()


@given("{item:TestObject} ← intersection(√{time:g}, {thing:TestSolid})")
def step_intersection_create_given_with_sqrt(context, item, time, thing):
    ensure_context_has_dict(context)
    context.dict[item] = intersection(math.sqrt(float(time)), context.dict[str(thing)])


@given("{item:TestObject} ← intersection({time:g}, {thing:TestSolid})")
def step_intersection_create_given(context, item, time, thing):
    ensure_context_has_dict(context)
    context.dict[item] = intersection(float(time), context.dict[str(thing)])


@given("{item1:ListName} ← intersections({item2:TestObject}, {item3:TestObject})")
def step_intersection_list_concatenate_given(context, item1, item2, item3):
    assert(item2 in context.dict.keys())
    assert(item3 in context.dict.keys())
    context.dict[item1] = intersections(context.dict[str(item2)], context.dict[str(item3)])


@given("{item1:ListName} ← intersections({item2:TestObject})")
def step_intersection_concatenate_single_given(context, item1, item2):
    assert(item2 in context.dict.keys())
    context.dict[item1] = intersections(context.dict[str(item2)])



@given("{item1:ListName} ← intersections({item2:TestObject}, {item3:TestObject}, {item4:TestObject}, {item5:TestObject})")
def step_intersection_list_concatenate_given(context, item1, item2, item3, item4, item5):
    assert(item2 in context.dict.keys())
    assert(item3 in context.dict.keys())
    assert(item4 in context.dict.keys())
    assert(item5 in context.dict.keys())
    context.dict[item1] = intersections(context.dict[str(item2)], context.dict[str(item3)], context.dict[str(item4)], context.dict[str(item5)])



@when("{item:TestObject} ← intersection({time:g}, {thing:TestSolid})")
def step_intersection_create_when(context, item, time, thing):
    ensure_context_has_dict(context)
    context.dict[item] = intersection(float(time), context.dict[str(thing)])


@when("{item:TestObject} ← prepare_computations({intersect:TestObject}, {ray:TestRay})")
def step_intersection_create_when(context, item, intersect, ray):
    ensure_context_has_dict(context)
    context.dict[str(item)] = prepare_computations(context.dict[str(intersect)], context.dict[str(ray)])

@when("{item:TestObject} ← prepare_computations({intersect:ListName}[0], {ray:TestRay}, {intersection_list:ListName})")
def step_intersection_create_when_ver2(context, item, intersect, ray, intersection_list):
    ensure_context_has_dict(context)
    context.dict[str(item)] = prepare_computations(context.dict[str(intersect)][0], context.dict[str(ray)], context.dict[str(intersection_list)])


@when("{item:TestObject} ← prepare_computations({intersect:ListName}[1], {ray:TestRay}, {intersection_list:ListName})")
def step_intersection_create_when_ver3(context, item, intersect, ray, intersection_list):
    ensure_context_has_dict(context)
    context.dict[str(item)] = prepare_computations(context.dict[str(intersect)][1], context.dict[str(ray)], context.dict[str(intersection_list)])



@when("{item:TestObject} ← prepare_computations({intersect:TestObject}, {ray:TestRay}, {intersection_list:ListName})")
def step_intersection_create_when_ver4(context, item, intersect, ray, intersection_list):
    ensure_context_has_dict(context)
    context.dict[str(item)] = prepare_computations(context.dict[str(intersect)], context.dict[str(ray)], context.dict[str(intersection_list)])



@when("{item1:ListName} ← intersections({item2:TestObject}, {item3:TestObject})")
def step_intersection_list_concatenate_when(context, item1, item2, item3):
    assert(item2 in context.dict.keys())
    assert(item3 in context.dict.keys())
    context.dict[item1] = intersections(context.dict[str(item2)], context.dict[str(item3)])


@when("{item:TestObject} ← hit({list:ListName})")
def step_find_hit_in_intersection_list(context, item, list):
    assert(list in context.dict.keys())
    context.dict[str(item)] = hit(context.dict[str(list)])



@then("{item1:TestObject} is nothing")
def step_hit_in_intersections_list_is_nothing(context, item1):
    assert (item1 in context.dict.keys())
    item1_object = context.dict[str(item1)]
    assert (item1_object == None)



@then("{item:TestObject}.{element:CompsElement} = false")
def step_comps_contains_element_value(context, item, element):
    assert(item in context.dict.keys())
    comps_object_str = "context.dict['"+str(item)+"']."+str(element)
    comps_object_element = eval(comps_object_str)
    assert(equal(comps_object_element, False))



@then("{item:TestObject}.{element:CompsElement} = true")
def step_comps_contains_element_value(context, item, element):
    assert(item in context.dict.keys())
    comps_object_str = "context.dict['"+str(item)+"']."+str(element)
    comps_object_element = eval(comps_object_str)
    assert(equal(comps_object_element, True))


@then("{item:TestObject}.{element:IntersectionElement} = {value:g}")
def step_intersection_contains_element(context, item, element, value):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    intersection_object = eval(local_object_str)
    test_value = float(value)
    assert(equal(intersection_object, test_value))



@then("{item:TestObject}.{element:IntersectionElement} = {value:TestSolid}")
def step_intersection_contains_element(context, item, element, value):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    intersection_object = eval(local_object_str)
    test_value = context.dict[str(value)]
    assert(intersection_object == test_value)


@then("{item1:TestObject}.{element1:CompsElement} = point({x:g}, {y:g}, {z:g})")
def step_comps_contains_element_A(context, item1, element1, x, y, z):
    assert (item1 in context.dict.keys())
    comps_object_str = "context.dict['" + str(item1) + "']." + str(element1)
    comps_object_element = eval(comps_object_str)
    point_value = point(float(x), float(y), float(z))
    assert (equal(comps_object_element, point_value))


@then("{item1:TestObject}.{element1:CompsElement} = vector({x:g}, {y:g}, -{z:g})")
def step_comps_contains_element_B(context, item1, element1, x, y, z):
    assert (item1 in context.dict.keys())
    comps_object_str = "context.dict['" + str(item1) + "']." + str(element1)
    comps_object_element = eval(comps_object_str)
    point_value = vector(float(x), float(y), -float(z))
    assert (equal(comps_object_element, point_value))


@then("{item1:TestObject}.{element1:CompsElement} = {item2:TestObject}.{element2:IntersectionElement}")
def step_comps_contains_element_C(context, item1, element1, item2, element2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.dict.keys())
    comps_object_str = "context.dict['"+str(item1)+"']."+str(element1)
    comps_object_element = eval(comps_object_str)
    intersection_object_str = "context.dict['"+str(item2)+"']."+str(element2)
    intersection_object_element = eval(intersection_object_str)
    assert(comps_object_element == intersection_object_element)


@then("{item1:TestObject} = {item2:TestObject}")
def step_intersections_are_equivalent_then(context, item1, item2):
    assert (item1 in context.dict.keys())
    assert (item2 in context.dict.keys())
    item1_object_str = "context.dict['" + str(item1) + "']"
    item1_object = eval(item1_object_str)
    item2_object_str = "context.dict['" + str(item2) + "']"
    item2_object = eval(item2_object_str)
    assert (item1_object == item2_object)


@then("{item1:TestObject}.{element1:CompsElement}.z < -EPSILON/2")
def step_comps_contains_element_B(context, item1, element1):
    assert (item1 in context.dict.keys())
    comps_object_str = "context.dict['" + str(item1) + "']." + str(element1) +".z"
    comps_object_element = eval(comps_object_str)
    epsilon_value = EPSILON
    assert (comps_object_element < (-epsilon_value/2))


@then("{item1:TestObject}.{element1:CompsElement}.z > EPSILON/2")
def step_comps_contains_element_B(context, item1, element1):
    assert (item1 in context.dict.keys())
    comps_object_str = "context.dict['" + str(item1) + "']." + str(element1) + ".z"
    comps_object_element = eval(comps_object_str)
    epsilon_value = EPSILON
    assert (comps_object_element > (epsilon_value / 2))


@then("{item1:TestObject}.{element1:CompsElement}.z {equality_test:TestEquality} comps.{element2:CompsElement}.z")
def step_comps_contains_element_B(context, item1, element1, equality_test, element2):
    assert (item1 in context.dict.keys())
    assert ("comps" in context.dict.keys())
    assert (equality_test in valid_equality_elements)
    item1_object_str = "context.dict['" + str(item1) + "']." + str(element1)
    item1_object_element = eval(item1_object_str).z
    item2_object_element = context.dict['comps'].__dict__[str(element2)].z
    if equality_test == "<":
        assert (item1_object_element < item2_object_element)
    elif equality_test == ">":
        assert (item1_object_element > item2_object_element)
    else:
        print("Unrecognized equality test ", equality_test)
        assert(False)
        
