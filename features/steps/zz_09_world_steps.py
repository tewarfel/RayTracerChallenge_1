from behave import *
from hamcrest import assert_that, equal_to
import base
from parse_type import TypeBuilder
import numpy as np


valid_test_objects = ["w", "s1", "s2", "light", "shape", "i", "comps", "outer", "inner"]
parse_test_object = TypeBuilder.make_choice(valid_test_objects)
register_type(TestObject=parse_test_object)

valid_test_variables = ["intensity", "position", "eyev", "normalv", "result", "c", "p"]
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
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.world()




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
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    real_position = base.point(float(px), float(py), float(pz))
    real_intensity = base.color(float(red), float(green), float(blue))
    context.dict[item] = base.point_light(real_position, real_intensity)


@given("{item:TestObject}.light ← point_light(point({px:g}, {py:g}, {pz:g}), color({red:g}, {green:g}, {blue:g}))")
def step_impl_point_light_for_world(context, item, px, py, pz, red, green, blue):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}

    real_position = base.point(float(px), float(py), float(pz))
    real_intensity = base.color(float(red), float(green), float(blue))
    context.dict[item].light = [base.point_light(real_position, real_intensity)]


@given("{item:TestObject} ← sphere()")
def step_given_s_is_sphere(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.sphere()


@given("{item:TestObject} is added to {world:TestObject}")
def step_given_item_added_to_world(context, item, world):
    assert(item in context.dict.keys())
    assert(world in context.dict.keys())
    context.dict[str(world)].objects.append(context.dict[str(item)])
    print(context.dict[str(world)].objects)
    

@given("{item:TestObject} ← sphere() with translation({x}, {y}, {z})")
def step_given_s_is_sphere_with_translation(context, item, x, y, z):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = base.sphere(sphere_transform=base.translation(float(x), float(y), float(z)))


@given("{item:TestObject} ← sphere(sphere_material=material(material_color=({red}, {green}, {blue}), diffuse={d}, specular={sp}))")
def step_impl_sphere_with_material(context, item, red, green, blue, d, sp):
    the_material_color = base.color(float(red), float(green), float(blue))
    new_material = base.material(material_color=the_material_color, diffuse=float(d), specular=float(sp))
    new_sphere = base.sphere(sphere_material=new_material)
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = new_sphere


@given("{item:TestObject} ← sphere(sphere_transform=transform(scaling({x}, {y}, {z})))")
def step_impl_sphere_with_transform(context, item, x, y, z):
    new_transform = base.scaling(float(x), float(y), float(z))
    new_sphere = base.sphere(sphere_transform=new_transform)
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[str(item)] = new_sphere



@given("{item:TestObject} ← default_world()")
def step_default_world_create(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.default_world()




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




@when("{item:TestObject} ← default_world()")
def step_default_world_create(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.default_world()



@when("{item:ListName} ← intersect_world({w:TestObject}, {r:TestRay})")
def step_intersect_world_ray(context, item, w, r):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    test_ray = context.dict[str(r)]
    print(test_ray.__dict__)
    print(context.dict[str(w)].__dict__)
    context.dict[str(item)] = base.intersect_world(context.dict[str(w)], context.dict[str(r)])


@when("{item:TestVariable} ← shade_hit({w:TestObject}, {comps:TestObject})")
def step_shade_hit_world(context, item, w, comps):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    world_object = context.dict[str(w)]
    comps_object = context.dict[str(comps)]
    context.tuple[str(item)] = base.shade_hit(world_object, comps_object)


@when("{item:TestVariable} ← color_at({w:TestObject}, {r:TestRay})")
def step_shade_hit_world(context, item, w, r):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}
    world_object = context.dict[str(w)]
    ray_object = context.dict[str(r)]
    resulting_color = base.color_at(world_object, ray_object)
    print("color_at result is ", resulting_color)
    context.tuple[str(item)] = resulting_color





@then("{item:TestObject}.{element:WorldElement} = {item2:TestObject}")
def step_default_world_contains_element(context, item, element, item2):
    assert(item in context.dict.keys())
    local_object_str = "context.dict['"+str(item)+"']."+str(element)
    light_list = eval(local_object_str)
    test_value = context.dict[str(item2)]

    match_found = False
    for source in light_list:
        if base.equal(source.position,test_value.position):
            if base.equal(source.intensity, test_value.intensity):
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
   
        if match_found and base.equal(thing.transform, test_object.transform):
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
    result = base.is_shadowed(world_object, point_object)
    assert(result == False)


@then("is_shadowed({item1:TestObject}, {item2:TestVariable}) is true")
def step_then_is_shadowed_is_false(context, item1, item2):
    assert(item1 in context.dict.keys())
    assert(item2 in context.tuple.keys())
    world_object = context.dict[str(item1)]
    point_object = context.tuple[str(item2)]
    result = base.is_shadowed(world_object, point_object)
    assert(result == True)





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
def step_impl_generic_material(context, item):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
    context.dict[item] = base.material()







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



@then("{item:TestVariable} = color({red:g}, {green:g}, {blue:g})")
def step_lighting_color_test(context, item, red, green, blue):
    assert(item in context.tuple.keys())
    local_object_str = "context.tuple['"+str(item)+"']"
    local_object = eval(local_object_str)
    value = base.color(float(red), float(green), float(blue))
    print("local object is ", local_object)
    print(value)
    assert(base.equal(local_object, value))


@then("{item1:TestVariable} = {item2:TestObject}.material.color")
def step_then_material_color_test(context, item1, item2):
    assert(item1 in context.tuple.keys())
    assert(item2 in context.dict.keys())
    local_color = context.tuple[str(item1)]
    material_color = context.dict[str(item2)].material.color
    print("local color is ", local_color)
    print(item2, " material color is ", material_color)
    assert(base.equal(local_color, material_color))
