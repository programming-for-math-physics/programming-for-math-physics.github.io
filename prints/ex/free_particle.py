#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
import time
import random

def init(rg, a, b, x):
    c = a + (b - a) * 0.4
    d = a + (b - a) * 0.5
    e = a + (b - a) * 0.6
    if c <= x <= e:
        return rg.random() + 1.0j * rg.random()
        return (e - d) - abs(x - d) + 0.0j 
        return 1.0 + 0.0j
        return ((x - c) * (x - e)) ** 2 + 0.0j
    else:
        return 0.0 + 0.0j

def sim():
    rg = random.Random()
    hs = 6.62606957e-34 / (2.0 * math.pi)
    m = 9.10938291e-31
    # 2.8179402894 * 10^{-15}
    a,b = 0.0,1.0e-14
    n = (1 << 10) + 1
    dx = (b - a) / n
    dt = 1.0e-1 * (2.0 * m * dx * dx / hs)
    n_steps = 10000000
    X = np.linspace(a, b, n)
    u  = np.array([ init(rg, a, b, x) for x in X ])
    u /= math.sqrt(sum(u * u.conj()) * (b - a) / n)
    [ line ] = plt.plot(X, abs(u))
    u_ = np.zeros(n)
    u_[1:n-1] = u[1:n-1] + (u[2:n] + u[0:n-2] - 2*u[1:n-1]) * (1.0j * hs * dt / (2.0 * m * dx * dx))
    t = 0
    for i in xrange(n_steps):
        # i h du/dt = -h^2 /2m nabla u 
        # u(t+dt) - u(t) = ih/2m nabla u dt
        # u[1:n-1] = u_[1:n-1] + (u_[2:n] + u_[0:n-2] - 2*u_[1:n-1]) * (1.0j * hs * dt / (2.0 * m * dx * dx))
        u[1:n-1] = u[1:n-1] + (u_[2:n] + u_[0:n-2] - 2*u_[1:n-1]) * (1.0j * hs * dt / (2.0 * m * dx * dx))
        if i % 1000 == 0:
            line.set_data(X, abs(u))
            print t, (sum(u * u.conj()) * (b - a) / n)
            yield [line]
        u,u_ = u_,u
        t += dt

class IterAnimation(animation.FuncAnimation):
    def __init__(self, fig, iterator, **kwargs):
        def f(*args):
            try:
                return iterator.next()
            except StopIteration:
                return []
        animation.FuncAnimation.__init__(self, fig, f, **kwargs)

ani = IterAnimation(plt.gcf(), sim(),
                    interval=25, repeat=0)
plt.show()

