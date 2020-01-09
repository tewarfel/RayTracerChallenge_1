from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np
from step_helper import *

valid_test_objects = ["hsize", "vsize","field_of_view", "c", "w"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["up", "from", "to"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_camera_elements = ["hsize", "vsize", "field_of_view", "transform", "pixel_size"]
parse_camera_element = TypeBuilder.make_choice(valid_camera_elements)
register_type(CameraElement=parse_camera_element)

valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)


@given("{item:TestObject} ← {value_num}/{value_denom:g}")
def step_given_object_value(context, item, value_num, value_denom):
    ensure_context_has_dict(context)
    value_num = np.pi if value_num == "π" else float(value_num)
    value_denom = float(value_denom)
    context.dict[str(item)] = (value_num / value_denom)

@given("{item:TestVariable} ← point({x:g}, {y:g}, {z})")
def step_given_object_point_value(context, item, x, y, z):
    ensure_context_has_tuple(context)
    print("assigned ", item, context.tuple[str(item)])
    context.tuple[str(item)] = base.point(float(x), float(y), float(z))



@given("{item:TestObject} ← {value:g}")
def step_given_object_value(context, item, value):
    ensure_context_has_dict(context)
    context.dict[str(item)] = float(value)


@given("{item:TestObject} ← camera({hsize:g}, {vsize:g}, {fov_numerator}/{fov_denominator:g})")
def step_given_create_camera(context, item, hsize, vsize, fov_numerator, fov_denominator):
    fov_numerator = np.pi if fov_numerator=="π" else float(fov_numerator)
    ensure_context_has_dict(context)
    context.dict[item] = base.camera(float(hsize), float(vsize), (fov_numerator/float(fov_denominator)))


@given("{item:TestObject}.transform ← view_transform({ofrom:TestVariable}, {to:TestVariable}, {up:TestVariable})")
def step_given_camera_transform_value(context, item, ofrom, to, up):
    assert(ofrom in context.tuple.keys())
    assert(to in context.tuple.keys())
    assert(up in context.tuple.keys())
    context.dict[str(item)].set_transform(base.view_transform(context.tuple[str(ofrom)],
                                                              context.tuple[str(to)],
                                                              context.tuple[str(up)]))
    


    

@when("{item:TestObject} ← camera({hsize:TestObject}, {vsize:TestObject}, {fov:TestObject})")
def step_when_create_camera(context, item, hsize, vsize, fov):
    context.dict[item] = base.camera(context.dict[str(hsize)],
                                         context.dict[str(vsize)],
                                         context.dict[str(fov)])
    

@when("{item:TestRay} ← ray_for_pixel({camera:TestObject}, {x:g}, {y:g})")
def step_when_create_ray_for_pixel(context, item, camera, x, y):
    ensure_context_has_dict(context)
    context.dict[item] = base.ray_for_pixel(context.dict[str(camera)], float(x), float(y))


@when("{item:TestObject}.{element:CameraElement} ← rotation_y({rot_num}/{rot_denom:g}) * translation({x}, {y}, {z})")
def step_camera_element_has_transform_value(context, item, element, rot_num, rot_denom, x, y, z):
    assert(item in context.dict.keys())
    rot_num = np.pi if rot_num=="π" else float(rot_num)
    rot_denom = float(rot_denom)
    context.dict[str(item)].set_transform(np.matmul(base.rotation_y(rot_num/rot_denom), base.translation(float(x), float(y), float(z))))



@when("image ← render({camera:TestObject}, {world:TestObject})")
def step_when_render_world(context, camera, world):
    ensure_context_has_dict(context)
    context.dict["image"] = base.render(context.dict[str(camera)], context.dict[str(world)])




@then("{item:TestObject}.{element:CameraElement} = {numerator}/{denominator:g}")
def step_camera_element_has_rational_value(context, item, element, numerator, denominator):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    camera_object_element = eval(local_object_str)
    numerator = np.pi if numerator=="π" else float(numerator)
    test_value = numerator/float(denominator)
    assert(base.equal(camera_object_element, test_value))
    
    
@then("{item:TestObject}.{element:CameraElement} = {value:g}")
def step_camera_element_has_value(context, item, element, value):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    camera_object_element = eval(local_object_str)
    test_value = float(value)
    assert(base.equal(camera_object_element, test_value))

@then("{item:TestObject}.{element:CameraElement} = identity_matrix")
def step_camera_element_has_value_identity(context, item, element):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    camera_object_element = eval(local_object_str)
    test_value = np.identity(4, dtype=float)
    assert(base.equal(camera_object_element, test_value))


@then("{item:TestRay}.{element:RayElement} = point({x}, {y}, {z})")
def step_ray_element_has_value(context, item, element, x, y, z):
    assert(item in context.dict.keys())
    comps_object_element = context.dict[str(item)].__dict__[str(element)]
    test_value = base.point(float(x), float(y), float(z))
    assert(base.equal(comps_object_element, test_value))


@then("pixel_at(image, {x:g}, {y:g}) = color({red:g}, {green:g}, {blue:g})")
def step_ray_element_has_value(context, x, y, red, green, blue):
    assert("image" in context.dict.keys())
    test_value = base.pixel_at(context.dict["image"], int(x), int(y))
    test_color = base.color(float(red), float(green), float(blue))
    assert(base.equal(test_value, test_color))





