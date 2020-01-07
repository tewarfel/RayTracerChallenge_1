from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np


valid_test_objects = ["light","m", "in_shadow"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["intensity", "position", "eyev", "normalv", "result"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_light_elements = ["position", "intensity"]
parse_light_element = TypeBuilder.make_choice(valid_light_elements)
register_type(LightElement=parse_light_element)

valid_material_elements = ["color", "ambient", "diffuse", "specular", "shininess", "reflective", "transparency", "refractive_index"]
parse_material_element = TypeBuilder.make_choice(valid_material_elements)
register_type(MaterialElement=parse_material_element)


@given("{item:TestVariable} ← color({r:g}, {g:g}, {b:g})")
def step_impl_color_assign(context, item, r, g, b):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.color(float(r), float(g), float(b))


@given("{item:TestVariable} ← point({x:g}, {y:g}, {z:g})")
def step_impl_point_assign_B(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.point(float(x), float(y), float(z))



@given("{item:TestObject} ← true")
def step_impl_logic_assign_true(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = True




@given("{item:TestVariable} ← vector({x:g}, √{ynum:g}/{ydenom:g}, -√{znum:g}/{zdenom:g})")
def step_impl_vector_assign_B(context, item, x, ynum, ydenom, znum, zdenom):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), np.sqrt(float(ynum)) / float(ydenom), -np.sqrt(float(znum)) / float(zdenom))
    

@given("{item:TestVariable} ← vector({x:g}, {y:g}, -{z:g})")
def step_impl_vector_assign_C(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), float(y), -float(z))


@given("{item:TestVariable} ← vector({x:g}, {y:g}, {z:g})")
def step_impl_vector_assign_D(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), float(y), float(z))


@given("{item:TestVariable} ← vector({x:g}, -√{ynum:g}/{ydenom:g}, -√{znum:g}/{zdenom:g})")
def step_impl_vector_assign_E(context, item, x, ynum, ydenom, znum, zdenom):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), -np.sqrt(float(ynum)) / float(ydenom),
                                          -np.sqrt(float(znum)) / float(zdenom))


@given("{item:TestObject} ← material()")
def step_impl_generic_material_given(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.material()



@given("{item:TestObject} ← point_light(point({px:g}, {py:g}, {pz:g}), color({red:g}, {green:g}, {blue:g}))")
def step_impl_point_light_for_materials(context, item, px, py, pz, red, green, blue):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    real_position = base.point(float(px), float(py), float(pz))
    real_intensity = base.color(float(red), float(green), float(blue))
    context.dict[item] = base.point_light(real_position, real_intensity)





@when("{item:TestVariable} ← lighting({material:TestObject}, {light:TestObject}, {point_position:TestVariable}, {eye_vector:TestVariable}, {normal_vector:TestVariable})")
def step_set_lighting_values(context, item, material, light, point_position, eye_vector, normal_vector):
    assert(material in context.dict.keys())
    assert(light in context.dict.keys())
    assert(point_position in context.tuple.keys())
    assert(eye_vector in context.tuple.keys())
    assert(normal_vector in context.tuple.keys())
    material_val = context.dict[str(material)]
    light_val = context.dict[str(light)]
    point_value = context.tuple[str(point_position)]
    eye_vec_value = context.tuple[str(eye_vector)]
    norm_vec_value = context.tuple[str(normal_vector)]
    lighting_value = base.lighting(material_val, light_val, point_value, eye_vec_value, norm_vec_value)
    context.tuple[str(item)] = lighting_value



@when("{item:TestVariable} ← lighting({material:TestObject}, {light:TestObject}, {point_position:TestVariable}, {eye_vector:TestVariable}, {normal_vector:TestVariable}, {in_shadow:TestObject})")
def step_set_lighting_values_with_shadow(context, item, material, light, point_position, eye_vector, normal_vector, in_shadow):
    assert (material in context.dict.keys())
    assert (light in context.dict.keys())
    assert (point_position in context.tuple.keys())
    assert (eye_vector in context.tuple.keys())
    assert (normal_vector in context.tuple.keys())
    assert (in_shadow in context.dict.keys())
    material_val = context.dict[str(material)]
    light_val = context.dict[str(light)]
    point_value = context.tuple[str(point_position)]
    eye_vec_value = context.tuple[str(eye_vector)]
    norm_vec_value = context.tuple[str(normal_vector)]
    in_shadow_value = context.dict[str(in_shadow)]
    lighting_value = base.lighting(material_val, light_val, point_value, eye_vec_value, norm_vec_value, in_shadow_value)
    context.tuple[str(item)] = lighting_value






@then("{item:TestObject}.{element:MaterialElement} = color({red:g}, {green:g}, {blue:g})")
def step_impl_ray_intersect_list_count(context, item, element, red, green, blue):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    local_object = eval(local_object_str)
    value = base.color(float(red), float(green), float(blue))
    assert(base.equal(local_object, value))


@then("{item:TestObject}.{element:MaterialElement} = {value:g}")
def step_impl_ray_intersect_list_count(context, item, element, value):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    local_object = eval(local_object_str)
    value = float(value)
    assert(base.equal(local_object, value))


@then("{item:TestVariable} = color({red:g}, {green:g}, {blue:g})")
def step_lighting_color_test(context, item, red, green, blue):
    assert(item in context.tuple.keys())
    local_object_str = "context.tuple['"+str(item)+"']"
    local_object = eval(local_object_str)
    value = base.color(float(red), float(green), float(blue))
    assert(base.equal(local_object, value))
