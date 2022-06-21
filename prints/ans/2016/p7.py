#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ∂u     ∂u
# -- = 2 --
# ∂t     ∂x

# u(x,0) =  x + 1 (-1 <= x <= 0)
#          -x + 1 (0  <= x <= 1)
#               0 (|x| > 1)
# u(0,t) = 0
# u(1,t) = 0


# u(x, t+dt) - u(x, t)       u(x+dx,t) - u(x,t)
# --------------------  = 2 --------------------
#          dt                       dx

# u(x,t+dt) = u(x,t) + 2 (u(x+dx,t) - u(x,t)) dt/dx

def sim(T, dt):
    X = np.linspace(-5, 5, 100)
    dx = X[1] - X[0]
    u = np.zeros(X.shape)
    for i,x in enumerate(X):
        if -1 <= x <= 0:
            u[i] = x + 1
        elif 0 <= x <= 1:
            u[i] = -x + 1
    n_steps = int(T / dt)
    for t in range(n_steps):
        u[1:-1] = 2 * (u[2:] - u[1:-1]) * (dt/dx)
    return X,u
    
def main():
    x,u = sim(0.0, 0.1)
    plt.plot(x, u)
    plt.show()

def sim_anime(T, dt):
    X = np.linspace(-5, 5, 100)
    dx = X[1] - X[0]
    u = np.zeros(X.shape)
    for i,x in enumerate(X):
        if -1 <= x <= 0:
            u[i] = x + 1
        elif 0 <= x <= 1:
            u[i] = -x + 1
    n_steps = int(T / dt)
    [line] = plt.plot(X, u)
    for t in range(n_steps):
        u[1:-1] = 2 * (u[2:] - u[1:-1]) * (dt/dx)
        print(t)
        yield [line]
    
def go_animation(iterator, **kwargs):
    def anime_fun(*args):
        try:
            return next(iterator)
        except StopIteration:
            return []
    ani = animation.FuncAnimation(plt.gcf(), anime_fun, **kwargs)
    plt.show()
    
def main_anime():
    T = 10.0
    dt = 0.1
    go_animation(sim_anime(T, dt), interval=100)

main_anime()
