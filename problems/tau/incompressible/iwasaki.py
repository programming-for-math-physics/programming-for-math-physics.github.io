#!/usr/bin/python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import time
import pdb

# 2次元で ハーゲン・ポアズイユ流をシミュレート
# 
#            ux = 0
#   +----------------------+
# ---->
# ---->
# ---->
# ---->
#   +----------------------+
#            ux = 0

def partial_by_x(f):
    """
    f : scalar field (m x n array)
    returns : ∂f/∂x  ((m - 1) x n array)
    """
    m,n = f.shape
    p = f[1:,:] - f[:-1,:]
    assert(p.shape == (m - 1, n)), (p.shape, (m - 1, n))
    return p

def partial_by_y(f):
    """
    f : scalar field (m x n array)
    returns : ∂f/∂y  (m x (n - 1) array)
    """
    m,n = f.shape
    p = f[:,1:] - f[:,:-1]
    assert(p.shape == (m, n - 1)), (p.shape, (m, n - 1))
    return p

def grad_f(f):
    """
    f : scalar field (m x n array)
    returns : (∂f/∂x, ∂f/∂y)  (2 x (m - 1) x (n - 1) array)
    """
    m,n = f.shape
    gx = partial_by_x(f)
    gy = partial_by_y(f)
    r =  np.vstack([ gx[:,1:], gy[1:,:] ]).reshape((2, m - 1, n - 1))
    return r

def u_dot_grad_f(u, f):
    """
    u : vector field (2 x m x n)
    f : scalar field (m x n)
    compute (u・∇) f = (u0 ∂/∂x + u1 ∂/∂y) f
    """
    d,m,n = u.shape
    assert(d == 2), d
    assert(f.shape == (m, n)), (f.shape, (m, n))
    g = u[0,1:,1:] * partial_by_x(f[:,1:]) + u[1,1:,1:] * partial_by_y(f[1:,:])
    assert(g.shape == (m - 1, n - 1)), (g.shape, (m - 1, n - 1))
    return g

# v : vector field
# compute (u・∇) v
def u_dot_grad_v(u, v):
    """
    u : vector field (2 x m x n)
    v : vector field (2 x m x n)
    compute (u・∇) v = ((u0 ∂/∂x + u1 ∂/∂y) v0, (u0 ∂/∂x + u1 ∂/∂y) v1)
    """
    d,m,n = v.shape
    assert(d == 2), d
    assert(u.shape == (d,m,n)), (u.shape, (d,m,n))
    gx = u_dot_grad_f(u, v[0,:,:])
    gy = u_dot_grad_f(u, v[1,:,:])
    assert(gx.shape == (m - 1, n - 1)), (gx.shape, (m - 1, n - 1))
    assert(gy.shape == (m - 1, n - 1)), (gy.shape, (m - 1, n - 1))
    r =  np.vstack([ gx, gy ]).reshape((2, m - 1, n - 1))
    return r

def div(v):
    """
    v : vector field (2 x m x n)
    compute ∇・v =  ∂v0/∂x + ∂v1/∂y
    """
    d,m,n = v.shape
    g = partial_by_x(v[0,:,1:]) + partial_by_y(v[1,1:,:])
    assert(g.shape == (m - 1, n - 1)), (g.shape, (m - 1, n - 1))
    return g

def laplace_f(f):
    """
    f : scalar field (m x n)
    returns : Δf =  ∂^2f/∂x^2 + ∂^2f/∂y^2  ((m - 1) x (n - 1))
    """
    m,n = f.shape
    l = f[:-2,1:-1] + f[2:,1:-1] + f[1:-1,:-2] + f[1:-1,2:] - 4 * f[1:-1,1:-1]
    assert(l.shape == (m - 2, n - 2)), (l.shape, (m - 2, n - 2))
    return l

def laplace_v(v):
    """
    v : vector field (2 x m x n)
    returns : Δv =  (∂^2v0/∂x^2 + ∂^2v0/∂y^2,
                      ∂^2v1/∂x^2 + ∂^2v1/∂y^2)
              (2 x (m - 1) x (n - 1))
    """
    d,m,n = v.shape
    assert(d == 2), d
    lx = laplace_f(v[0,:,:])
    ly = laplace_f(v[1,:,:])
    assert(lx.shape == (m - 2, n - 2)), (lx.shape, (m - 2, n - 2))
    assert(ly.shape == (m - 2, n - 2)), (ly.shape, (m - 2, n - 2))
    l = np.vstack([ lx, ly ]).reshape((d, m - 2, n - 2))
    return l

def solve_poisson(p, f):
    """
    f : scalar field (m x n)
    solve Δp = f
    """
    m,n = f.shape
    N = m * n

    """
    make matrix A for (m x n) region ((m * n) x (m * n) matrix).
    pressure values pointing to outside of [1:-1,1:-1] are subtracted from f;
    f = A p + c
    => f - c = A p
    """
    D = {}
    for i in range(m):
        for j in range(n):
            D[i,j,i,j] = -4
            if i + 1 < m:
                D[i,j,i+1,j] = 1
            else:
                f[i, j] -= p[-1, j+1]
            if i > 0:
                D[i,j,i-1,j] = 1
            else:
                f[i, j] -= p[0, j+1]
            if j + 1 < n:
                D[i,j,i,j+1] = 1
            else:
                f[i, j] -= p[i+1, -1]
            if j > 0:
                D[i,j,i,j-1] = 1
            else:
                f[i, j] -= p[i+1, 0]
    I = {}
    for i in range(m):
        for j in range(n):
            I[i,j] = len(I)
    A = scipy.sparse.dok_matrix((N, N))
    for (i,j,ii,jj),v in D.items():
        A[I[i,j],I[ii,jj]] = v

    A = scipy.sparse.csr_matrix(A)

    p[1:-1,1:-1] = scipy.sparse.linalg.spsolve(A, f.reshape(N)).reshape((m, n))
    # assign pressure values on both walls (assuming Neumann condition)
    p[:,0] = p[:,1]
    p[:,-1] = p[:,-2]

def step(u, p, dt):
    """
    calc 1 step.
    u : velocity field (vector field) 2 x m x n
    p : pressure field (scalar field) m x n
    """
    d,m,n = u.shape
    assert(d == 2), d
    assert(p.shape == (m,n)), (p.shape, (m, n))
    c = 1                       # 1/Re  (Re : Reynolds constant)
    # calc righthand side of the poission equation
    # (u・∇)u
    vgu = u_dot_grad_v(u, u)
    assert(vgu.shape == (d, m - 1, n - 1)), (vgu.shape, (d, m - 1, n - 1))
    # - ∇・(u・∇)u
    div_vgu = - div(vgu)
    assert(div_vgu.shape == (m - 2, n - 2)), (div_vgu.shape, (m - 2, n - 2))
    # solve Δp = - ∇・(u・∇)u
    solve_poisson(p, div_vgu)
    # ∇p
    gp = grad_f(p)
    assert(gp.shape == (d, m - 1, n - 1)), (gp.shape, (d, m - 1, n - 1))
    # - (u・∇)u - ∇p + c Δu
    dudt = - vgu[:,1:,1:] - gp[:,1:,1:] + c * laplace_v(u)
    assert(dudt.shape == (d, m - 2, n - 2)), (dudt.shape, (d, m - 2, n - 2))
    u[:,1:-1,1:-1] += dudt * dt
    # impose periodic boundary condition on both sides
    u[:,0,:] = u[:,-2,:]
    u[:,-1,:] = u[:,1,:]

def simulate():
    d = 2                       # dimension (2)
    m = 40                      # x-axis
    n = 20                      # y-axis
    dt = 0.01
    u = np.zeros((d, m, n))
    p = np.zeros((m, n))
    p[0,:] = 0.0                # boundary 
    p[-1,:] = -1.0              # boundary 
    n_steps = 100000
    # fig = plt.figure()
    for i in range(n_steps):
        if i % 200 == 0:
            print("step %d" % i)
            print("p")
            print(p)
            print("u[0]")
            print(u[0])
            if i == 0:
                field = plt.imshow(u[0], vmin = 0, vmax = 1.5)
                fig = plt.gcf()
                #plt.clim()   # clamp the color limits
                plt.colorbar()
            else:
                #field.set_array(shrink(u[0]))
                field.set_data(u[0])
            plt.pause(0.01)
        step(u, p, dt)

def main():
    return simulate()

ani = main()
