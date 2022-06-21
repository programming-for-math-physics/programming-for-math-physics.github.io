#!/usr/bin/python3

from vpython import *
#from visual import *
import random,sys

def Ws(s):
    sys.stdout.write(s)

def interact(a, b):
    ab = b.pos - a.pos
    r = (a.radius + b.radius) / ab.mag
    f = r - r * r * r
    fv = ab / ab.mag * f
    a.acc += fv / a.mass
    b.acc -= fv / b.mass
    return ab.mag
        
def collision(a, b):
    x = b.pos - a.pos
    v = b.vel - a.vel
    e = 0.95
    if x.mag < a.radius + b.radius and x.dot(v) < 0:
        # a.m * a.v' + b.m * b.v' = a.m * a.v + b.m * b.v
        #  -1 * a.v' +   1 * b.v' =   e * a.v -   e * b.v
        avel_new = ((a.mass - e * b.mass) * a.vel + (b.mass + e * b.mass) * b.vel) / (a.mass + b.mass)
        bvel_new = ((a.mass + e * a.mass) * a.vel + (b.mass - e * a.mass) * b.vel) / (a.mass + b.mass)
        a.vel = avel_new
        b.vel = bvel_new
        return 1
    else:
        return 0

def step(B, t, dt):
    for a in B:
        a.acc = - a.pos / a.pos.mag
        a.acc += -0.1 * a.vel
    dt_abs = []
    D = []
    for i,a in enumerate(B):
        for j,b in enumerate(B):
            if i < j:
                d = interact(a, b)
                D.append((i,j,d))
                # Ws("%.3f : dist %d - %d = %f\n" % (t, i, j, d))
    for a in B:
        a.vel += a.acc * dt
        a.pos += a.vel * dt
    n_cols = 0
    for i,a in enumerate(B):
        for j,b in enumerate(B):
            if i < j:
                c = collision(a, b)
                if c > 0:
                    # Ws("%.3f : collision %d - %d\n" % (t, i, j))
                    pass
                n_cols += c
    # assert (n_cols < 2), n_cols
    return D

def rand_float(rg, a, b):
    return a + (b - a) * rg.random()
        
def random_vec(rg):
    return vector(rand_float(rg, -1, 1),
                  rand_float(rg, -1, 1),
                  rand_float(rg, -1, 1))
    
def init2(n):
    rg = random.Random()
    rg.seed(123)
    a = sphere(pos=random_vec(rg), mass=1.0)
    b = sphere(pos=random_vec(rg), mass=1.0)
    a.vel = b.pos - a.pos
    b.vel = a.pos - b.pos
    scene.autoscale = 0
    scene.autocenter = 0
    return [ a, b ]
    
def init(n):
    sphere(color=color.yellow, radius=0.05)
    rg = random.Random()
    a = 5 * n ** (1.0/3.0)
    B = [ sphere(pos=a * random_vec(rg),
                 vel=vector(0,0,0),mass=1.0) for i in range(n) ]
    scene.autoscale = 0
    scene.autocenter = 0
    return B
    
def run(n, T, dt):
    B = init(n)
    n_steps = int(T / dt) + 1
    t = 0.0
    for i in range(n_steps):
        rate(30)
        step(B, t, dt)
        t += dt

def main():
    n = 4
    T = 100.0
    dt = 1.0e-2
    run(n, T, dt)

main()
