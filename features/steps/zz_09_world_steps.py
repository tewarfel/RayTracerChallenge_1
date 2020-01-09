from behave import *
from hamcrest import assert_that, equal_to
from vec3 import Vec3, vec3
from vec4 import Vec4, point, vector
import numpy as np
from shape import material, sphere, test_shape, default_world, point_light
from base import equal, intersect_world, shade_hit, is_shadowed, color_at, World, render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x
from parse_type import TypeBuilder
from step_helper import *


valid_test_objects = ["w", "s1", "s2", "light", "shape", "i", "comps", "outer", "inner", "lower", "upper", "s1"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["intensity", "position", "eyev", "normalv", "result", "c", "p", "color"]
parse_test_variable = TypeBuilder.make_choice(valid_test_variables)
register_type(TestVariable=parse_test_variable)

valid_light_elements = ["position", "intensity"]
parse_light_element = TypeBuilder.make_choice(valid_light_elements)
register_type(LightElement=parse_light_element)

valid_material_elements = ["color", "ambient", "diffuse", "specular", "shininess", "reflective", "transparency", "refractive_index"]
parse_material_element = TypeBuilder.make_choice(valid_material_elements)
register_type(MaterialElement=parse_material_element)

valid_world_elements = ["light", "objects"]
parse_world_element = TypeBuilder.make_choice(valid_world_elements)
register_type(WorldElement = parse_world_element)


valid_intersect_list_names = ["xs"]
parse_intersect_list_name = TypeBuilder.make_choice(valid_intersect_list_names)
register_type(ListName=parse_intersect_list_name)


valid_test_rays = ["r"]
parse_test_ray = TypeBuilder.make_choice(valid_test_rays)
register_type(TestRay=parse_test_ray)


@given("{item:TestObject} ← world()")
def step_world_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = world()

@given("{item1:TestObject} is added to {item2:TestObject}")
def step_world_create(context, item1, item2):
    assert(item1 in context.dict.keys())
    context.dict[str(item2)].objects.append(context.dict[str(item1)])




@then("{item:TestObject} contains no objects")
def step_world_empty(context, item):
    assert(item in context.dict.keys())
    thing = context.dict[str(item)]
    assert(len(thing.objects) == 0)


@then("{item:TestObject} has no light source")
def step_world_empty_2(context, item):
    assert(item in context.dict.keys())
    thing = context.dict[str(item)]
    assert(len(thing.light) == 0)


@given("{item:TestObject}.material.ambient ← 1")
def step_world_item_material_ambient_one(context, item):
    assert(item in context.dict.keys())
    context.dict[str(item)].material.ambient = 1.0
    


@given("{item:TestObject} ← point_light(point({px:g}, {py:g}, {pz:g}), color({red:g}, {green:g}, {blue:g}))")
def step_impl_point_light_for_materials(context, item, px, py, pz, red, green, blue):
    ensure_context_has_dict(context)

    real_position = point(np.float32(px), np.float32(py), np.float32(pz))
    real_intensity = color(np.float32(red), np.float32(green), np.float32(blue))
    context.dict[item] = point_light(real_position, real_intensity)


@given("{item:TestObject}.light ← point_light(point({px:g}, {py:g}, {pz:g}), color({red:g}, {green:g}, {blue:g}))")
def step_impl_point_light_for_world(context, item, px, py, pz, red, green, blue):
    ensure_context_has_dict(context)

    real_position = point(np.float32(px), np.float32(py), np.float32(pz))
    real_intensity = color(np.float32(red), np.float32(green), np.float32(blue))
    context.dict[item].light = [point_light(real_position, real_intensity)]


@given("{item:TestObject} ← sphere()")
def step_given_s_is_sphere(context, item):
    ensure_context_has_dict(context)
    context.dict[str(item)] = sphere()


@given("{item:TestObject} is added to {world:TestObject}")
def step_given_item_added_to_world(context, item, world):
    assert(item in context.dict.keys())
    assert(world in context.dict.keys())
    context.dict[str(world)].objects.append(context.dict[str(item)])
    

@given("{item:TestObject} ← sphere() with translation({x}, {y}, {z})")
def step_given_s_is_sphere_with_translation(context, item, x, y, z):
    ensure_context_has_dict(context)
    context.dict[str(item)] = sphere(sphere_transform=translation(np.float32(x), np.float32(y), np.float32(z)))


@given("{item:TestObject} ← sphere(sphere_material=material(material_color=({red}, {green}, {blue}), diffuse={d}, specular={sp}))")
def step_impl_sphere_with_material(context, item, red, green, blue, d, sp):
    the_material_color = color(np.float32(red), np.float32(green), np.float32(blue))
    new_material = material(material_color=the_material_color, diffuse=float(d), specular=float(sp))
    new_sphere = sphere(sphere_material=new_material)
    ensure_context_has_dict(context)
    context.dict[str(item)] = new_sphere


@given("{item:TestObject} ← sphere(sphere_transform=transform(scaling({x}, {y}, {z})))")
def step_impl_sphere_with_transform(context, item, x, y, z):
    new_transform = scaling(np.float32(x), np.float32(y), np.float32(z))
    new_sphere = sphere(sphere_transform=new_transform)
    ensure_context_has_dict(context)
    context.dict[str(item)] = new_sphere



@given("{item:TestObject} ← default_world()")
def step_default_world_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = default_world()


@given("{listitem:ListName} ← intersections(-√{t1:g}/{t1denom:g}:{s1:TestObject}, √{t2:g}/{t2denom:g}:{s2:TestObject})")
def step_create_intersection_list1(context, listitem, t1, t1denom, s1, t2, t2denom, s2):
    assert(s1 in context.dict.keys())
    assert(s2 in context.dict.keys())
    context.dict[str(listitem)] = intersections(intersection(np.float32(-math.sqrt(t1))/np.float32(t1denom), context.dict[str(s1)]),
                                                intersection(np.float32(math.sqrt(t2))/np.float32(t2denom), context.dict[str(s2)]))




@given("{listitem:ListName} ← intersections({t1:g}:{s1:TestObject}, {t2:g}:{s2:TestObject})")
def step_create_intersection_list2(context, listitem, t1, s1, t2, s2):
    assert(s1 in context.dict.keys())
    assert(s2 in context.dict.keys())
    context.dict[str(listitem)] = intersections(intersection(np.float32(t1), context.dict[str(s1)]),
                                                intersection(np.float32(t2), context.dict[str(s2)]))



@given("{item:TestRay} ← ray(point({px}, {py}, {pz}), vector({vx}, {vy}, {vz}))")
def step_impl_generic_ray_full(context, item, px, py, pz, vx, vy, vz):
    pt = point(np.float32(px), np.float32(py), np.float32(pz))
    vc = vector(np.float32(vx), np.float32(vy), np.float32(vz))
    ensure_context_has_dict(context)
    context.dict[str(item)] = ray(pt, vc)


@given("{item:TestObject} has material.transparency={trans:g}, material.refractive_index={ri:g}")
def step_impl_material_characteristics_2(context, item, trans, ri):
    context.dict[str(item)].material.transparency=np.float32(trans)
    context.dict[str(item)].material.refractive_index=np.float32(ri)


@when("{item:TestObject} ← default_world()")
def step_default_world_create(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = default_world()



@when("{item:ListName} ← intersect_world({w:TestObject}, {r:TestRay})")
def step_intersect_world_ray(context, item, w, r):
    ensure_context_has_dict(context)
    test_ray = context.dict[str(r)]
    context.dict[str(item)] = intersect_world(context.dict[str(w)], context.dict[str(r)])


@when("{item:TestVariable} ← shade_hit({w:TestObject}, {comps:TestObject})")
def step_shade_hit_world(context, item, w, comps):
    ensure_context_has_tuple(context)
    world_object = context.dict[str(w)]
    comps_object = context.dict[str(comps)]
    context.tuple[str(item)] = shade_hit(world_object, comps_object)


@when("{item:TestVariable} ← color_at({w:TestObject}, {r:TestRay})")
def step_shade_hit_world(context, item, w, r):
    ensure_context_has_tuple(context)
    world_object = context.dict[str(w)]
    ray_object = context.dict[str(r)]
    resulting_color = color_at(world_object, ray_object, 5)
    context.tuple[str(item)] = resulting_color



@when("{item:TestVariable} ← reflected_color({w:TestObject}, {o:TestObject}, 0)")
def step_reflected_color_world_with_depth_zero(context, item, w, o):
    ensure_context_has_tuple(context)
    world_object = context.dict[str(w)]
    comps_object = context.dict[str(o)]
    resulting_color = reflected_color(world_object, comps_object, 0)
    context.tuple[str(item)] = resulting_color




@when("{item:TestVariable} ← reflected_color({w:TestObject}, {o:TestObject})")
def step_reflected_color_world(context, item, w, o):
    ensure_context_has_tuple(context)
    world_object = context.dict[str(w)]
    comps_object = context.dict[str(o)]
    resulting_color = reflected_color(world_object, comps_object, 5)
    context.tuple[str(item)] = resulting_color


@when("{item:TestVariable} ← refracted_color({w:TestObject}, {o:TestObject}, {remaining:g})")
def step_refracted_color_world(context, item, w, o, remaining):
    ensure_context_has_tuple(context)
    world_object = context.dict[str(w)]
    comps_object = context.dict[str(o)]
    resulting_color = refracted_color(world_object, comps_object, int(remaining))
    context.tuple[str(item)] = resulting_color





@then("{item:TestObject}.{element:WorldElement} = {item2:TestObject}")
def step_default_world_contains_element(context, item, element, item2):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    light_list = eval(local_object_str)
    test_value = context.dict[str(item2)]

    match_found = False
    for source in light_list:
        if equal(source.position,test_value.position):
            if equal(source.intensity, test_value.intensity):
                match_found = True
                break
    assert(match_found)





@then("{item:TestObject} contains {item2:TestObject}")
def step_default_world_contains_object(context, item, item2):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"'].objects"
    object_list = eval(local_object_str)
    test_object = context.dict[str(item2)]
    match_found = False
    for thing in object_list:
        for element in thing.material.__dict__.keys():
            if thing.material.__dict__[str(element)] == test_object.material.__dict__[str(element)]:
                match_found = True
            else:
                match_found = False
                break
        if match_found and equal(thing.transform, test_object.transform):
            break
        else:
            match_found = False
    assert(match_found)



@then("is_shadowed({item1:TestObject}, {item2:TestVariable}) is false")
def step_then_is_shadowed_is_false(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.tuple.keys())
    world_object = context.dict[str(item1)]
    point_object = context.tuple[str(item2)]
    result = is_shadowed(world_object, point_object)
    assert(result == False)


@then("is_shadowed({item1:TestObject}, {item2:TestVariable}) is true")
def step_then_is_shadowed_is_false(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.tuple.keys())
    world_object = context.dict[str(item1)]
    point_object = context.tuple[str(item2)]
    result = is_shadowed(world_object, point_object)
    assert(result == True)


@then("color_at({item1:TestObject}, {item2:TestRay}) should terminate successfully")
def step_then_terminates_successfully(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.dict.keys())
    world_object = context.dict[str(item1)]
    ray_object = context.dict[str(item2)]
    result = color_at(world_object, ray_object, 5)
    assert(result is not None)





@given("{item:TestObject} ← the first object in {item2:TestObject}")
def step_default_world_first_object(context, item, item2):
    assert (item2 in context.dict.keys())
    object_list = context.dict[str(item2)].objects
    assert(len(object_list) > 0)
    first_object = object_list[0]
    context.dict[str(item)] = first_object



@given("{item:TestObject} ← the second object in {item2:TestObject}")
def step_default_world_second_object(context, item, item2):
    assert (item2 in context.dict.keys())
    object_list = context.dict[str(item2)].objects
    assert(len(object_list) > 1)
    second_object = object_list[1]
    context.dict[str(item)] = second_object



@given("{item:TestObject} ← intersection({item2:TestObject}")
def step_default_world_first_object(context, item, item2):
    assert (item2 in context.dict.keys())
    object_list = context.dict[str(item2)].objects
    assert (len(object_list) > 0)
    first_object = object_list[1]
    context.dict[str(item)] = first_object


@given("{item:TestVariable} ← point({x:g}, {y:g}, {z:g})")
def step_impl_point_assign_B(context, item, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = point(np.float32(x), np.float32(y), np.float32(z))



@given("{item:TestObject} ← true")
def step_impl_logic_assign_true(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = True




@given("{item:TestVariable} ← vector({x:g}, √{ynum:g}/{ydenom:g}, -√{znum:g}/{zdenom:g})")
def step_impl_vector_assign_B(context, item, x, ynum, ydenom, znum, zdenom):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(np.float32(x), np.sqrt(np.float32(ynum)) / np.float32(ydenom), -np.sqrt(np.float32(znum)) / np.float32(zdenom))
    

@given("{item:TestVariable} ← vector({x:g}, {y:g}, -{z:g})")
def step_impl_vector_assign_C(context, item, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(np.float32(x), np.float32(y), -np.float32(z))


@given("{item:TestVariable} ← vector({x:g}, {y:g}, {z:g})")
def step_impl_vector_assign_D(context, item, x, y, z):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(np.float32(x), np.float32(y), np.float32(z))


@given("{item:TestVariable} ← vector({x:g}, -√{ynum:g}/{ydenom:g}, -√{znum:g}/{zdenom:g})")
def step_impl_vector_assign_E(context, item, x, ynum, ydenom, znum, zdenom):
    ensure_context_has_tuple(context)
    context.tuple[item] = vector(np.float32(x), -np.sqrt(np.float32(ynum)) / np.float32(ydenom),
                                          -np.sqrt(np.float32(znum)) / np.float32(zdenom))


@given("{item:TestObject} ← material()")
def step_impl_generic_material(context, item):
    ensure_context_has_dict(context)
    context.dict[item] = material()







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
    lighting_value = lighting(material_val, light_val, point_value, eye_vec_value, norm_vec_value)
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
    lighting_value = lighting(material_val, light_val, point_value, eye_vec_value, norm_vec_value, in_shadow_value)
    context.tuple[str(item)] = lighting_value


@then("{item:TestObject}.{element:MaterialElement} = color({red:g}, {green:g}, {blue:g})")
def step_impl_ray_intersect_list_count(context, item, element, red, green, blue):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    local_object = eval(local_object_str)
    value = color(np.float32(red), np.float32(green), np.float32(blue))
    assert(equal(local_object, value))



@then("{item:TestVariable} = color({red:g}, {green:g}, {blue:g})")
def step_lighting_color_test(context, item, red, green, blue):
    assert(item in context.tuple.keys())
    local_object_str = "context.tuple['"+str(item)+"']"
    local_object = eval(local_object_str)
    value = color(np.float32(red), np.float32(green), np.float32(blue))
    assert(equal(local_object, value))


@then("{item1:TestVariable} = {item2:TestObject}.material.color")
def step_then_material_color_test(context, item1, item2):
    assert(item1 in context.tuple.keys())
    assert(item2 in context.dict.keys())
    local_color = context.tuple[str(item1)]
    material_color = context.dict[str(item2)].material.color
    assert(equal(local_color, material_color))
