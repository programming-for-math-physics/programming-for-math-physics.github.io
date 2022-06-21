import numpy as np
import matplotlib.pyplot as plt
import math

def plot_practice():
    plt.plot([1,2,3,4],[1,-1,2,-2])
    plt.show()

def plot_sin():
    X = np.linspace(0.0, 2.0 * math.pi, 100)
    Y = np.sin(X)
    plt.plot(X, Y)
    plt.show()

def scatter_disc():
    X0 = np.random.random(1000) * 2.0 - 1.0
    Y0 = np.random.random(1000) * 2.0 - 1.0
    X = []
    Y = []
    for x,y in zip(X0, Y0):
        if x * x + y * y < 1.0:
            X.append(x)
            Y.append(y)
    plt.scatter(X, Y)
    plt.show()

def xx_pcolor():
    X = np.linspace(-5,5,200)
    Y = np.linspace(-5,5,100)
    X,Y = np.meshgrid(X, Y)
    plt.pcolor(X, Y, X*X - X *Y + Y*Y - X - Y)
    plt.show()

import mpl_toolkits.mplot3d.axes3d

def xx_surface():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,projection='3d')
    X = np.linspace(-5,5,200)
    Y = np.linspace(-5,5,100)
    X,Y = np.meshgrid(X, Y)
    ax.plot_surface(X, Y, X*X - X *Y + Y*Y - X - Y)
    fig.show()

    
print "OK"
