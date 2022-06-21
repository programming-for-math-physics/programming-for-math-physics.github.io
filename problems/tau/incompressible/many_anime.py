#!/usr/bin/python3
# %matplotlib notebook
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def mainx():
    fig = plt.figure()
    ax0 = fig.add_subplot(1,2,1)
    ax1 = fig.add_subplot(1,2,2)
    x = np.linspace(0.0, 2.0 * np.pi, 100)
    for k in range(1, 6):
        if k == 1:
            [ line0 ] = ax0.plot(x, np.sin(k * x))
            [ line1 ] = ax1.plot(x, np.cos(k * x))
        else:
            line0.set_data(x, np.sin(k * x))
            line1.set_data(x, np.cos(k * x))
        plt.pause(0.5)

def shrink(f):
    m,n = f.shape
    return f[:m-1,:n-1].flatten()
        
def main():
    fig = plt.figure()
    ax0 = fig.add_subplot(1,2,1)
    #ax1 = fig.add_subplot(1,2,2)
    x = np.linspace(0.0, 2.0, 10)
    y = np.linspace(0.0, 1.0, 5)
    x,y = np.meshgrid(x, y)
    m,n = x.shape
    for k in range(1, 100):
        if k == 1:
            #f0 = ax0.pcolor(x, y, y - np.sin(k * x))
            #f1 = ax1.pcolor(x, y, y - np.cos(k * x))
            f0 = ax0.quiver(x, y,
                            np.cos(k * x),
                            np.sin(k * x))
            #f1 = ax1.quiver(x, y, y - np.cos(k * x))
        else:
            f0.set_UVC(np.cos(k * x), np.sin(k * x), None)
            #f1.set_array(shrink(y - np.cos(k * x)))
        plt.pause(1.0)

main()
