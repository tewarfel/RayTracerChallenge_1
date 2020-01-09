from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector, is_point, is_vector, vec4
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light, glass_sphere
from base import hit, EPSILON, equal, World, render, translation, magnitude, normalize, dot, cross, reflect, scaling, view_transform, intersection, intersections, prepare_computations,  world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *


valid_vec4_extensions = ["x", "y", "z", "w"]
parse_vec4_extension = TypeBuilder.make_choice(valid_vec4_extensions)
register_type(Vec4Ext=parse_vec4_extension)

valid_test_variables = ["v", "v1", "v2", "p", "a", "b", "zero", "norm", "n", "r"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

#valid_test_scalar_operations = ["*", "/"]
#parse_test_scalar_operation = TypeBuilder.make_choice(valid_test_scalar_operations)
#register_type(TestScalarOperation=parse_test_scalar_operation)

@given("{item:TestVariable} ← tuple({x}, {y}, {z}, {w})")
def step_impl_generic_tuple(context,item,x,y,z,w):
    ensure_context_has_tuple(context)
    context.tuple[item] = Vec4(float(x), float(y), float(z), float(w))



@given(u'{item:TestVariable} ← point({x:g}, {y:g}, {z:g})')
def step_impl_generic_point(context,item, x,y,z):
    ensure_context_has_tuple(context)
    context.tuple[item] = point(float(x), float(y), float(z))
    
    
@given(u'{item:TestVariable} ← vector(√{x_numerator:g}/{x_denom:g}, √{y_numerator:g}/{y_denom:g}, {z:g})')
def step_impl_generic_vector_A(context, item, x_numerator, x_denom, y_numerator, y_denom, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(np.sqrt(float(x_numerator)) / float(x_denom), np.sqrt(float(y_numerator)) / float(y_denom), float(z))


@given(u'{item:TestVariable} ← vector({x:g}, {y:g}, {z:g})')
def step_impl_generic_vector_B(context, item, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(float(x), float(y), float(z))


@when("{item:TestVariable} ← normalize({v:TestVariable})")
def step_impl_when_generic_vector(context, item, v):
    try:
        if (context.tuple is None):
            assert(False)
        else:
            if v in context.tuple.keys():
                context.tuple[item] = normalize(context.tuple[eval(v)])
            else:
                print(context.tuple.keys())
                assert(False)
    except:
        assert(False)


@when("{item:TestVariable} ← reflect({v:TestVariable}, {n:TestVariable})")
def step_impl_when_generic_vector_reflected(context, item, v, n):
    ensure_context_has_tuple(context)
    v_value = context.tuple[str(v)]
    n_value = context.tuple[str(n)]
    context.tuple[str(item)] = reflect(v_value, n_value)




@then("{item:TestVariable}.{part:Vec4Ext} = {value:g}")
def step_then_part_equals_value(context, item, part, value):
    assert(part in valid_vec4_extensions)
    item_string = 'context.tuple["' +str(item) + '"].' + str(part)
    assert_that(eval(item_string), equal_to(float(value)))

    
@then(u'{item:TestVariable} is a {thing}')
def step_then_item_is_thing(context, item, thing):
    estring = "is_" + str(thing) + "(context.tuple['"+str(item)+"'])"
    assert_that(eval(estring), equal_to(True))

@then("dot({item1:TestVariable}, {item2:TestVariable}) = {value}")
def step_then_dot_product_is_value(context, item1, item2, value):
    estring = "dot(context.tuple['"+str(item1)+"'], context.tuple['"+str(item2)+"'])"
    assert_that(eval(estring), equal_to(float(value)))


@then(u'{item:TestVariable} is not a {thing}')
def step_then_item_is_thing(context, item, thing):
    estring = "is_" + str(thing) + "(context.tuple['" + str(item) + "'])"
    assert_that(eval(estring), equal_to(False))


@then(u'{item1}{index1} + {item2}{index2} = tuple({x},{y},{z},{w})')
def step_then_tuple_sum(context, item1, index1, item2, index2, x, y, z, w):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), float(" + str(w) + "))"
    i1 = context.tuple[str(item1)+str(int(index1))]
    i2 = context.tuple[str(item2)+str(int(index2))]
    new_item = vec4(i1.x + i2.x, i1.y + i2.y, i1.z + i2.z, i1.w + i2.w)
    assert_that(eval(estring), equal_to(new_item))
    assert_that((i1+i2), equal_to(new_item))

@then(u'{item:TestVariable} = tuple({x},{y},{z},{w})')
def step_then_item_is_tuple(context, item, x,y,z,w):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), float(" + str(w)+"))"
    assert_that(item in context.tuple.keys(), equal_to(True))
    assert_that(eval(estring), equal_to(context.tuple[item]))


@then(u'-{item:TestVariable} = tuple({x},{y},{z},{w})')
def step_then_item_is_tuple(context, item, x, y, z, w):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), float(" + str(w) + "))"
    assert_that(item in context.tuple.keys(), equal_to(True))
    assert_that(-eval(estring), equal_to(context.tuple[item]))



@given(u'{variable}{index} ← tuple({x},{y},{z},{w})')
def step_impl_indexed_tuple(context, variable, index, x,y,z,w):
    ensure_context_has_tuple(context)
    
    assignment_string = "context.tuple." + str(variable)+str(int(index))
    value_string = estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), float(" + str(w)+"))"
    context.tuple[str(variable)+str(int(index))] = eval(value_string)


@given("{variable:TestVariable}{index:g} ← point({x},{y},{z})")
def step_impl_indexed_point(context, variable, index, x, y, z):
    ensure_context_has_tuple(context)
    
    assignment_string = "context.tuple." + str(variable) + str(int(index))
    value_string = estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), 1)"
    context.tuple[str(variable) + str(int(index))] = eval(value_string)



@then(u'{item1} - {item2} = point({x},{y},{z})')
def step_then_vect_sub(context, item1, item2, x, y, z):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(float(z)) + "), 1.0)"
    i1 = context.tuple[str(item1)]
    i2 = context.tuple[str(item2)]
    new_item = vec4(i1.x - i2.x, i1.y - i2.y, i1.z - i2.z, i1.w - i2.w)
    assert_that(eval(estring), equal_to(new_item))
    assert_that((i1 - i2), equal_to(new_item))


@then(u'{item1} - {item2} = vector({x},{y},{z})')
def step_then_vect_sub_zero(context, item1, item2, x, y, z):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(float(z)) + "), 0)"
    i1 = context.tuple[str(item1)]
    i2 = context.tuple[str(item2)]
    new_item = vec4(i1.x - i2.x, i1.y - i2.y, i1.z - i2.z, i1.w - i2.w)
    assert_that(eval(estring), equal_to(new_item))
    assert_that((i1 - i2), equal_to(new_item))

@then("magnitude({item:TestVariable}) = √{value}")
def step_then_magnitude_equals(context, item, value):
    v = context.tuple[str(item)]
    mag_v = magnitude(v)
    assert_that(mag_v, equal_to(np.sqrt(float(value))))

@then("magnitude({item:TestVariable}) = {value}")
def step_then_magnitude_equals(context, item, value):
    v = context.tuple[str(item)]
    mag_v = magnitude(v)
    assert_that(mag_v, equal_to(float(value)))

@then("{item:TestVariable} {operation} {scalar:g} = tuple({x},{y},{z},{w})")
def step_then_item_is_tuple2(context, item, operation, scalar, x,y,z,w):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(z) + "), float(" + str(w)+"))"
    assert_that(item in context.tuple.keys(), equal_to(True))
    operand = float(scalar)
    if operation == "*":
        assert_that(eval(estring), equal_to(context.tuple[item] * operand))
    elif operation == "/":
        assert_that(eval(estring), equal_to(context.tuple[item] / operand))
    else:
        assert_that(False)

@then("normalize({item:TestVariable}) = vector({x},{y},{z})")
def step_then_magnitude_equals(context, item, x,y,z):
    v = context.tuple[str(item)]
    norm_v = normalize(v)
    assert_that(norm_v, equal_to(vector(float(x), float(y), float(z))))
    
@then("normalize({item:TestVariable}) = approximately vector({x},{y},{z})")
def step_then_magnitude_equals(context, item, x,y,z):
    v = context.tuple[str(item)]
    norm_v = normalize(v)
    assert_that(equal(norm_v.x, float(x)))
    assert_that(equal(norm_v.y, float(y)))
    assert_that(equal(norm_v.z, float(z)))
    assert_that(equal(norm_v.w, 0))
    
@then("cross({item1:TestVariable}, {item2:TestVariable}) = vector({x},{y},{z})")
def step_then_cross_product_is_value(context, item1, item2, x,y,z):
    estring = "cross(context.tuple['"+str(item1)+"'], context.tuple['"+str(item2)+"'])"
    assert_that(eval(estring), equal_to(vector(float(x), float(y), float(z))))


@then("{item:TestVariable} = vector(√{xnum:g}/{xdenom:g}, √{ynum:g}/{ydenom:g}, √{znum:g}/{zdenom:g})")
def step_then_vect_result_sqrt_rational(context, item, xnum, xdenom, ynum, ydenom, znum, zdenom):
    value = vec4(np.sqrt(float(xnum)) / float(xdenom), np.sqrt(float(ynum)) / float(ydenom), np.sqrt(float(znum)) / float(zdenom), 0.0)
    i1 = context.tuple[str(item)]
    assert(equal(value, i1))





@then("{item:TestVariable} = vector({x},{y},{z})")
def step_then_vect_result(context, item, x, y, z):
    estring = "vec4(float(" + str(x) + "), float(" + str(y) + "), float(" + str(float(z)) + "), 0.0)"
    i1 = context.tuple[str(item)]
    assert(equal(eval(estring), i1))

