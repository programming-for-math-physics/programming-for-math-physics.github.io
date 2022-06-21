#!/usr/bin/python
#
#  df/dt = nabla f
#
import numpy as np
import matplotlib.pyplot as plt
import random

def solve_heat(X, Y, f, t_end, dt):
    k = 1.0
    m,n = f.shape
    for t in np.arange(0.0, t_end, dt):
        f[1:m-1,1:n-1] += (f[0:m-2,1:n-1] + f[2:m,1:n-1] + f[1:m-1,0:n-2] + f[1:m-1,2:n] - 4.0 * f[1:m-1,1:n-1]) * (k * dt)
    return f

def f0(i, j, n):
    if i == 0:
        return j / float(n)
    elif j == 0:
        return i / float(n)
    elif i == n - 1:
        return 1.0
    elif j == n - 1:
        return 1.0
    else:
        return random.random()

def main():
    n = 100
    T = 1000.0
    dt = 0.1
    X = np.linspace(0.0, 1.0, n)
    Y = np.linspace(0.0, 1.0, n)
    f = np.zeros((n,n))
    # init value
    for i in range(n):
        for j in range(n):
            f[i,j] = f0(i,j,n)
    solve_heat(X, Y, f, T, dt)
    plt.pcolor(X, Y, f)
    plt.show()

print "OK"

main()
