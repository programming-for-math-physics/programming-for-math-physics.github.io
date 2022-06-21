from visual import *
import math

def f(t):
    return vector(0, math.sin(math.sqrt(2) * t), 0)

def spring(k, m, f):
    g = 9.8
    l = 3.0
    y_min = - m * g / k * 2
    ceil  = box(pos=vector(0,l,0), length=5, height=0.1, width=5)
    floor = box(pos=vector(0,-1+y_min,0), length=5, height=0.1, width=5)
    s0 = sphere(radius=1.0)
    s = sphere(pos=vector(0,0,0), radius=1.0,
               vel=vector(0,0,0), color=color.yellow)
    h = helix(pos=(0,l,0), axis=(0,-l,0), radius=0.5, thickness=0.2)
    dt = 0.1
    for i in range(1000):
        rate(10)
        ay = - k * s.pos.y / m - g
        s.acc = vector(0, ay, 0)#  + f(i * dt)
        s.vel = s.vel + s.acc * dt
        s.pos = s.pos + s.vel * dt
        h.axis = (0, s.pos.y - l, 0)
        
def main():
    spring(1.5, 1.0, f)

main()

