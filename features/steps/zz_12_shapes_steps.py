from behave import *
from hamcrest import assert_that, equal_to
from parse_type import TypeBuilder
from step_helper import *

valid_test_shapes = ["s"]
parse_test_shape = TypeBuilder.make_choice(valid_test_shapes)
register_type(TestShape=parse_test_shape)


valid_shape_elements = ["material", "transform"]
parse_shape_element = TypeBuilder.make_choice(valid_shape_elements)
register_type(ShapeElement=parse_shape_element)


valid_test_objects = ["m"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_group_objects = ["g1", "g2"]
parse_group_object = TypeBuilder.make_choice(valid_group_objects)
register_type(GroupObject=parse_group_object)

valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)

valid_test_variables = ["p", "n"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)

valid_ray_elements = ["origin", "direction"]
parse_ray_element = TypeBuilder.make_choice(valid_ray_elements)
register_type(RayElement=parse_ray_element)



@given("{item:TestShape} ← test_shape()")
def step_impl_test_shape_sphere(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = test_shape()


@then("{item:TestShape}.{element:ShapeElement} = translation({x:g}, {y:g}, {z:g})")
def step_impl_shape_element_translation(context, item, element, x, y, z):
    assert(item in context.dict.keys())
    assert(element in valid_shape_elements)
    shape_element = context.dict[str(item)].__dict__[str(element)]
    transform_value = translation(float(x), float(y), float(z))
    assert(equal(shape_element, transform_value))


@then("{item:TestShape}.saved_ray.origin = point({x:g}, {y:g}, {z:g})")
def step_impl_ray_intersect_list_count(context, item, x, y, z):
    assert(item in context.dict.keys())
    local_value = context.dict[str(item)].saved_ray.origin
    test_value = point(float(x), float(y), float(z))
    assert(equal(local_value, test_value))

@then("{item:TestShape}.saved_ray.direction = vector({x:g}, {y:g}, {z:g})")
def step_impl_ray_intersect_list_count(context, item, x, y, z):
    assert(item in context.dict.keys())
    local_value = context.dict[str(item)].saved_ray.direction
    test_value = vector(float(x), float(y), float(z))
    assert(equal(local_value, test_value))





@then("{item:TestRay}.{element:RayElement} = {value:RayElement}")
def step_impl_ray_element(context, item, element, value):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = context.tuple[str(value)]
    assert(equal(thing, vec4_value))



@then("position({item:TestRay}, {t}) = point({x}, {y}, {z})")
def step_impl_eval_ray_position(context, item, t, x, y, z):
    assert (item in context.dict.keys())
    ray = context.dict[str(item)]
    ray_position = ray.position(float(eval(t)))
    test_point = point(float(x), float(y), float(z))
    assert (equal(ray_position, test_point))


@then("{listname:ListName}.count = {value:g}")
def step_impl_ray_intersect_list_count(context, listname, value):
    assert(listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    count_value = int(value)
    assert(equal(listlen, count_value))


@then("{listname:ListName}[{element:g}].t = {value:g}")
def step_impl_ray_intersect_element_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    t_value = (context.dict[str(listname)])[element].t
    assert (equal(t_value, float(value)))


@then("{listname:ListName}[{element:g}].object = {value}")
def step_impl_ray_intersect_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    thing = (context.dict[str(listname)])[element].object
    value_object = context.dict[str(value)]
    assert (equal(thing.instance_id, value_object.instance_id))


@then("{listname:ListName}[{element:g}] = {value:g}")
def step_impl_ray_intersect_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    t_value = (context.dict[str(listname)])[element].t
    assert (equal(t_value, float(value)))



@then("{item:TestSolid}.transform = identity_matrix")
def step_test_sphere_transform_is_identity(context, item):
    assert(item in context.dict.keys())
    s = context.dict[item]
    assert(equal(s.transform, np.identity(4, dtype=float)))


@then("{item:TestSolid}.transform = {value:TestMatrix}")
def step_test_sphere_transform_is_identity(context, item, value):
    assert (item in context.dict.keys())
    assert (value in context.dict.keys())
    s = context.dict[item]
    transform_matrix = context.dict[value]
    assert (equal(s.transform, transform_matrix))


@then("{item:TestVariable} = vector(√{xnum}/{xdenom}, √{ynum}/{ydenom}, √{znum}/{zdenom})")
def step_get_obj_normal_at_point(context, item, xnum, xdenom, ynum, ydenom, znum, zdenom):
    assert(item in context.tuple.keys())
    value = context.tuple[str(item)]
    new_vector = vector(np.sqrt(float(xnum)) / float(xdenom), np.sqrt(float(ynum)) / float(ydenom), np.sqrt(float(znum)) / float(zdenom))
    assert(equal(value, new_vector))
   
   


@then("{item:TestVariable} = vector({x:g}, {y:g}, -{z:g})")
def step_test_normal_value2(context, item, x, y, z):
    new_vector = vector(np.float32(x), np.float32(y), -np.float32(z))
    assert(item in context.tuple.keys())
    nval = context.tuple[str(item)]
    assert(equal(nval, new_vector))

@then("{item:TestVariable} = vector({x:g}, -{y:g}, {z:g})")
def step_test_normal_value2b(context, item, x, y, z):
    new_vector = vector(np.float32(x), -np.float32(y), np.float32(z))
    assert(item in context.tuple.keys())
    nval = context.tuple[str(item)]
    assert(equal(nval, new_vector))


@then("{item:TestVariable} = normalize({item2:TestVariable})")
def step_test_normal_value3(context, item, item2):
    assert(item in context.tuple.keys())
    nval = context.tuple[str(item)]
    assert(item2 in context.tuple.keys())
    nval2 = context.tuple[str(item2)]
    assert(equal(nval, normalize(nval2)))



@then("{item:TestObject} = material()")
def step_test_generic_material_then(context, item):
    assert(item in context.dict.keys())
    material1 = context.dict[item]
    material2 = material()
    assert(material1 == material2)
    


@then("{item:TestSolid}.material = {item2}")
def step_then_object_material_value(context, item, item2):
    assert (item in context.dict.keys())
    assert (item2 in context.dict.keys())
    assert(context.dict[str(item)].material==context.dict[str(item2)])


@then("{item:TestSolid}.material.{mchar:MaterialElement} = {value:g}")
def step_then_solid_material_characteristic_is_value(context, item, mchar, value):
    result = context.dict[str(item)].material.__dict__[str(mchar)]
    test_value = float(value)
    assert(equal(result, test_value))
    