from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np


valid_test_matrices = ["M", "m", "A", "B", "C", "transform", "inv", "half_quarter", "full_quarter", "T", "t"]
parse_test_matrix = TypeBuilder.make_choice(valid_test_matrices)
register_type(TestMatrix=parse_test_matrix)

valid_vec4_extensions = ["x", "y", "z", "w"]
parse_vec4_extension = TypeBuilder.make_choice(valid_vec4_extensions)
register_type(Vec4Ext=parse_vec4_extension)

valid_test_variables = ["v", "p", "p2", "p3", "p4", "from", "to", "up"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)


#@given(u'{item:TestVariable} ← point({x:g}, {y:g}, {z:g})')
#def step_impl_generic_point(context, item, x, y, z):
#    try:
#        if (context.tuple is None):
#            context.tuple = {}
#    except:
#        context.tuple = {}
#    context.tuple[item] = base.point(float(x), float(y), float(z))


@given(u'{item:TestVariable} ← vector({x:g}, {y:g}, {z:g})')
def step_impl_generic_vector(context, item, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[item] = base.vector(float(x), float(y), float(z))


@given("{item:TestMatrix} ← translation({x:g}, {y:g}, {z:g})")
def step_impl_generic_translation_matrix(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.translation(float(x), float(y), float(z))


@given("{item:TestMatrix} ← scaling({x:g}, {y:g}, {z:g})")
def step_impl_generic_scaling_matrix(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.scaling(float(x), float(y), float(z))


@given("{item1:TestMatrix} ← inverse(transform)")
def step_given_matrix_is_inv_transform(context, item1):
    assert("transform" in context.dict.keys())
    context.dict[str(item1)] = base.inverse(context.dict["transform"])


@given("{item1:TestMatrix} ← shearing({xy:g}, {xz:g}, {yx:g}, {yz:g}, {zx:g}, {zy:g})")
def step_given_matrix_is_shearing_transform(context, item1, xy, xz, yx, yz, zx, zy):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item1)] = base.shearing(xy, xz, yx, yz, zx, zy)


@given("{item:TestMatrix} ← rotation_x({numerator} / {denominator:g})")
def step_impl_rotation_x_rational(context, item, numerator, denominator):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    val_num = np.pi if str(numerator) == "π" else float(numerator)
    val_denom = float(denominator)
    context.dict[item] = base.rotation_x(val_num / val_denom)


@given("{item:TestMatrix} ← rotation_y({numerator} / {denominator:g})")
def step_impl_rotation_y_rational(context, item, numerator, denominator):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    val_num = np.pi if str(numerator) == "π" else float(numerator)
    val_denom = float(denominator)
    context.dict[item] = base.rotation_y(val_num / val_denom)


@given("{item:TestMatrix} ← rotation_z({numerator} / {denominator:g})")
def step_impl_rotation_z_rational(context, item, numerator, denominator):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    val_num = np.pi if str(numerator) == "π" else float(numerator)
    val_denom = float(denominator)
    context.dict[item] = base.rotation_z(val_num / val_denom)


@given("{variable:TestVariable} ← point({x:g}, {y:g}, {z:g})")
def step_impl_indexed_point2(context, variable, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[str(variable)] = base.point(float(x), float(y), float(z))


@given("{variable:TestVariable} ← point({x:g}, {y:g}, -{z:g})")
def step_impl_indexed_neg_point2(context, variable, x, y, z):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    context.tuple[str(variable)] = base.point(float(x), float(y), -float(z))


@when("{item1:TestVariable} ← {item2:TestMatrix} * {item3:TestVariable}")
def step_impl_when_generic_vector(context, item1, item2, item3):
    assert (item2 in context.dict.keys())
    assert (item3 in context.tuple.keys())
    A = context.dict[str(item2)]
    p = context.tuple[str(item3)]
    value = np.matmul(A, p)
    context.tuple[item1] = base.Vec4(value[0], value[1], value[2], value[3])




@when("{item1:TestMatrix} ← {item2:TestMatrix} * {item3:TestMatrix} * {item4:TestMatrix}")
def step_impl_when_generic_vector(context, item1, item2, item3, item4):
    assert(item2 in context.dict.keys())
    assert(item3 in context.dict.keys())
    assert(item4 in context.dict.keys())
    A = context.dict[str(item4)]
    B = context.dict[str(item3)]
    C = context.dict[str(item2)]
    context.dict[str(item1)] = np.matmul(C, np.matmul(B, A))


@when("{item1:TestMatrix} ← view_transform({item2:TestVariable}, {item3:TestVariable}, {item4:TestVariable})")
def step_impl_when_view_transform(context, item1, item2, item3, item4):
    assert(item2 in context.tuple.keys())
    assert(item3 in context.tuple.keys())
    assert(item4 in context.tuple.keys())
    vup = context.tuple[str(item4)]
    vto = context.tuple[str(item3)]
    vfrom = context.tuple[str(item2)]
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item1)] = base.view_transform(vfrom, vto, vup)


@then("{item1:TestMatrix} * {item2:TestVariable} = point({x:g}, {y:g}, {z:g})")
def step_then_matrix_mul_point_equals_point(context, item1, item2, x, y, z):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(x, y, z))
    assert (base.equal(result, pt2))

# with poxitive x-value
@then("{item1:TestMatrix} * {item2:TestVariable} = point(√{x_num:g}/{x_denom:g}, √{y_num:g}/{y_denom:g}, {z:g})")
def step_then_matrix_mul_point_equals_point(context, item1, item2, x_num, x_denom, y_num, y_denom, z):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(np.sqrt(x_num) / x_denom, np.sqrt(y_num) / y_denom, z))
    assert (base.equal(result, pt2))


# with negative x-value
@then("{item1:TestMatrix} * {item2:TestVariable} = point(-√{x_num:g}/{x_denom:g}, √{y_num:g}/{y_denom:g}, {z:g})")
def step_then_matrix_mul_neg_point_equals_point(context, item1, item2, x_num, x_denom, y_num, y_denom, z):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(-np.sqrt(x_num) / x_denom, np.sqrt(y_num) / y_denom, z))
    assert (base.equal(result, pt2))


# with negative Z value
@then("{item1:TestMatrix} * {item2:TestVariable} = point({x:g}, √{y_num:g}/{y_denom:g}, -√{z_num:g}/{z_denom})")
def step_then_matrix_mul_point_equals_neg_point(context, item1, item2, x, y_num, y_denom, z_num, z_denom):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(float(x), np.sqrt(float(y_num)) / float(y_denom), -np.sqrt(float(z_num)) / float(z_denom)))
    assert (base.equal(result, pt2))

# with positive Z value
@then("{item1:TestMatrix} * {item2:TestVariable} = point({x:g}, √{y_num:g}/{y_denom:g}, √{z_num:g}/{z_denom})")
def step_then_matrix_mul_point_equals_point(context, item1, item2, x, y_num, y_denom, z_num, z_denom):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(float(x), np.sqrt(float(y_num)) / float(y_denom), np.sqrt(float(z_num)) / float(z_denom)))
    assert (base.equal(result, pt2))


@then("{item1:TestMatrix} * {item2:TestVariable} = point(√{x_num:g}/{x_denom:g}, {y:g}, √{z_num:g}/{z_denom})")
def step_then_matrix_mul_point_equals_point2(context, item1, item2, x_num, x_denom, y, z_num, z_denom):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.point(np.sqrt(float(x_num)) / float(x_denom), float(y), np.sqrt(float(z_num)) / float(z_denom)))
    assert (base.equal(result, pt2))


@then("{item1:TestMatrix} * {item2:TestVariable} = vector({x:g}, {y:g}, {z:g})")
def step_then_matrix_mul_vector_equals_point(context, item1, item2, x, y, z):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(base.vector(x, y, z))
    assert (base.equal(result, pt2))


@then("{item1:TestMatrix} * {item2:TestVariable} = {item3:TestVariable}")
def step_then_matrix_mul_point_equals_point(context, item1, item2, item3):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    assert (item3 in context.tuple.keys())
    
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    pt = context.tuple[str(item2)]
    result = np.matmul(matrix1, pt)
    pt2 = np.array(context.tuple[str(item3)])
    assert (base.equal(result, pt2))


@then("{item1:TestVariable} = point({x:g}, -{y:g}, {z:g})")
def step_then_matrix_mul_point_equals_point(context, item1, x, y, z):
    assert (item1 in context.tuple.keys())
    ip1 = context.tuple[str(item1)]
    result = base.point(float(x), -float(y), float(z))
    assert (base.equal(ip1, result))


@then("{item1:TestVariable} = point({x:g}, {y:g}, {z:g})")
def step_then_matrix_mul_point_equals_point(context, item1, x, y, z):
    assert (item1 in context.tuple.keys())
    ip1 = context.tuple[str(item1)]
    result = base.point(float(x), float(y), float(z))
    assert (base.equal(ip1, result))


@then("{item:TestMatrix} = identity_matrix")
def step_then_matrix_is_identity(context, item):
    assert(item in context.dict.keys())
    t = context.dict[str(item)]
    height, width = t.shape
    assert(height==width)
    assert(base.equal(t, np.identity(height, dtype=float)))
    
    
@then("{item:TestMatrix} = scaling({x}, {y}, {z})")
def step_then_matrix_is_scaling_matrix(context, item, x, y, z):
    assert(item in context.dict.keys())
    t = context.dict[str(item)]
    height, width = t.shape
    assert(height==width)
    result = base.scaling(float(x), float(y), float(z))
    assert(base.equal(t, result))


@then("{item:TestMatrix} = translation({x}, {y}, {z})")
def step_then_matrix_is_translation_matrix(context, item, x, y, z):
    assert (item in context.dict.keys())
    t = context.dict[str(item)]
    height, width = t.shape
    assert (height == width)
    result = base.translation(float(x), float(y), float(z))
    assert (base.equal(t, result))

    
@then("{item:TestMatrix} is the following {height:g}x{width:g} matrix: {matrix}")
def step_impl_matrix(context, item, height, width, matrix):
    assert(item in context.dict.keys())
    t_matrix = context.dict[str(item)]
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (height, width))
    assert(base.equal(t_matrix, new_matrix))
    
