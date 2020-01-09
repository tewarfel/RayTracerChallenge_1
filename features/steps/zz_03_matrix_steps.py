from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np
from step_helper import *

valid_test_matrices = ["M", "A", "B", "C", "inv", "half_quarter"]
parse_test_matrix = TypeBuilder.make_choice(valid_test_matrices)
register_type(TestMatrix=parse_test_matrix)

valid_test_variables = ["b", "a"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)


#@given("the following 4x4 matrix {item:TestVariable}: {matrix}")
@given("the following {height:g}x{width:g} matrix {item:TestMatrix}: {matrix}")
def step_impl_matrix(context, height, width, item, matrix):
    ensure_context_has_dict(context)
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (height, width))
    context.dict[item] = new_matrix


@given("{item:TestMatrix} ← transpose(identity_matrix)")
def step_identity_transpose_matrix(context, item):
    ensure_context_has_dict(context)
    dim = 4
    new_matrix = np.identity(dim, dtype=float)
    assert (new_matrix.shape == (dim, dim))
    context.dict[item] = np.transpose(new_matrix)


@given("{item1:TestMatrix} ← inverse({item2:TestMatrix})")
def step_assign_inverse_matrix(context, item1, item2):
    assert(item2 in context.dict.keys())
    matrix = context.dict[str(item2)]
    assert(base.is_invertible(matrix))
    context.dict[item1] = base.inverse(matrix)


@given("{item1:TestMatrix} ← submatrix({item2:TestMatrix}, {row:g}, {col:g})")
def step_assign_submatrix(context, item1, item2, row, col):
    assert(item2 in context.dict.keys())
    matrix2 = context.dict[str(item2)]
    matrix2_height, matrix2_width = matrix2.shape
    new_matrix = base.submatrix(matrix2, row, col)
    assert (new_matrix.shape == ((matrix2_height -1), (matrix2_width-1)))
    context.dict[item1] = new_matrix


@given("the following matrix {item:TestMatrix}: {matrix}")
def step_impl_matrix(context, item, matrix):
    ensure_context_has_dict(context)
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    context.dict[item] = new_matrix


@given("{item1:TestMatrix} ← {item2:TestMatrix} * {item3:TestMatrix}")
def step_given_matrix_equal_matrix_mul_matrix(context, item1, item2, item3):
    assert (item2 in context.dict.keys())
    assert (item3 in context.dict.keys())
    matrix2 = context.dict[str(item2)]
    matrix3 = context.dict[str(item3)]
    context.dict[str(item1)] = np.matmul(matrix2, matrix3)


@then("submatrix({item1:TestMatrix}, {row:g}, {col:g}) is the following {height:g}x{width:g} matrix:{matrix}")
def step_assign_submatrix_result(context, item1, row, col, height, width, matrix):
    assert(item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix1_height, matrix1_width = matrix1.shape
    new_matrix = base.submatrix(matrix1, row, col)
    assert (new_matrix.shape == ((matrix1_height -1), (matrix1_width-1)))
    result_matrix_string = "np.array(" + matrix + ", dtype=float)"
    result_matrix = eval(result_matrix_string)
    assert (result_matrix.shape == (height, width))
    assert((height == matrix1_height-1) and (width == matrix1_width -1))
    assert(np.array_equal(new_matrix, result_matrix))
    

@then("{item1:TestMatrix} = identity_matrix")
def step_then_matrix_equals_identity(context, item1):
    assert(item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    assert(height == width)
    matrix2 = np.identity(height, dtype=float)
    assert(np.array_equal(matrix1, matrix2))


@then("{item:TestMatrix}[{y:g},{x:g}] = {numerator:g}/{denominator:g}")
def step_then_matrix_element_equals_rational_value(context, item, y, x, numerator, denominator):
    assert(item in context.dict.keys())
    this_matrix = context.dict[str(item)]
    assert(base.equal(this_matrix[int(y), int(x)], float(numerator) / float(denominator)))


@then("{item:TestMatrix}[{y:g},{x:g}] = {value:g}")
def step_then_matrix_element_equals_value(context, item, y, x, value):
    assert(item in context.dict.keys())
    this_matrix = context.dict[str(item)]
    assert(base.equal(this_matrix[int(y), int(x)], float(value)))


@then("{item1:TestMatrix} = {item2:TestMatrix}")
def step_then_matrix_equals_matrix(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix2 = context.dict[str(item2)]
    assert(np.array_equal(matrix1, matrix2))
    
    
@then("{item1:TestMatrix} != {item2:TestMatrix}")
def step_then_matrix_equals_matrix(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix2 = context.dict[str(item2)]
    assert(not np.array_equal(matrix1, matrix2))
    
    
@then("{item1:TestMatrix} * {item2:TestMatrix} is the following {height:g}x{width:g} matrix: {matrix}")
def step_then_matrix_mul_matrix_equals_matrix(context, item1, item2, height, width, matrix):
    assert (item1 in context.dict.keys())
    assert (item2 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix2 = context.dict[str(item2)]
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (height, width))
    assert (np.array_equal(np.matmul(matrix1, matrix2), new_matrix))


@then("{item1:TestMatrix} * {item2:TestVariable} = tuple({x:g}, {y:g}, {z:g}, {w:g})")
def step_then_matrix_mul_tuple_equals_tuple(context, item1, item2, x,y,z,w):
    assert (item1 in context.dict.keys())
    assert (item2 in context.tuple.keys())
    matrix1 = context.dict[str(item1)]
    tuple2 = context.tuple[str(item2)]
    tuple_as_matrix = np.array([tuple2.x, tuple2.y, tuple2.z, tuple2.w], dtype=float)
    assert (np.array_equal(np.matmul(matrix1, tuple_as_matrix), np.array([x,y,z,w], dtype=float)))
    assert(np.array_equal((matrix1 @ tuple2), base.Vec4(float(x), float(y), float(z), float(w))))
    
    
@then("{item1:TestMatrix} * identity_matrix = {item2:TestMatrix}")
def step_then_matrix_mul_matrix_equals_matrix(context, item1, item2):
    assert (item1 in context.dict.keys())
    assert (item2 in context.dict.keys())
    assert(base.equal(context.dict[item1], context.dict[item2]))
    matrix1 = context.dict[str(item1)]
    assert(matrix1.shape[0] == matrix1.shape[1])
    result = np.matmul(matrix1, np.identity(matrix1.shape[0]))
    assert(np.array_equal(matrix1, result))


@then("identity_matrix * {item1:TestVariable} = {item2:TestVariable}")
def step_then_matrix_mul_matrix_equals_matrix(context, item1, item2):
    assert (item1 in context.tuple.keys())
    assert (item2 in context.tuple.keys())
    assert(base.equal(context.tuple[item1], context.tuple[item2]))
    matrix1 = context.tuple[str(item1)]
    result = np.matmul(matrix1, np.identity(4))
    assert(np.array_equal(matrix1, result))
    
    
@then("transpose({item1:TestMatrix}) is the following matrix: {matrix}")
def step_then_matrix_transpose_equals_matrix(context, item1, matrix):
    assert (item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix1_height, matrix1_width = matrix1.shape
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (matrix1_width, matrix1_height))
    result = np.transpose(matrix1)
    assert(np.array_equal(new_matrix, result))


@then("determinant({item1:TestMatrix}) = {value:g}")
def step_then_determinant_matrix_equals_value(context, item1, value):
    assert (item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    height, width = matrix1.shape
    float_value = float(value)
    det = base.determinant(matrix1)
    assert (base.equal(det, float_value))


@then("minor({item:TestMatrix}, {row:g}, {col:g}) = {value:g}")
def step_then_minor_matrix_equals_value(context, item, row, col, value):
    assert(item in context.dict.keys())
    this_matrix = context.dict[str(item)]
    matrix_minor = base.minor(this_matrix, row, col)
    assert(base.equal(matrix_minor, float(value)))


@then("cofactor({item:TestMatrix}, {row:g}, {col:g}) = {value:g}")
def step_then_cofactor_matrix_equals_value(context, item, row, col, value):
    assert(item in context.dict.keys())
    this_matrix = context.dict[str(item)]
    matrix_cofactor = base.cofactor(this_matrix, row, col)
    assert(base.equal(matrix_cofactor, float(value)))


@then("{item:TestMatrix} is invertible")
def step_then_matrix_is_invertible(context, item):
    assert(item in context.dict.keys())
    assert(base.is_invertible(context.dict[str(item)]))


@then("{item:TestMatrix} is not invertible")
def step_then_matrix_is_not_invertible(context, item):
    assert(item in context.dict.keys())
    assert_that(base.is_invertible(context.dict[str(item)]), equal_to(False))
    
    
@then("{item1:TestMatrix} is the following {height:g}x{width:g} matrix: {matrix}")
def step_then_matrix_result_equals_matrix(context, item1, height, width, matrix):
    assert (item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (height, width))
    assert(base.equal(matrix1, new_matrix))


@then("inverse({item1:TestMatrix}) is the following {height:g}x{width:g} matrix: {matrix}")
def step_then_inverse_matrix_result_equals_matrix(context, item1, height, width, matrix):
    assert (item1 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    inverse_matrix1 = base.inverse(matrix1)
    new_matrix_string = "np.array(" + matrix + ", dtype=float)"
    new_matrix = eval(new_matrix_string)
    assert (new_matrix.shape == (height, width))
    assert (base.equal(inverse_matrix1, new_matrix))


@then("{item1:TestMatrix} * inverse({item2:TestMatrix}) = {item3:TestMatrix}")
def step_then_matrix_result_equals_inv_matrix_mul_matrix(context, item1, item2, item3):
    assert (item1 in context.dict.keys())
    assert (item2 in context.dict.keys())
    assert (item3 in context.dict.keys())
    matrix1 = context.dict[str(item1)]
    matrix2 = context.dict[str(item2)]
    inv_matrix2 = base.inverse(matrix2)
    matrix3 = context.dict[str(item3)]
    result = np.matmul(matrix1, inv_matrix2)
    assert(base.equal(result, matrix3))

