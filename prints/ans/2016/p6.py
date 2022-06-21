import matplotlib.pyplot as plt
import numpy as np
from visual import *

def dipole():
    n = 75
    a = 1.0
    F = np.zeros((n,n,n))
    P = np.linspace(-a, a, n)
    for rho,c in [ (1.0, vector(0.8,0,0)), (-1.0, vector(-0.8,0,0)) ]:
        for i,x in enumerate(P):
            for j,y in enumerate(P):
                for k,z in enumerate(P):
                    r = (vector(x,y,z) - c).mag
                    if r > 0.1:
                        F[i,j,k] += rho / r
    U = F[:,:,n/2]
    X,Y = np.meshgrid(P,P)
    plt.pcolor(X,Y,np.sqrt(U))
    plt.show()
    
                    
