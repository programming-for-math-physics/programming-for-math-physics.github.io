from visual import *
import math

def free_fall(theta):
    v0 = 20.0
    x = arrow(axis=(50.0,0,0), shaftwidth=1.0)
    y = arrow(axis=(0,50.0,0), shaftwidth=1.0)
    s = sphere(vel=vector(v0 * math.cos(theta), 
                          v0 * math.sin(theta), 0.0),
               color=color.yellow)
    g = vector(0.0, 9.8, 0.0)
    dt = 0.01
    for i in range(1000):
        rate(1.0/dt)
        s.pos = s.pos + s.vel * dt
        s.vel = s.vel - g * dt
        if s.pos.y < 0.0:
            break
    
free_fall(math.pi / 3.0)

