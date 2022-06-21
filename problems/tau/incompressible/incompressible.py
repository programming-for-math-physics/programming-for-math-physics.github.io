#!/usr/bin/python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import time,sys
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

def partial_by_x_periodic(f, h):
    """
    f : scalar field (m x n array). periodic along x axis
    returns : ∂f/∂x  ((m - 1) x n array)
    """
    return (np.roll(f, -1, axis=0) - f) / h

def partial_by_y_periodic(f, h):
    """
    f : scalar field (m x n array). periodic along y axis
    returns : ∂f/∂y  (m x (n - 1) array)
    """
    return (np.roll(f, -1, axis=1) - f) / h

def grad_f_periodic(f, h):
    """
    f : scalar field (m x n array). periodic along both axes
    returns : (∂f/∂x, ∂f/∂y)  (2 x (m - 1) x (n - 1) array)
    """
    m,n = f.shape
    gx = partial_by_x_periodic(f, h)
    gy = partial_by_y_periodic(f, h)
    return np.vstack([ gx, gy ]).reshape((2, m, n))

def u_dot_grad_f_periodic(u, f, h):
    """
    u : vector field (2 x m x n)
    f : scalar field (m x n). periodic along both dimensions
    compute (u・∇) f = (u0 ∂/∂x + u1 ∂/∂y) f
    """
    d,m,n = u.shape
    assert(d == 2), d
    assert(f.shape == (m, n)), (f.shape, (m, n))
    g = (u[0,:,:] * partial_by_x_periodic(f, h)
         + u[1,:,:] * partial_by_y_periodic(f, h))
    assert(g.shape == (m, n)), (g.shape, (m, n))
    return g

# v : vector field
# compute (u・∇) v
def u_dot_grad_v_periodic(u, v, h):
    """
    u : vector field (2 x m x n)
    v : vector field (2 x m x n)
    compute (u・∇) v = ((u0 ∂/∂x + u1 ∂/∂y) v0, (u0 ∂/∂x + u1 ∂/∂y) v1)
    """
    d,m,n = v.shape
    assert(d == 2), d
    assert(u.shape == (d,m,n)), (u.shape, (d,m,n))
    gx = u_dot_grad_f_periodic(u, v[0,:,:], h)
    gy = u_dot_grad_f_periodic(u, v[1,:,:], h)
    assert(gx.shape == (m, n)), (gx.shape, (m, n))
    assert(gy.shape == (m, n)), (gy.shape, (m, n))
    r =  np.vstack([ gx, gy ]).reshape((2, m, n))
    return r

def div_periodic(v, h):
    """
    v : vector field (2 x m x n). both components periodic along both axes
    compute ∇・v =  ∂v0/∂x + ∂v1/∂y
    """
    d,m,n = v.shape
    g = (partial_by_x_periodic(v[0,:,:], h)
         + partial_by_y_periodic(v[1,:,:], h))
    assert(g.shape == (m, n)), (g.shape, (m, n))
    return g

def laplace_f_periodic(f, h):
    """
    f : scalar field (m x n)
    returns : Δf =  ∂^2f/∂x^2 + ∂^2f/∂y^2  ((m - 1) x (n - 1))
    """
    m,n = f.shape
    l = (np.roll(f, 1, axis=0)
         + np.roll(f, 1, axis=1)
         + np.roll(f, -1, axis=0)
         + np.roll(f, -1, axis=1)
         - 4 * f) / (h*h)
    assert(l.shape == (m, n)), (l.shape, (m, n))
    return l

def laplace_v_periodic(v, h):
    """
    v : vector field (2 x m x n)
    returns : Δv =  (∂^2v0/∂x^2 + ∂^2v0/∂y^2,
                      ∂^2v1/∂x^2 + ∂^2v1/∂y^2)
              (2 x (m - 1) x (n - 1))
    """
    d,m,n = v.shape
    assert(d == 2), d
    lx = laplace_f_periodic(v[0,:,:], h)
    ly = laplace_f_periodic(v[1,:,:], h)
    assert(lx.shape == (m, n)), (lx.shape, (m, n))
    assert(ly.shape == (m, n)), (ly.shape, (m, n))
    l = np.vstack([ lx, ly ]).reshape((d, m, n))
    return l

def solve_pressure(p, f, h):
    """
    f : scalar field (m x n)
    solve Δp = f
    """
    m,n = f.shape
    N = (m - 2) * (n - 2)

    """
    make matrix A for (m x n) region ((m * n) x (m * n) matrix).
    pressure values pointing to outside of [1:-1,1:-1] are subtracted from f;
    f = A p + c
    => f - c = A p
    """
    D = {}
    # f [0..m-1] x [0..n-1]
    # p [1..m-2] x [1..n-2]
    f = h * h * f
    for i in range(1, m-1):
        for j in range(1, n-1):
            # (p[i+1,j]+p[i,j+1]+p[i-1,j]+p[i,j-1]-4p[i,j]) = h*h*f[i,j]
            D[i,j,i,j] = -4
            if i + 1 < m - 1:
                D[i,j,i+1,j] = 1
            else:
                f[i, j] -= p[i+1, j]
            if i > 1:
                D[i,j,i-1,j] = 1
            else:
                f[i, j] -= p[i-1, j]
            if j + 1 < n - 1:
                D[i,j,i,j+1] = 1
            else:
                D[i,j,i,j] += 1
                # f[i, j] -= p[i, j+1]
            if j > 1:
                D[i,j,i,j-1] = 1
            else:
                D[i,j,i,j] += 1
                #f[i, j] -= p[i, j-1]
    I = {}
    for i in range(1, m-1):
        for j in range(1, n-1):
            I[i,j] = len(I)
    A = scipy.sparse.dok_matrix((N, N))
    for (i,j,ii,jj),v in D.items():
        A[I[i,j],I[ii,jj]] = v
    A = scipy.sparse.csr_matrix(A)
    p[1:-1,1:-1] = scipy.sparse.linalg.spsolve(A, f[1:-1,1:-1].reshape(N)).reshape((m-2, n-2))
    # assign pressure values on both walls (assuming Neumann condition)
    p[1:-1,0] = p[1:-1,1]
    p[1:-1,-1] = p[1:-1,-2]

def make_gp(m, n, h):
    dpx = np.array([ -1 / (h * m) ] * (m * n)).reshape((m, n))
    dpy = np.zeros((m, n))
    return np.vstack([ dpx, dpy ]).reshape((2, m, n))

def step(u, p, dt, h):
    """
    calc 1 step.
    u : velocity field (vector field) 2 x m x n
    p : pressure field (scalar field) m x n
    """
    d,m,n = u.shape
    assert(d == 2), d
    assert(p.shape == (m,n)), (p.shape, (m, n))
    Re = 1
    # calc righthand side of the poission equation
    # (u・∇)u
    ugu = u_dot_grad_v_periodic(u, u, h)
    assert(ugu.shape == (d, m, n)), (ugu.shape, (d, m, n))
    # - ∇・(u・∇)u
    div_ugu = - div_periodic(ugu, h)
    assert(div_ugu.shape == (m, n)), (div_ugu.shape, (m, n))
    # solve Δp = - ∇・(u・∇)u
    solve_pressure(p, div_ugu, h)
    # ∇p
    gp = grad_f_periodic(p, h)
    #gp = make_gp(m, n, h)
    assert(gp.shape == (d, m, n)), (gp.shape, (d, m, n))
    lap = laplace_v_periodic(u, h)
    # - (u・∇)u - ∇p + c Δu
    dudt = - ugu - gp + (1/Re) * lap
    assert(dudt.shape == (d, m, n)), (dudt.shape, (d, m, n))
    #pdb.set_trace()
    u[:,:,1:-1] += dudt[:,:,1:-1] * dt
    return (ugu, gp, lap, dudt)

def make_quiver(ax, f, h):
    """
    f : scalar field
    """
    d,m,n = f.shape
    x = np.arange(m) * h
    y = np.arange(n) * h
    x,y = np.meshgrid(x, y, indexing='ij')
    return ax.quiver(x, y, f[0], f[1], scale_units="dots", scale=0.01)

def set_data_quiver(qv, ax, f, h):
    qv.set_UVC(f[0], f[1], None)

def make_plot(ax, f, h):
    """
    f : scalar field
    """
    n, = f.shape
    y = np.arange(n) * h
    [ p ] = ax.plot(y, f)
    return p

def set_data_plot(pl, ax, f, h):
    n, = f.shape
    y = np.arange(n) * h
    pl.set_data(y, f)
    # ax.set_ylim((f.min(), f.max() * 1.5))

def make_pcolor(ax, f, h):
    """
    f : scalar field
    """
    m,n = f.shape
    x = np.arange(m) * h
    y = np.arange(n) * h
    x,y = np.meshgrid(x, y, indexing='ij')
    pc = ax.pcolor(x, y, f, vmin=0.0, vmax=1.5)
    return pc

def set_data_pcolor(pc, ax, f, h):
    m,n = f.shape
    pc.set_array(f[:m-1,:n-1].flatten())

def make_imshow(ax, f, h):
    """
    f : scalar field
    """
    im = ax.imshow(f, vmin=0.0, vmax=0.5)
    return im

def do_animation(iterator, **kwargs):
    def anime_fun(*args):
        try:
            return next(iterator)
        except StopIteration:
            return []
    ani = animation.FuncAnimation(plt.gcf(),
                                  anime_fun, **kwargs)
    plt.show()
    return ani

def show_dot():
    sys.stdout.write(".")
    sys.stdout.flush()

def simulate():
    d = 2                       # dimension (2)
    m = 40                     # x-axis 200
    n = 20                      # y-axis 50
    dt = 0.0001
    h = 1.0 / n
    u = np.zeros((d, m, n))
    p = np.zeros((m, n))
    p[0,:] = 1.0
    p[-1,:] = 0.0
    n_steps = 1000
    n_figs = 1
    figs = [ plt.figure() for _ in range(n_figs) ]
    axs = [ fig.add_subplot(1, 1, 1) for fig in figs ]
    # [ ax_u, ax_ux, ax_p ] = axs
    [ ax_ux ] = axs
    ax_ux.set_ylim((0, 0.03))
    for i in range(n_steps):
        ugu,gp,lap,dudt = step(u, p, dt, h)
        if i == 0:
            #vis_u = make_quiver(ax_u, u, h)
            #vis_p = make_pcolor(ax_p, p, h)
            vis_ux = make_plot(ax_ux, u[0,0,:], h)
        else:
            #set_data_quiver(vis_u, ax_u, u, h)
            #set_data_pcolor(vis_p, ax_p, p, h)
            set_data_plot(vis_ux, ax_ux, u[0,5,:], h)
        plt.pause(0.1)
        
def main():
    # return simulate1()
    # return do_animation(simulate2(), interval=100)
    return simulate()

main()
