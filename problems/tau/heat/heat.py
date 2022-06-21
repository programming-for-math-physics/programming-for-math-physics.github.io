import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anm

# [0,1]x[0,1]の領域を1辺hの正方形に区切り, 
# dtずつ時刻を進めて, 時刻Tまでシミュレートする

def heat1d(h, dt, end_t):
    ax = fig.add_subplot(111)
    k = 0.1
    n = int(1/h)
    X = np.linspace(0,1,n)
    T = np.sin(np.pi * X)
    T[0] = 0
    T[n-1] = 1
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        T[1:n-1] += (k * dt / (h*h)) * (T[0:n-2] - 2 * T[1:n-1] + T[2:n])
    plt.plot(X, T)
    plt.show()

def heat1dx(fig, h, dt, end_t):
    ax = fig.add_subplot(111)
    k = 0.1
    n = int(1/h)
    X = np.linspace(0,1,n)
    T = np.sin(np.pi * X)
    T[0] = 0
    T[n-1] = 1
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        T[1:n-1] += (k * dt / (h*h)) * (T[0:n-2] - 2 * T[1:n-1] + T[2:n])
        if s == 0:
            [ line ] = ax.plot(X, T)
        else:
            line.set_data(X, T)
        yield [ line ]

def animate_heat1d(h, dt, end_t):
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=heat1dx(fig, h, dt, end_t), 
                            interval=30)
    plt.show()
    return ani

def heat2d(h, dt, end_t):
    k = 0.1
    n = int(1/h)
    X = np.linspace(0,1,n)
    Y = np.linspace(0,1,n)
    X,Y = np.meshgrid(X,Y)
    T = np.zeros((n,n))
    T[:,0] = 1
    T[0,:] = 1
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        T[1:n-1,1:n-1] = T[1:n-1,1:n-1] + (k * dt / (h*h)) * (T[2:n,1:n-1] + T[0:n-2,1:n-1] + T[1:n-1,2:n] + T[1:n-1,0:n-2] - 4*T[1:n-1,1:n-1])
    plt.pcolor(X, Y, T)
    plt.show()

def shrink(z):
    # z : 2次元配列 を縦横1ずつ縮めて, かつ無理やり1次元の配列に直す
    m,n = z.shape
    return z[:m-1,:n-1].reshape((m - 1) * (n - 1))

def heat2dx(fig, h, dt, end_t):
    ax = fig.add_subplot(111)
    k = 0.1
    n = int(1/h)
    X = np.linspace(0,1,n)
    Y = np.linspace(0,1,n)
    X,Y = np.meshgrid(X,Y)
    T = np.zeros((n,n))
    T[:,0] = 1
    T[0,:] = 1
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        T[1:n-1,1:n-1] = T[1:n-1,1:n-1] + (k * dt / (h*h)) * (T[2:n,1:n-1] + T[0:n-2,1:n-1] + T[1:n-1,2:n] + T[1:n-1,0:n-2] - 4*T[1:n-1,1:n-1])
        if s == 0:
            pc = plt.pcolor(X, Y, T)
        else:
            pc.set_array(shrink(T))
        yield [ pc ]

def animate_heat2d(h, dt, end_t):
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=heat2dx(fig, h, dt, end_t), 
                            interval=30)
    plt.show()
    return ani

# heat1d(1.0e-2, 1.0e-4, 1.0)
# animate_heat1d(1.0e-2, 1.0e-4, 1.0)
# heat2d(1.0e-2, 1.0e-4, 1.0)
animate_heat2d(1.0e-2, 1.0e-4, 1.0)

