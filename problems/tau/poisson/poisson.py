#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# u[0:m,0:n]
def poisson(u, T, dt, h):
    fig = plt.figure()
    m,n = u.shape
    X = np.arange(0, m) * h
    Y = np.arange(0, n) * h
    X,Y = np.meshgrid(X, Y)
    imgs = []
    n_imgs = 100
    n_iters = int(T/dt)
    for i in range(n_iters):
        u[1:m-1,1:n-1] += (u[0:m-2,1:n-1] + u[2:m,1:n-1] + u[1:m-1,0:n-2] + u[1:m-1,2:n] - 4 * u[1:m-1,1:n-1]) * (dt/(h*h))
        if ((i - 1) * n_imgs) // n_iters < (i * n_imgs) // n_iters:
            imgs.append([plt.pcolor(X, Y, u)])
            print("   imgs: %d" % len(imgs))
    ani = animation.ArtistAnimation(fig, imgs, interval=500)
    plt.show()
    return ani
    
def main():
    m,n = 100,100
    h = 1.0 / m
    u = np.random.random((m,n))
    if 1:
        u[0:m,0]   = np.random.random(m) * 0.1
        u[0,0:n]   = np.random.random(n) * 0.1
        u[0:m,n-1] = np.arange(0, m) * h + np.random.random(m) * 0.1
        u[m-1,0:n] = np.arange(0, n) * h + np.random.random(n) * 0.1
    T = 0.01
    dt = h * h * 0.1
    return poisson(u, T, dt, h)
    
ani = main()
