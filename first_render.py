from base import *


def __main__():
    floor = sphere(sphere_transform=scaling(10, 0.01, 10))
    floor.material = material()
    floor.material.color = color(1, 0.9, 0.9)
    floor.material.specular = 0
    
    left_wall = sphere()
    left_wall.set_transform(np.matmul(np.matmul(translation(0,0,5), rotation_y(-np.pi / 4)),  np.matmul(rotation_x(np.pi/2), scaling(10, 0.01, 10))))
    
    left_wall.material = material()
    left_wall.material.color = color(0.3, 0.3, 0.9)
    left_wall.material.specular = 0
    
    right_wall = sphere()
    right_wall.set_transform(np.matmul(np.matmul(translation(0,0,5), rotation_y(np.pi / 4)), np.matmul(rotation_x(np.pi/2), scaling(10, 0.01, 10))))
    right_wall.material = floor.material
    
    
    middle = sphere(sphere_material=material(material_color=color(0.1, 1, 0.5), diffuse=0.7, specular=0.3),
                    sphere_transform=translation(-0.5, 1, 0.5))
        
    right  = sphere(sphere_material=material(material_color=color(0.5, 1, 0.1), diffuse=0.7, specular=0.3),
                    sphere_transform=np.matmul(translation(1.5, 0.5, -0.5), scaling(0.5, 0.5, 0.5)))
        
    left  = sphere(sphere_material=material(material_color=color(1, 0.8, 0.1), diffuse=0.7, specular=0.3),
                    sphere_transform=np.matmul(translation(-1.5, 0.33, -0.75), scaling(0.33, 0.33, 0.33)))
        
    light_source = point_light(point(-10, 10, -10), color(1, 1, 1))
    
    this_world = world()
    this_world.objects=[floor, left_wall, right_wall, middle, left, right]
    this_world.light = [light_source]
    
    this_camera = camera(100, 50, np.pi/3)
    this_camera.set_transform(view_transform(point(0, 1.5, -5), point(0, 1, 0), vector(0, 1, 0)))
    
    c = render(this_camera, this_world)
    c.write_image("first_sphere_render_h.png")

__main__()

print("Vec4s still active:", Vec4.active_count)
print("max number of Vec4s active:", Vec4.max_active)
print("Vec4s used:", Vec4.total_used)

print("Vec3s still active:", Vec3.active_count)
print("max number of Vec3s active:", Vec3.max_active)
print("Vec3s used:", Vec3.total_used)