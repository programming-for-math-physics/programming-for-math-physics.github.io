#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math,random
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time

#
# solve time-independent shrodinger equation:
#
# (-h'^2/2m △ + V(x)) f = E f
#
# where V(x) = -e * e/(4.0 * pi * epsilon |x|)
#
# h' = h/(2 pi) (h is a plank constant)
# m  = mass of electron
# e  = charge of ploton
# epsilon = permittivity of vacuum
#

# (△ - 2m/h_^2 V(x)) f = E f

# (△ + m e^2/(2h_^2 * pi * epsilon |x|)) f = E f
#  

if 0:
    eps =  8.854187817e-12
    m   =  9.10938291e-31
    e   = -1.602176565e-19
    h   =  6.62606957e-34
    h_  =  h / (2.0 * math.pi)
    r   =  5.3e-11
else:
    eps =  1.0
    m   =  1.0
    e   = -1.0e10
    h   =  1.0
    h_  =  h / (2.0 * math.pi)
    r   =  1.0

print(m * e * e / (2 * math.pi * eps * h_ * h_ * r))

#
# make the lefthand side matrix of
# 
# ((-h_**2 /(2.0 * m)) △ - e**2 /(4.0 * pi * eps) * 1.0/|x|) f = E f
#
# in space [-a,a] x [-a,a] x [-a,a],
# with a mesh of n x n x n interim points 
# (i.e., dx = (2a)/(n+1))
#

def make_lhs_matrix_3d(n, a):
    # 3D laplacian matrix
    L = scipy.sparse.diags([-6.0,  1.0,  1.0,   1.0,  1.0,  1.0,  1.0 ], 
                           [   0,     1,   -1,    n,   -n,  n*n, -n*n ], 
                           shape=(n**3, n**3))
    # D = matrix representing the potential 
    l = np.linspace(-a, a, n+2)[1:-1]
    x,y,z = np.meshgrid(l, l, l)
    V = 1.0 / np.sqrt(x*x+y*y+z*z)
    D = scipy.sparse.diags([ V.flatten() ], [ 0 ])
    dx = (2.0 * a) / (n + 1)
    a = -h_ * h_ / (2.0 * m * dx * dx)
    b = -e * e / (4.0 * math.pi * eps)
    # here, the "true" matrix is a * L + b * D, but
    # to maintain human-readability of the matrix,
    # we divide it by (-a).
    # we return the triple (scale, potential, matrix)
    H_ = -L - (b/a) * D
    return -a,V,H_

def visualize_3d(a, V, E, phis):
    """
    visialize the result
     a : half of the side length of the cube in which 
         we simulated. that is, we calculated solutions 
         in the domain [-a,a]^3
     V : the n x n x n 3D array describing the potential 
         in the above domain. n is the number of points
         along each axis.
     E : a 1D array describing eigenvalues we obtained
     phis : a (n**3) x nf 2D array describing eigenfunctions 
         we obtained. n is the number of points
         along each axis and nf the number of eigenvalues
         we obtained.
    
    this function shows them in a tile of graphs like this.
    
    
     +-----+-----+-----+-----+-----+---------+
     |  1  |  2  |  3  | ..  |     |nf+1     |
     |     |     |     |     |     |         |
     | V   |phi0 |phi1 |     |     |phi[nf-1]|
     |(2D) |(2D) |(2D) |     |     |(2D)     |
     +-----+-----+-----+-----+-----+---------+
     |nf+2 |nf+3 |nf+4 | ..  |     |2(nf+1)  |
     |     |     |     |     |     |         |
     | V   |phi0 |phi1 |     |     |phi[nf-1]|
     |(1D) |(1D) |(1D) |     |     |(1D)     |
     +-----+-----+-----+-----+-----+---------+
    """

    #
    # n  : number of lattice points
    # nf : the number of eigenvalues/functions we found
    print("Eigenvalues = %s" % E)
    n3,nf = phis.shape
    n = int(math.pow(n3+0.01, 1.0/3.0))
    assert(n ** 3 == n3), (n, n3)
    n_2 = n // 2
    l = np.linspace(-a, a, n+2)[1:-1]
    x,y = np.meshgrid(l,l)
    # number of rows/colums of the tile above
    row = 2
    col = nf + 1
    # really start working
    fig = plt.figure()
    # show V, both in 1D and 2D
    ax2d = fig.add_subplot(row,col,1)
    ax2d.set_title("potential (2D; z=0)")
    ax2d.pcolor(x, y, V[:,:,n_2])
    ax1d = fig.add_subplot(row,col,nf+2)
    ax1d.set_title("potential (1D; y=z=0)")
    ax1d.plot(l, V[:,n_2,n_2])
    # show nf eigenvalues/functions
    for k in range(nf):
        # extract k-th column of phis
        phi = phis[:,k].reshape(n,n,n)
        # show in 2D
        ax2 = fig.add_subplot(row,col,k+2)
        ax2.set_title("phi^2 (2D; E=%e)" % E[k])
        f = phi[:,:,n_2] * phi[:,:,n_2].conjugate()
        ax2.pcolor(x, y, f)
        # show in 1D
        ax1 = fig.add_subplot(row,col,k+nf+3)
        ax1.set_title("phi^2 (1D; E=%e)" % E[k])
        f = phi[:,n_2,n_2] * phi[:,n_2,n_2].conjugate()
        ax1.plot(l, f)
    plt.show()

def hydrogen(n):
    """
    solve shrodinger equation of a hydrogen
    atom (or a hydrogen-like ion that has
    only one electron) in a cube, using
    n x n x n lattice points.
    
    """
    # simulate in [-a,a]x[-a,a]x[-a,a]
    a = 4 * r
    # we get a trouble if n is odd, as an origin 
    # will be included in the lattice, at which 
    # the potential is infinite 
    if n % 2 != 0:
        sys.stderr.write("avoid using an odd n to avoid "
                         "zero division near the origin, "
                         "fixed it to %d\n" % (n + 1))
        n = n + 1
    # get H of Hx = Ex, along with potential V
    # for visualization purpose.
    # the returned H_ is actually a matrix such 
    # that scale * H_ is the real matrix.
    # so we need to scale returned eivenvalues
    scale,V,H_ = make_lhs_matrix_3d(n, a)
    # scale MUST BE > 0.0 so that finding
    # algebraically smallest eigenvalues returns
    # eigenvalues we want; otherwise we colud fix
    # that by finding largest ones, but do not bother
    assert(scale > 0.0)
    # error tolerance
    tol = 0
    t0 = time.time()
    # find algebraically smallest 6 eigenvalues of H
    # E,phis = scipy.sparse.linalg.eigsh(H_, k=10, which='SA', tol=tol)
    E,phis = scipy.sparse.linalg.eigsh(-H_, k=10, which='LA', tol=tol)
    t1 = time.time()
    print("%f sec" % (t1 - t0))
    visualize_3d(a, V, scale * E, phis)

hydrogen(50)
