#!/usr/bin/python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as anm

# [0,1]x[0,1]の領域を1辺hの正方形に区切り, 
# dtずつ時刻を進めて, 時刻Tまでシミュレートする

def wave1d(fig, h, dt, end_t):
    ax = fig.add_subplot(111)
    ax.set_ylim(-2.0, 2.0)
    k = 0.1
    c = 1
    n = int(1/h)
    n1 =       n // 4
    n2 = (2 * n) // 4
    n3 = (3 * n) // 4
    x = np.linspace(0,1,n)
    y = np.zeros(n)
    y[:n2] = np.sin(2 * np.pi * x[:n2])
    # y[n1:n3] = np.ones(n3 - n1)
    v = np.zeros(n)
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        v[1:n-1] += (c * c / (h * h) * dt) * (y[0:n-2] - 2 * y[1:n-1] + y[2:n])
        v[n-1] = v[n-2]
        y += v * dt
        if s == 0:
            [ line ] = ax.plot(x, y)
        else:
            line.set_data(x, y)
        yield [ line ]

def animate_wave1d(h, dt, end_t):
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=wave1d(fig, h, dt, end_t), 
                            interval=30)
    plt.show()
    return ani

def shrink(z):
    # z : 2次元配列 を縦横1ずつ縮めて, かつ無理やり1次元の配列に直す
    m,n = z.shape
    return z[:m-1,:n-1].reshape((m - 1) * (n - 1))

def wave2dx(fig, h, dt, end_t):
    ax = fig.add_subplot(111)
    k = 0.1
    c = 1
    n = int(1/h)
    n1 =       n // 4
    n2 = (2 * n) // 4
    n3 = (3 * n) // 4
    x = np.linspace(0,1,n)
    y = np.linspace(0,1,n)
    x,y = np.meshgrid(x, y)
    z = np.zeros((n,n))
    z = np.maximum(z, 0.1 - (x - 0.5)**2 - (y - 0.5)**2)
    # y[n1:n3] = np.ones(n3 - n1)
    v = np.zeros((n, n))
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        v[1:n-1,1:n-1] += (c * c / (h * h) * dt) * (z[0:n-2,1:n-1] + z[2:n,1:n-1] + z[1:n-1,0:n-2] + z[1:n-1,2:n] - 4 * z[1:n-1,1:n-1])
        z += v * dt
        if s == 0:
            pc = ax.pcolor(x, y, z)
        else:
            pc.set_array(shrink(z))
        yield [ pc ]

def wave2dxx(fig, h, dt, end_t):
    ax = fig.add_subplot(111, projection="3d")
    k = 0.1
    c = 1
    n = int(1/h)
    x = np.linspace(0,1,n)
    y = np.linspace(0,1,n)
    x,y = np.meshgrid(x, y)
    z = np.zeros((n,n))
    z = np.maximum(z, 0.1 - (x - 0.5)**2 - (y - 0.5)**2)
    # y[n1:n3] = np.ones(n3 - n1)
    v = np.zeros((n, n))
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        print(s)
        v[1:n-1,1:n-1] += (c * c / (h * h) * dt) * (z[0:n-2,1:n-1] + z[2:n,1:n-1] + z[1:n-1,0:n-2] + z[1:n-1,2:n] - 4 * z[1:n-1,1:n-1])
        z += v * dt
        ax.clear()
        sfc = ax.plot_surface(x, y, z)
        ax.set_zlim(-2,2)
        yield
        
def animate_wave2d(h, dt, end_t):
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=wave2dxx(fig, h, dt, end_t), 
                            interval=30)
    plt.show()
    print("done")
    return ani

#animate_wave1d(1.0e-2, 1.0e-2, 5.0)
animate_wave2d(1.0e-2, 1.0e-3, 5.0)
