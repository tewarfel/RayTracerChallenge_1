from behave import *
from hamcrest import assert_that, equal_to
from parse_type import TypeBuilder
from memblock import *
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


@given("{item:TestVariable} ← color({x:g}, {y:g}, {z:g})")
def step_impl_color(context, item, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = Vec3(np.float32(x), np.float32(y), np.float32(z))


@then("{item:TestVariable}.{part:ColorExt} = {value:g}")
def step_then_part_equals_value(context, item, part, value):
    assert part in valid_color_extensions
    item_string = 'context.tuple["' +str(item) + '"].' + str(part)
    assert_that(equal(eval(item_string), np.float32(value)))


@then("{item1:TestVariable} + {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_vec_add_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "Vec3(np.float32(" + str(r) + "), np.float32(" + str(g) + "), np.float32(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(equal(eval(estring), (context.tuple[item1] + context.tuple[item2])))

@then("{item1:TestVariable} * {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_color_mult_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "Vec3(np.float32(" + str(r) + "), np.float32(" + str(g) + "), np.float32(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(equal(eval(estring), (context.tuple[item1] * context.tuple[item2])))


@then("{item1:TestVariable} - {item2:TestVariable} = color({r:g}, {g:g}, {b:g})")
def step_then_vec_sub_equals(context, item1, item2, r, g, b):
    if item2 in valid_test_variables:
        estring = "Vec3(np.float32(" + str(r) + "), np.float32(" + str(g) + "), np.float32(" + str(b) + "))"
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        assert_that(item2 in context.tuple.keys(), equal_to(True))
        assert_that(equal(eval(estring), (context.tuple[item1] - context.tuple[item2])))


@then("{item1:TestVariable} * {item2:g} = color({r:g}, {g:g}, {b:g})")
def step_then_scalar_multiply_equals(context, item1,  item2, r, g, b):
    if isinstance(item2,float) or isinstance(item2, int):
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        item_string = 'context.tuple["' + str(item1) + '"]'
        assert_that(color(np.float32(r), np.float32(g), np.float32(b)).__eq__(context.tuple[item1] * np.float32(item2)))


@then("{item1:TestVariable} / {item2:g} = color({r:g}, {g:g}, {b:g})")
def step_then_scalar_divide_equals(context, item1, item2, r, g, b):
    if isinstance(item2, float) or isinstance(item2, int):
        assert_that(item1 in context.tuple.keys(), equal_to(True))
        item_string = 'context.tuple["' + str(item1) + '"]'
        operand1 = eval(item_string)
        assert_that(color(r, g, b).__eq__(context.tuple[item1] / np.float32(item2)))


    
