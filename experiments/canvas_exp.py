from base import *


class Projectile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def projectile(position, velocity):
    return Projectile(position, velocity)



class Environment:
    def __init__(self, gravity, wind):
        self.gravity = gravity
        self.wind = wind


def environment(gravity, wind):
    return Environment(gravity, wind)



def tick(env, proj):
    new_position = proj.position + (0.125 * proj.velocity)
    new_velocity = proj.velocity + (0.125 * (env.gravity + env.wind))
    return projectile(new_position, new_velocity)



start = point(0,1,0)
velocity = normalize(vector(1, 1.8,0)) * 11.25
p = projectile(start, velocity)

gravity = vector(0, -0.1, 0)
wind = vector(-0.01, 0, 0)
e = environment(gravity, wind)

c = canvas(900, 550)

done = False
while (not done):
    #print("p is ", p)
    #print("p.position is ", p.position)
    
    x = p.position.x
    y = p.position.y
    if y<0:
        done = True
    if x<0:
        done = True
    if x > c.width:
        done = True
    
    if not done:
        c.write_pixel(x,y,color(1.0, 0, 0))
        p = tick(e, p)
      
        
c.write_image("arc.png")
