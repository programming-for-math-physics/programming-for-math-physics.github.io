#!/usr/bin/python3
from vpython import *

def koma():
    m = 1.0
    I = 10.0
    w = vector(1,2,0)
    g = vector(0, -9.8, 0)
    stick_len = 10.0
    rg_len = 5.0
    cylinder(axis=vector(0,20,0), radius=0.1, color=color.yellow)
    box(height=0.1, width=1.0, depth=1.0)
    stick = cylinder(axis=stick_len * w / w.mag, radius=0.2)
    traj = points()
    traj.append(stick.axis)
    scene.autoscale = 0
    scene.autocenter = 0
    T = 100.0
    dt = 0.01
    n = int(T / dt)
    for i in range(n):
        rate(1.0 / dt)
        T = (rg_len * w / w.mag).cross(m * g)
        w += (T / I) * dt
        stick.axis = stick_len * w / w.mag
        traj.append(stick.axis)

koma()
