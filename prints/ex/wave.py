#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
import time

#
#  df/dt = c df/dx
#

def f0(x, a, b):
    c = (a + b) / 2.0
    wave_len = (b - a) / 50.0
    if abs(x - c) > wave_len:
        return 0
    return - abs(x - c) + wave_len

def do_sim1(f0, a=0.0, b=10.0, T=10.0, n=10000, n_steps=100000):
    X = np.linspace(a, b, n)
    u = np.array([ f0(x, a, b) for x in X ])
    plots = []
    plots.append(plt.plot(X, u))
    du = np.zeros(n)
    dt = T / float(n_steps)
    dx = (b - a) / float(n - 1)
    c = 0.1
    t = 0.0
    for i in range(n_steps):
        u[1:n-1] += (u[2:n] - u[1:n-1]) * (c * dt / dx)
        if int(t * 1000 / 25) < int((t + dt) * 1000 / 25):
            plots.append(plt.plot(X, u))
        t = t + dt
    return plots

def do_sim2(f0, a=0.0, b=10.0, T=10.0, n=10000, n_steps=100000):
    X = np.linspace(a, b, n)
    u = np.array([ f0(x, a, b) for x in X ])
    [ line ] = plt.plot(X, u)
    du = np.zeros(n)
    dt = T / float(n_steps)
    dx = (b - a) / float(n - 1)
    c = 1.0
    t = 0.0
    for i in range(n_steps):
        t0 = time.time()
        if 1:
            u[1:n-1] += (u[2:n] - u[1:n-1]) * (c * dt / dx)
        else:
            for i in range(1, n - 1):
                u[i] += (u[i+1] - u[i]) * (c * dt / dx)
        t1 = time.time()
        #print t1 - t0
        if int(t * 1000 / 25) < int((t + dt) * 1000 / 25):
            line.set_data(X, u)
            yield [ line ]
        t = t + dt

if 0:
    ani = animation.ArtistAnimation(plt.gcf(), do_sim1(f0), 
                                    interval=25, blit=1, repeat=0)
    plt.show()

class IterAnimation(animation.FuncAnimation):
    def __init__(self, fig, iterator, **kwargs):
        def f(*args):
            try:
                return iterator.next()
            except StopIteration:
                return []
        animation.FuncAnimation.__init__(self, fig, f, **kwargs)

ani = IterAnimation(plt.gcf(), do_sim2(f0), 
                    interval=25, repeat=0)
plt.show()


print "OK"
