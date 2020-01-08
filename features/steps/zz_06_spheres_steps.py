from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np

valid_test_solids = ["s", "s2", "shape"]
parse_test_solid = TypeBuilder.make_choice(valid_test_solids)
register_type(TestSolid=parse_test_solid)

valid_test_objects = ["m"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_matrices = ["t", "m"]
parse_test_matrix = TypeBuilder.make_choice(valid_test_matrices)
register_type(TestMatrix=parse_test_matrix)

valid_vec4_extensions = ["x", "y", "z", "w"]
parse_vec4_extension = TypeBuilder.make_choice(valid_vec4_extensions)
register_type(Vec4Ext=parse_vec4_extension)

valid_test_variables = ["origin", "direction", "n"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_test_rays = ["r", "r2"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)

valid_ray_elements = ["origin", "direction", "transform"]
parse_ray_element = TypeBuilder.make_choice(valid_ray_elements)
register_type(RayElement=parse_ray_element)

valid_material_elements = ["color", "ambient", "diffuse", "specular", "shininess", "reflective", "transparency", "refractive_index"]
parse_material_element = TypeBuilder.make_choice(valid_material_elements)
register_type(MaterialElement=parse_material_element)

valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)

valid_material_elements = ["color", "ambient", "diffuse", "specular", "shininess", "reflective", "transparency", "refractive_index"]
parse_material_element = TypeBuilder.make_choice(valid_material_elements)
register_type(MaterialElement=parse_material_element)



@given("{item:TestSolid} ← glass_sphere()")
def step_impl_generic_glass_sphere(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.glass_sphere()



@given("{item:TestMatrix} ← translation({x:g}, {y:g}, {z:g})")
def step_impl_generic_translation_matrix(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.translation(float(x), float(y), float(z))


@given("{item:TestRay} ← ray(point({px}, {py}, {pz}), vector({vx}, {vy}, {vz}))")
def step_impl_generic_ray_full(context, item, px, py, pz, vx, vy, vz):
    print("in ray definition")
    pt = base.point(float(px), float(py), float(pz))
    vc = base.vector(float(vx), float(vy), float(vz))
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.ray(pt, vc)
    print("ray is ", context.dict[str(item)].__dict__)


@given("{item:TestSolid} ← sphere()")
def step_impl_generic_solid_sphere(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.sphere()


@given("{item:TestMatrix} ← scaling({x1}, {y1}, {z1}) * rotation_z({numerator}/{denominator})")
def step_given_transform_cascade(context, item, x1, y1, z1, numerator, denominator):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
        
    if numerator == "π":
        numerator = np.pi
    else:
        numerator = float(numerator)
        
    m = np.matmul(base.scaling(float(x1), float(y1), float(z1)), base.rotation_z(numerator / float(denominator)))
    context.dict[str(item)] = m



@given("set_transform({item:TestSolid}, {item2:TestMatrix})")
def step_set_obj_new_scaling_transform_B(context, item, item2):
    assert (item in context.dict.keys())
    assert (item2 in context.dict.keys())
    transform_matrix = context.dict[str(item2)]
    s = context.dict[item]
    base.set_transform(s, transform_matrix)




@given("{item:TestObject}.{element:MaterialElement} ← {value}")
def step_given_object_material_value(context, item, element, value):
    assert(item in context.dict.keys())
    context.dict[str(item)].__dict__[str(element)] = float(value)
    


@given("set_transform({item:TestSolid}, translation({x}, {y}, {z}))")
def step_set_obj_new_scaling_transform(context, item, x, y, z):
    assert (item in context.dict.keys())
    transform_matrix = base.translation(float(x), float(y), float(z))
    s = context.dict[item]
    base.set_transform(s, transform_matrix)




@when("{item:TestRay} ← ray({origin}, {direction})")
def step_impl_generic_ray_implied(context, item, origin, direction):
    assert(origin in context.tuple.keys())
    assert(direction in context.tuple.keys())
    origin_pt = context.tuple[str(origin)]
    dir_vector = context.tuple[str(direction)]
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.ray(origin_pt, dir_vector)
    print(context.dict[str(item)])


@when("{ray2:TestRay} ← transform({ray1:TestRay}, {m:TestMatrix})")
def step_impl_generic_ray_implied(context, ray2, ray1, m):
    assert(m in context.dict.keys())
    assert(ray1 in context.dict.keys())
    original_ray = context.dict[str(ray1)]
    transform_matrix = context.dict[str(m)]
    context.dict[str(ray2)] = base.transform(original_ray, transform_matrix)


@when("{listname:ListName} ← intersect({test_sphere:TestSolid}, {src_ray:TestRay})")
def step_impl_ray_element_point(context, listname, test_sphere, src_ray):
    assert(test_sphere in context.dict.keys())
    assert(src_ray in valid_test_rays)
    assert(src_ray in context.dict.keys())
    ray = context.dict[str(src_ray)]
    sphere = context.dict[str(test_sphere)]
    intersection_list = base.intersect(sphere, ray)
    context.dict[str(listname)] = intersection_list


@when("set_transform({item:TestSolid}, scaling({x}, {y}, {z}))")
def step_set_obj_new_scaling_transform(context, item, x, y, z):
    assert (item in context.dict.keys())
    transform_matrix = base.scaling(float(x), float(y), float(z))
    s = context.dict[item]
    base.set_transform(s, transform_matrix)




@when("{item:TestObject} ← {item2:TestSolid}.material")
def step_impl_generic_material_when(context, item, item2):
    assert(item2 in context.dict.keys())
    material = context.dict[item2].material
    context.dict[item] = material




@when("set_transform({item:TestSolid}, translation({x}, {y}, {z}))")
def step_set_obj_new_scaling_transform2(context, item, x, y, z):
    assert (item in context.dict.keys())
    transform_matrix = base.translation(float(x), float(y), float(z))
    s = context.dict[item]
    base.set_transform(s, transform_matrix)


@when("set_transform({item:TestSolid}, {new_transform:TestMatrix})")
def step_set_obj_new_transform(context, item, new_transform):
    assert (item in context.dict.keys())
    assert (new_transform in context.dict.keys())
    transform_matrix = context.dict[str(new_transform)]
    s = context.dict[item]
    base.set_transform(s, transform_matrix)




@when("{item:TestVariable} ← normal_at({s:TestSolid}, point(√{xnum}/{xdenom}, √{ynum}/{ydenom}, √{znum}/{zdenom}))")
def step_get_obj_normal_at_point(context, item, s, xnum, xdenom, ynum, ydenom, znum, zdenom):
    assert (s in context.dict.keys())
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    new_point = base.point(np.sqrt(float(xnum)) / float(xdenom), np.sqrt(float(ynum)) / float(ydenom), np.sqrt(float(znum)) / float(zdenom))
    test_solid = context.dict[str(s)]
    norm = base.normal_at(test_solid, new_point)
    context.tuple[str(item)] = norm


@when("{item:TestVariable} ← normal_at({s:TestSolid}, point({x}, √{ynum}/{ydenom}, -√{znum}/{zdenom}))")
def step_get_obj_normal_at_point(context, item, s, x, ynum, ydenom, znum, zdenom):
    assert (s in context.dict.keys())
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    
    new_point = base.point(np.sqrt(float(x)), np.sqrt(float(ynum)) / float(ydenom),
                               -np.sqrt(float(znum)) / float(zdenom))
    test_solid = context.dict[str(s)]
    norm = base.normal_at(test_solid, new_point)
    context.tuple[str(item)] = norm



@when("{item:TestVariable} ← normal_at({s:TestSolid}, point({x}, {y}, {z}))")
def step_get_obj_normal_at_point(context, item, s, x, y, z):
    assert (s in context.dict.keys())
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    
    new_point = base.point(float(x), float(y), float(z))
    test_solid = context.dict[str(s)]
    norm = base.normal_at(test_solid, new_point)
    context.tuple[str(item)] = norm


@when("{item:TestSolid}.material ← {item2}")
def step_when_object_material_value(context, item, item2):
    assert (item in context.dict.keys())
    assert (item2 in context.dict.keys())
    context.dict[str(item)].material = context.dict[str(item2)]


@then("{item:TestObject}.{element:MaterialElement} = color({red:g}, {green:g}, {blue:g})")
def step_impl_ray_intersect_list_count(context, item, element, red, green, blue):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    local_object = eval(local_object_str)
    value = base.color(float(red), float(green), float(blue))
    assert(base.equal(local_object, value))




@then("{item:TestRay}.{element:RayElement} = vector({x}, {y}, {z})")
def step_impl_ray_element_vector(context, item, element, x, y, z):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = base.vector(float(x), float(y), float(z))
    assert(base.equal(thing, vec4_value))



@then("{item:TestRay}.{element:RayElement} = {value:RayElement}")
def step_impl_ray_element(context, item, element, value):
    assert(item in context.dict.keys())
    assert(element in valid_ray_elements)
    ray = context.dict[str(item)]
    thing = eval("ray."+str(element))
    vec4_value = context.tuple[str(value)]
    assert(base.equal(thing, vec4_value))



@then("position({item:TestRay}, {t}) = point({x}, {y}, {z})")
def step_impl_eval_ray_position(context, item, t, x, y, z):
    assert (item in context.dict.keys())
    ray = context.dict[str(item)]
    ray_position = ray.position(float(eval(t)))
    test_point = base.point(float(x), float(y), float(z))
    assert (base.equal(ray_position, test_point))


@then("{listname:ListName}.count = {value:g}")
def step_impl_ray_intersect_list_count(context, listname, value):
    assert(listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    count_value = float(value)
    assert(base.equal(listlen, count_value))


@then("{listname:ListName}[{element:g}].t = {value:g}")
def step_impl_ray_intersect_element_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    t_value = (context.dict[str(listname)])[element].t
    assert (base.equal(t_value, float(value)))


@then("{listname:ListName}[{element:g}].object = {value}")
def step_impl_ray_intersect_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    thing = (context.dict[str(listname)])[element].object
    value_object = context.dict[str(value)]
    assert (base.equal(thing.instance_id, value_object.instance_id))


@then("{listname:ListName}[{element:g}] = {value:g}")
def step_impl_ray_intersect_list_count(context, listname, element, value):
    assert (listname in context.dict.keys())
    listlen = len(context.dict[str(listname)])
    element = int(element)
    assert(element >= 0)
    assert(element < listlen)
    t_value = (context.dict[str(listname)])[element].t
    assert (base.equal(t_value, float(value)))



@then("{item:TestSolid}.transform = identity_matrix")
def step_test_sphere_transform_is_identity(context, item):
    assert(item in context.dict.keys())
    s = context.dict[item]
    assert(base.equal(s.transform, np.identity(4, dtype=float)))


@then("{item:TestSolid}.transform = {value:TestMatrix}")
def step_test_sphere_transform_is_identity(context, item, value):
    assert (item in context.dict.keys())
    assert (value in context.dict.keys())
    s = context.dict[item]
    transform_matrix = context.dict[value]
    assert (base.equal(s.transform, transform_matrix))


@then("{item:TestVariable} = vector(√{xnum}/{xdenom}, √{ynum}/{ydenom}, √{znum}/{zdenom})")
def step_get_obj_normal_at_point(context, item, xnum, xdenom, ynum, ydenom, znum, zdenom):
    assert(item in context.tuple.keys())
    value = context.tuple[str(item)]
    new_vector = base.vector(np.sqrt(float(xnum)) / float(xdenom), np.sqrt(float(ynum)) / float(ydenom), np.sqrt(float(znum)) / float(zdenom))
    print("new vector is ", new_vector)
    assert(base.equal(value, new_vector))
   
   


@then("{item:TestVariable} = vector({x}, {y}, {z})")
def step_test_normal_value2(context, item, x, y, z):
    new_vector = base.vector(float(x), float(y), float(z))
    assert(item in context.tuple.keys())
    nval = context.tuple[str(item)]
    assert(base.equal(nval, new_vector))


@then("{item:TestVariable} = normalize({item2:TestVariable})")
def step_test_normal_value3(context, item, item2):
    assert(item in context.tuple.keys())
    nval = context.tuple[str(item)]
    assert(item2 in context.tuple.keys())
    nval2 = context.tuple[str(item2)]
    assert(base.equal(nval, base.normalize(nval2)))



@then("{item:TestObject} = material()")
def step_test_generic_material_then(context, item):
    assert(item in context.dict.keys())
    material1 = context.dict[item]
    material2 = base.material()
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
    assert(base.equal(result, test_value))
    