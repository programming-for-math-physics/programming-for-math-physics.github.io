from math import cos, log, pi
#import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt

def g(t):
    return cos(t) * log(cos(t))

def integral(g, a, b):
    n = 3000
    dt = (b - a) / n
    rng = np.linspace(a, b, n + 1)
    s = sum(g(t) + g(t + dt) for t in rng[:-1])
    return 0.5 * dt * s

def f(x):
    return (cos(x) * log(cos(x))
            - cos(x) + integral(g, 0, x))

def graph(f, a, b):
    n = 3000
    dt = (b - a) / n
    X = np.linspace(a, b, n + 1)
    Y = [f(x) for x in X]
    plt.plot(X, Y)
    plt.show()

def minimize(f, a, b):
    n = 3000
    dt = (b - a) / n
    X = np.linspace(a, b, n + 1)
    return min((f(t), t) for t in X)

def main():
    return minimize(f, 0, pi/2)
    #return graph(f, 0, 1)
    # return graph(f, 0.78, 0.79)
