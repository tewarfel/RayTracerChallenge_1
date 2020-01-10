#from vec3 import Vec3, vec3
#from vec4 import * # Vec4, point, vector

from memblock import *
import numpy as np
from shape import material, sphere, cube, test_shape, plane, point_light

from base import render, translation, scaling, view_transform, world, camera, color, rotation_y, rotation_z, rotation_x, stripe_pattern


def main():
    floor = plane()
    floor.material = material()
    floor.material.color = color(0.9, 0.35, 0.25)
    floor.material.specular = 0
    
    
    middle = sphere(sphere_material=material(material_color=color(0.05, 0.5, 0.25), diffuse=0.25, specular=0.8,
                                                                  transparency=0.97, refractive_index=1.5,
                                                                  shininess=300,
                                                                  pattern=stripe_pattern(color(0.05, 0.5, 0.25),
                                                                                         color(0.5, 0.25, 0.05), transform=scaling(0.25, 0.25, 0.25))),
                    sphere_transform=translation(-0.5, 1, 0.5))
        
    right  = sphere(sphere_material=material(material_color=color(0.15, 0, 0),
                                                                  diffuse=0.15, specular=0.95, transparency = 0.95,
                                                                  reflective=0.98, ambient=0.01, refractive_index=1.5,
                                                                  shininess=300),
                    sphere_transform=np.matmul(translation(1.5, 0.5, -0.5), scaling(0.65, 0.65, 0.65)))
        
    left  = cube(cube_material=material(material_color=color(0.2, 0.2, 0.4), diffuse=0.2, specular=0.9, transparency=0.9, shininess=250, refractive_index=1.25),
                    cube_transform=np.matmul(translation(-1.5, 0.33, -0.75), scaling(0.4, 0.4, 0.4)))
        
    light_source = point_light(point(-10, 10, -10), color(1, 1, 1))
    
    this_world = world()
    this_world.objects=[floor, middle, left, right]
    this_world.light = [light_source]
    
    this_camera = camera(1600, 800, np.pi/3)
    this_camera.set_transform(view_transform(point(0, 1.5, -5), point(0, 1, 0), vector(0, 1, 0)))
    
    c = render(this_camera, this_world)
    c.write_image("second_render_cubeC.png")

if __name__ == "__main__":
    main()

#print("Vec4s still active:", Vec4.active_count)
#print("max number of Vec4s active:", Vec4.max_active)
#print("Vec4s used:", Vec4.total_used)

#print("Vec3s still active:", Vec3.active_count)
#print("max number of Vec3s active:", Vec3.max_active)
#print("Vec3s used:", Vec3.total_used)