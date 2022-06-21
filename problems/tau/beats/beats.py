#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

def beats():
    f1 = 1000
    f2 = 997
    t = np.linspace(0, 1, 10000)
    y1 = np.sin(2 * np.pi * f1 * t)
    y2 = np.sin(2 * np.pi * f2 * t)
    plt.plot(t, y1 + y2)
    plt.show()
    
beats()
