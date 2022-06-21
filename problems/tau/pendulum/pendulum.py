#!/usr/bin/python3
from vpython import *
import math

def pendulum():
    theta = 0.0
    theta_ = 1.0
    l = 10.0
    ball = sphere(pos=l * vector(math.sin(theta), -math.cos(theta), 0))
    stick = cylinder(axis=ball.pos, radius=0.2)
    scene.autoscale = 0
    scene.autocenter = 0
    T = 100
    dt = 0.01
    n = int(T / dt)
    g = 9.8
    for i in range(n):
        rate(1.0/dt)
        theta__ = - (g/l) * math.sin(theta)
        theta_ += theta__ * dt
        theta  += theta_ * dt
        ball.pos = l * vector(math.sin(theta), -math.cos(theta), 0)
        stick.axis = ball.pos
    
pendulum()
