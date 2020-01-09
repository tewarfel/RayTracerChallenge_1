from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np
from step_helper import *


valid_test_variables = ["c", "c1", "c2", "c3", "red"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_color_extensions = ["red", "green", "blue"]
parse_color_extension = TypeBuilder.make_choice(valid_color_extensions)
register_type(ColorExt=parse_color_extension)

valid_components = ["width", "height", "background", "data"]
parse_valid_component = TypeBuilder.make_choice(valid_components)
register_type(CanvasComponent=parse_valid_component)


@given(u'{item:TestVariable} ← canvas({width:g}, {height:g})')
def step_impl_generic_canvas(context, item, width, height):
    ensure_context_has_dict(context)
    context.dict[item] = base.canvas(int(width), int(height))
    
    
@then("{item:TestVariable}.{part:CanvasComponent} = {value:g}")
def step_then_component_equals_value(context, item, part, value):
    assert part in valid_components
    item_string = 'context.dict["' +str(item) + '"].' + str(part)
    assert_that(eval(item_string), equal_to(float(value)))


@then("every pixel of {item:TestVariable} is color({r:g}, {g:g}, {b:g})")
def step_then_component_equals_value(context, item, r, g, b):
    assert item in valid_test_variables
    item_string = 'context.dict["' +str(item) + '"].data'
    RGB_matrix = eval(item_string)
    R_match = (RGB_matrix[0, :, :] == r)
    G_match = (RGB_matrix[1, :, :] == g)
    B_match = (RGB_matrix[2, :, :] == b)
    assert(np.all(R_match) and np.all(G_match) and np.all(B_match))


@given("{item:TestVariable} ← color({x:g}, {y:g}, {z:g})")
def step_impl_color(context, item, x, y, z):
    ensure_context_has_dict(context)
    context.dict[item] = base.Vec3(float(x), float(y), float(z))


@when("write_pixel({item:TestVariable}, {x:g}, {y:g}, {color_var})")
def step_impl_when_write_pixel(context, item, x, y, color_var):
    assert(item in context.dict)
    assert(color_var in context.dict)
    base.write_pixel(context.dict[item], x, y, context.dict[color_var])


@then("pixel_at({item:TestVariable}, {x:g}, {y:g}) = {color_var}")
def step_impl_then_pixel_at(context, item, x, y, color_var):
    assert(item in context.dict)
    assert(color_var in context.dict)
    item_string = 'context.dict["' +str(item) + '"].data'
    RGB_matrix = eval(item_string)
    color_value = eval("context.dict['" + color_var + "']")
    assert(RGB_matrix[0, int(y), int(x)] == color_value.red)
    assert(RGB_matrix[1, int(y), int(x)] == color_value.green)
    assert(RGB_matrix[2, int(y), int(x)] == color_value.blue)
    

