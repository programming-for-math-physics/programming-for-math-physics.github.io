#!/usr/bin/python3

from vpython import *
#from visual import *
import random,sys

def Ws(s):
    sys.stdout.write(s)

k = 1000.0
g = vector(0,9.8,0)
e = 1.0

def adv(k, dt):
    for o,vel,acc in k:
        o.pos_bak = o.pos
        o.vel_bak = o.vel
        o.pos += vel * dt
        o.vel += acc * dt

def restore(O):
    for o in O:
        o.pos = o.pos_bak
        o.vel = o.vel_bak

def rk_step(O, t, dt):
    k1 = calc_acc(O, t)
    adv(k1, dt/2.0)
    k2 = calc_acc(O, t + dt/2)
    restore(O)
    adv(k2, dt/2.0)
    k3 = calc_acc(O, t + dt/2)
    restore(O)
    adv(k3, dt)
    k4 = calc_acc(O, t + dt)
    restore(O)
    adv(k1, dt/6.0)
    adv(k2, dt/3.0)
    adv(k3, dt/3.0)
    adv(k4, dt/3.0)

def calc_acc(O, t):
    for o in O:
        o.acc = -g
    for i in range(0, len(O), 2):
        a = O[i]
        b = O[i+1]
        ab = b.pos - a.pos
        r = ab.mag
        f = k * (r - 1.0)
        a.acc += ab / ab.mag * (f / a.mass)
        b.acc -= ab / ab.mag * (f / b.mass)
    return [ (o, o.vel, o.acc) for o in O ]

def step(O, C, t, dt):
    # the bottom one hits the floor
    a = C[0][0]
    if a.pos.y < 0 and a.vel.y < 0:
        Ws("%.3f : collision 0 - floor\n" % t)
        a.vel.y *= -1
    # the top one ith spring hit the bottom one of the (i+1)th
    for i in range(len(C) - 1):
        a = C[i][1]
        b = C[i+1][0]
        ab = b.pos - a.pos
        abv = b.vel - a.vel
        if ab.y < 0 and abv.y < 0:
            Ws("%.3f : collision %d - %d\n" % (t, i, i + 1))
            #  a.m * a.vel' + b.m * b.vel' = a.m * a.vel + b.m * b.vel
            #   -1 * a.vel' +   1 * b.vel' =   e * a.vel +  -e * b.vel
            avy_new = ((a.mass - e * b.mass) * a.vel.y + (b.mass + e * b.mass) * b.vel.y) / (a.mass + b.mass)
            bvy_new = ((a.mass + e * a.mass) * a.vel.y + (b.mass - e * a.mass) * b.vel.y) / (a.mass + b.mass)
            a.vel.y = avy_new
            b.vel.y = bvy_new
    rk_step(O, t, dt)
    for a,b,s in C:
        s.pos = a.pos
        s.axis = b.pos - a.pos

        
def connected_masses(m, y0, y1):
    zero = vector(0,0,0)
    h = 0.1
    b0 = box(pos=vector(0,y0+h/2.0,0),
             length=1,width=1,height=h,mass=m,vel=zero,
             color=color.blue)
    b1 = box(pos=vector(0,y1-h/2.0,0),
             length=1,width=1,height=h,mass=m,vel=zero,
             color=color.red)
    s = helix(pos=vector(0,y0,0), axis=vector(0,y1-y0,0), radius=0.3)
    return (b0,b1,s)

def init():
    box(pos=vector(0,0,0),length=2,width=2,height=0.1,color=color.yellow)
    box(pos=vector(0,6,0),length=2,width=2,height=0.1,color=color.yellow)
    c0 = connected_masses(1.0, 3, 4)
    c1 = connected_masses(1.0, 4, 5)
    c2 = connected_masses(0.1, 5, 6)
    scene.autoscale = 1
    scene.autocenter = 1
    return [ c0, c1, c2 ]
    
def run(T, dt):
    C = init()
    O = []
    for a,b,s in C:
        O.append(a)
        O.append(b)
    n_steps = int(T / dt) + 1
    t = 0.0
    for i in range(n_steps):
        rate(int(1.0/dt))
        step(O, C, t, dt)
        t += dt

def main():
    T = 10.0
    dt = 1.0e-4
    run(T, dt)

main()
