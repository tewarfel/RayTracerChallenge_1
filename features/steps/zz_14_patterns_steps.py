from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3, is_vec3
from vec4 import Vec4, point, vector
from base import equal
import numpy as np
from shape import material, sphere, test_shape, point_light, plane
from base import render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from base import stripe_pattern, test_pattern, gradient_pattern, ring_pattern, checkers_pattern

from parse_type import TypeBuilder
from step_helper import *

valid_test_patterns = ["pattern"]
parse_test_pattern = TypeBuilder.make_choice(valid_test_patterns)
register_type(TestPattern=parse_test_pattern)

valid_pattern_elements = ["a", "b"]
parse_pattern_element = TypeBuilder.make_choice(valid_pattern_elements)
register_type(PatternElement=parse_pattern_element)


valid_test_solids = ["object","shape"]
parse_test_solid = TypeBuilder.make_choice(valid_test_solids)
register_type(TestSolid=parse_test_solid)

valid_test_variables = ["c", "black", "white"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)


@given("{item:TestVariable} ← color({red:g}, {green:g}, {blue:g})")
def step_set_background_color(context, item, red, green, blue):
    ensure_context_has_tuple(context)
    context.tuple[str(item)] = color(float(red), float(green), float(blue))


@given("{item:TestPattern} ← stripe_pattern({color1:TestVariable}, {color2:TestVariable})")
def step_set_background_color(context, item, color1, color2):
    ensure_context_has_dict(context)
    assert(color1 in context.tuple.keys())
    assert(color2 in context.tuple.keys())
    context.dict[str(item)] = stripe_pattern(context.tuple[str(color1)],
                                             context.tuple[str(color2)])

@given("{item:TestPattern} ← gradient_pattern({color1:TestVariable}, {color2:TestVariable})")
def step_set_background_color(context, item, color1, color2):
    ensure_context_has_dict(context)
    assert(color1 in context.tuple.keys())
    assert(color2 in context.tuple.keys())
    context.dict[str(item)] = gradient_pattern(context.tuple[str(color1)],
                                             context.tuple[str(color2)])


@given("{item:TestPattern} ← ring_pattern({color1:TestVariable}, {color2:TestVariable})")
def step_set_background_color(context, item, color1, color2):
    ensure_context_has_dict(context)
    assert (color1 in context.tuple.keys())
    assert (color2 in context.tuple.keys())
    context.dict[str(item)] = ring_pattern(context.tuple[str(color1)],
                                               context.tuple[str(color2)])


@given("{item:TestPattern} ← checkers_pattern({color1:TestVariable}, {color2:TestVariable})")
def step_set_background_color(context, item, color1, color2):
    ensure_context_has_dict(context)
    assert (color1 in context.tuple.keys())
    assert (color2 in context.tuple.keys())
    context.dict[str(item)] = checkers_pattern(context.tuple[str(color1)],
                                               context.tuple[str(color2)])


@given("{item:TestSolid} ← sphere()")
def step_impl_generic_solid_sphere_for_pattern(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = sphere()


@given("set_transform({item:TestSolid}, scaling({x:g}, {y:g}, {z:g}))")
def step_set_scaling_transform_for_solid_for_pattern(context, item, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(item)].set_transform(scaling(float(x), float(y), float(z)))


@given("set_pattern_transform({pattern:TestPattern}, scaling({x:g}, {y:g}, {z:g}))")
def step_set_scaling_transform_for_pattern_itself(context, pattern, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(pattern)].set_transform(scaling(float(x), float(y), float(z)))


@given("set_pattern_transform({pattern:TestPattern}, translation({x:g}, {y:g}, {z:g}))")
def step_set_translation_transform_for_pattern_itself(context, pattern, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(pattern)].set_transform(translation(float(x), float(y), float(z)))


@given("set_transform({solid:TestSolid}, scaling({x:g}, {y:g}, {z:g}))")
def step_set_scaling_transform_for_solid_3(context, solid, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(solid)].set_transform(scaling(float(x), float(y), float(z)))


@given("{item:TestPattern} ← test_pattern()")
def step_impl_generic_test_pattern(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = test_pattern()


@when("{color:TestVariable} ← stripe_at_object({pattern:TestPattern}, {item:TestSolid}, point({x:g}, {y:g}, {z:g}))")
def step_when_color_is_stripe_at_object_at_point(context, color, pattern, item, x, y, z):
    assert(pattern in context.dict.keys())
    assert(item in context.dict.keys())
    ensure_context_has_tuple(context)
    test_pattern = context.dict[str(pattern)]
    test_object = context.dict[str(item)]
    test_point = point(float(x), float(y), float(z))
    context.tuple[str(color)] = test_pattern.pattern_at_shape(test_object, test_point)


@when("set_pattern_transform({pattern:TestPattern}, translation({x:g}, {y:g}, {z:g}))")
def step_when_set_pattern_transform_translation(context, pattern, x, y, z):
    assert(pattern in context.dict.keys())
    test_pattern = context.dict[str(pattern)]
    test_pattern.set_transform(translation(float(x), float(y), float(z)))


@when("{color:TestVariable} ← pattern_at_shape({pattern:TestPattern}, {item:TestSolid}, point({x:g}, {y:g}, {z:g}))")
def step_when_color_is_pattern_at_shape_at_point(context, color, pattern, item, x, y, z):
    assert(pattern in context.dict.keys())
    assert(item in context.dict.keys())
    ensure_context_has_tuple(context)
    test_pattern = context.dict[str(pattern)]
    test_object = context.dict[str(item)]
    test_point = point(float(x), float(y), float(z))
    context.tuple[str(color)] = test_pattern.pattern_at_shape(test_object, test_point)


@then("pattern_at({item_pattern:TestPattern}, point({x:g}, {y:g}, {z:g})) = color({red:g}, {green:g}, {blue:g})")
def step_then_pattern_at_has_local_color_equals_specific(context, item_pattern, x, y, z, red, green, blue):
    assert(item_pattern in context.dict.keys())
    test_pattern = context.dict[str(item_pattern)]
    test_color = test_pattern.pattern_at_shape(sphere(), point(float(x), float(y), float(z)))
    color_value = color(float(red), float(green), float(blue))
    assert(equal(test_color, color_value))


@then("stripe_at({item_pattern:TestPattern}, point({x:g}, {y:g}, {z:g})) = {color:TestVariable}")
def step_then_local_color_on_pattern_equals(context, item_pattern, x, y, z, color):
    assert(item_pattern in context.dict.keys())
    test_pattern = context.dict[str(item_pattern)]
    test_color = test_pattern.pattern_at_shape(sphere(), point(float(x), float(y), float(z)))
    color_value = context.tuple[str(color)]
    assert(equal(test_color, color_value))


@then("pattern_at({item_pattern:TestPattern}, point({x:g}, {y:g}, {z:g})) = {color:TestVariable}")
def step_then_pattern_at_has_local_color_equals(context, item_pattern, x, y, z, color):
    assert(item_pattern in context.dict.keys())
    test_pattern = context.dict[str(item_pattern)]
    test_color = test_pattern.pattern_at_shape(sphere(), point(float(x), float(y), float(z)))
    color_value = context.tuple[str(color)]
    assert(equal(test_color, color_value))


@then("{item_pattern:TestPattern}.{pattern_element:PatternElement} = {color:TestVariable}")
def step_then_pattern_color_definition_is(context, item_pattern, pattern_element, color):
    assert(item_pattern in context.dict.keys())
    local_value = context.dict[str(item_pattern)].__dict__[str(pattern_element)]
    assert(equal(local_value, context.tuple[str(color)]))
    

@then("{item:TestVariable} = {color:TestVariable}")
def step_then_variable_equals_named_vec3_value(context, item, color):
    assert(item in context.tuple.keys())
    assert(color in context.tuple.keys())
    local_color = context.tuple[str(item)]
    named_color = context.tuple[str(color)]
    assert(equal(local_color, named_color))


@then("{item_pattern:TestPattern}.transform = identity_matrix")
def step_then_pattern_default_transform_is_identity(context, item_pattern):
    assert (item_pattern in context.dict.keys())
    local_value = context.dict[str(item_pattern)].transform
    assert (equal(local_value, np.identity(4, dtype=float)))


@then("{item_pattern:TestPattern}.transform = translation({x:g}, {y:g}, {z:g})")
def step_then_pattern_default_transform_is_identity(context, item_pattern, x, y, z):
    assert (item_pattern in context.dict.keys())
    local_value = context.dict[str(item_pattern)].transform
    assert (equal(local_value, translation(float(x), float(y), float(z))))

    