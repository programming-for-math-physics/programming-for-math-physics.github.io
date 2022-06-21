import numpy as np
import matplotlib.pyplot as plt
import math

# solve partial f / partial t = partial f / partial x
# in 0 <= x <= 1, 0 <= t <= 1

def f0(x):
    return np.sin(x)

def solve(f0):
    nx = 1001
    nt = 1000
    dx = math.pi / (nx - 1)
    dt = math.pi / nt
    x = np.linspace(0,math.pi,nx)
    f = f0(x)
    for i in range(10):
        f[:-1] = f[:-1] - (f[1:] - f[:-1]) * dt / dx
    plt.plot(x, f)
    plt.show()

print "OK"
