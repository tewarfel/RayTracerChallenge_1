from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np
from step_helper import *

valid_test_variables = ["c", "c1", "c2"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_color_extensions = ["red", "green", "blue"]
parse_color_extension = TypeBuilder.make_choice(valid_color_extensions)
register_type(ColorExt=parse_color_extension)

valid_test_scalar_operations = ["*", "/", "+", "-"]
parse_test_scalar_operation = TypeBuilder.make_choice(valid_test_scalar_operations)
register_type(TestScalarOperation=parse_test_scalar_operation)

valid_test_add_operations = ["+", "-"]
parse_test_add_operation = TypeBuilder.make_choice(valid_test_add_operations)
register_type(TestAddOperation=parse_test_add_operation)



@then("{item:TestVariable}.{part:ColorExt} = {value:g}")
def step_then_part_equals_value(context, item, part, value):
    assert part in valid_color_extensions
    item_string = 'context.tuple["' +str(item) + '"].' + str(part)
    assert_that(eval(item_string), equal_to(float(value)))


@then("{item1:TestVariable} + {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_vec_add_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "base.vec3(float(" + str(r) + "), float(" + str(g) + "), float(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(base.equal(eval(estring), (context.tuple[item1] + context.tuple[item2])))

@then("{item1:TestVariable} * {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_color_mult_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "base.vec3(float(" + str(r) + "), float(" + str(g) + "), float(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(base.equal(eval(estring), (context.tuple[item1] * context.tuple[item2])))


@then("{item1:TestVariable} - {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_vec_sub_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "base.vec3(float(" + str(r) + "), float(" + str(g) + "), float(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(base.equal(eval(estring), (context.tuple[item1] - context.tuple[item2])))


@then("{item1:TestVariable} * {item2:g} = color({r:g}, {g:g}, {b:g})")
def step_then_scalar_multiply_equals(context, item1,  item2, r, g, b):
    if isinstance(item2,float) or isinstance(item2, int):
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        item_string = 'context.tuple["' + str(item1) + '"]'
        assert_that(base.color(float(r), float(g), float(b)).__eq__(context.tuple[item1] * float(item2)))


@then("{item1:TestVariable} / {item2:g} = color({r:g}, {g:g}, {b:g})")
def step_then_scalar_divide_equals(context, item1, item2, r, g, b):
    if isinstance(item2, float) or isinstance(item2, int):
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        item_string = 'context.tuple["' + str(item1) + '"]'
        operand1 = eval(item_string)
        assert_that(base.color(r, g, b).__eq__(context.tuple[item1] / float(item2)))


@given("{item:TestVariable} ← color({x:g}, {y:g}, {z:g})")
def step_impl_color(context,item,x,y,z):
    ensure_context_has_tuple(context)
    context.tuple[item] = base.Vec3(float(x), float(y), float(z))

    
    
