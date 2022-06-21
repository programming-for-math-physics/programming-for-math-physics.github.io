import math
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d
import colorsys
from visual import *

def f(x, y):
    return x * x + 2 * x * y + 3 * y * y + 4 * x + 5 * y

def g(x, y):
    return (x + y + 2) ** 2 + 2 * (y + 1/4.0) ** 2 - 33/8.0

#   (x + y)^2 + 2y^2 + 4(x + y) + y
# = (x + y + 2)^2 - 4 + 2(y + 1/4)^2 - 1/8
# = (x + y + 2)^2 + 2(y + 1/4)^2 - 33/8
# x = -7/4, y = -1/4

def make_color(i, n):
    return colorsys.hsv_to_rgb(i/float(n), 1.0, 1.0)

def balls():
    n = 10
    scene.autocenter = 0
    scene.autoscale = 0
    scene.range = vector(n,n,n)
    #scene.forward = vector(0,0,-1)
    #scene.center = vector(0,0,0)
    #scene.fov = 1.0
    for i in range(n):
        rate(10)
        sphere(pos=vector(i,i,i), color=make_color(i, n))
    for i in range(100):
        rate(1)
        print scene.center, scene.forward, scene.range, scene.scale, scene.fov

def make_ball_color(pos):
    if pos.z > 0.0:
        z = 0.0
    else:
        z = pos.z
    return colorsys.hsv_to_rgb(-z/18.44, 1.0, 1.0)

def ball():
    g = vector(0.0,-9.8,0.0)
    dt = 0.001
    pitcher_pos = vector(0,    1.5, -18.44)
    mitt_pos    = vector(0,    0.5,   1.5)
    eye_pos     = vector(-1.0, 1.5,   0.0)
    scene.autocenter = 0
    scene.autoscale = 0
    scene.center = pitcher_pos
    scene.forward = pitcher_pos - eye_pos
    init_vel = (mitt_pos - pitcher_pos).proj(vector(0,0,1))
    init_vel /= init_vel.mag
    init_vel *= 150*1000.0/3600.0 
    ball_radius = 0.08
    ball = sphere(pos=pitcher_pos, vel=init_vel, radius=ball_radius)
    mitt = sphere(pos=mitt_pos, radius=ball_radius)
    eye = sphere(pos=eye_pos, radius=ball_radius)
    board = box(pos=((pitcher_pos+mitt_pos)*0.5).proj(vector(0,0,1)), 
                width = (pitcher_pos - mitt_pos).mag,
                length = 1.0, height = 0.01)
    while 1:
        rate(10)
        if scene.mouse.clicked:
            break
    mitt.visible = 0
    t = 0.0
    for i in range(2000):
        rate(1.0/dt)
        # ball.vel += g * dt
        # ball.pos += b.vel * dt
        new_pos = ball.pos + ball.vel * dt
        if new_pos.z > 0.0: break
        if 0:
            ball = sphere(pos=new_pos, vel=ball.vel + g * dt, 
                          radius=ball_radius, 
                          color=make_ball_color(new_pos))
        else:
            ball.pos = new_pos
            ball.vel += g * dt
        t += dt


def parabolic(thetas):
    g = vector(0.0,-9.8,0.0)
    v0 = 10.0
    dt = 0.01
    #scene.autoscale
    scene.autoscale = 0
    scene.center = (5.0, 5.0, 0.0)
    scene.width = 1000
    scene.height = 1000
    scene.background = color.gray(0.7)
    #scene.autocenter = 0
    P = [ sphere(pos=vector(0.0, 0.0, 0.0), 
                 radius=0.3,
                 retain=50, trail_type="points",
                 color=make_color(i, len(thetas)),
                 vel=vector(v0 * math.cos(t), v0 * math.sin(t), 0.0))
          for i,t in enumerate(thetas) ]
    C = [ curve(pos=[p.pos], color=make_color(i, len(P))) for i,p in enumerate(P) ]
    arrow(pos=(0.0,0.0,0.0), axis=(1.0,0.0,0.0))
    arrow(pos=(0.0,0.0,0.0), axis=(0.0,1.0,0.0))
    for i in range(1000):
        rate(30)
        for p,c in zip(P,C):
            if p.pos.y >= 0.0:
                a = g #  - 0.3 * p.vel
                p.vel += a * dt
                p.pos += p.vel * dt
            c.append(p.pos)

# 
# 
# 

def find_poly(XY):
    n = len(XY)
    A = np.zeros((n,n))
    b = np.zeros((n,1))
    for i,(x,y) in enumerate(XY):
        for j in range(n):
            A[i,j] = x ** j
        b[i] = y
    print A
    a = np.linalg.solve(A, b)
    return a

def find_poly_and_plot():
    # X = sorted(np.random.random(4))
    # Y = [ 0, 1, 0, 1 ]
    XY = np.random.random((4,2))
    a = find_poly(XY)
    print a
    def f(x):
        s = 0.0
        for i,ai in enumerate(a):
            s += ai * x ** i
        return s
    X = np.linspace(0.0,1.0,1000)
    Y = f(X)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-3,3)
    ax.plot(X, Y)
    ax.plot(XY[:,0], XY[:,1], '*')
    fig.show()

def minimize(f, x0, x1, y0, y1):
    m = (float("inf"), None, None)
    for x in np.linspace(x0,x1,1000):
        for y in np.linspace(y0,y1,1000):
            m = min(m, (f(x,y), x, y))
    return m

def minimize2(f, x0, y0):
    x,y = x0, y0
    h = 1.0e-1
    h_min = 1.0e-20
    while 1:
        dfdx,dfdy = ((f(x+h,y)-f(x,y))/h, (f(x,y+h)-f(x,y))/h)
        d = math.sqrt(dfdx * dfdx + dfdy * dfdy)
        if d < 1.0e-300:
            if h < h_min:
                break
            else:
                h = h * 0.5
        else:
            x_ = x - h * dfdx / d
            y_ = y - h * dfdy / d
            if f(x_,y_) < f(x,y):
                x = x_
                y = y_
            elif h < h_min:
                break
            else:
                h = h * 0.5
    return f(x,y),x,y

def minimize3(f, x0, y0):
    return scipy.optimize.minimize(lambda (x,y): f(x,y), (x0,y0))

def plot2(f, x0, x1, y0, y1):
    X = np.linspace(x0, x1, 50)
    Y = np.linspace(y0, y1, 50)
    X,Y = np.meshgrid(X, Y)
    fig = plt.figure()
    p = fig.add_subplot(221, projection='3d').plot_surface(X, Y, f(X, Y))
    p = fig.add_subplot(222, projection='3d').plot_wireframe(X, Y, f(X, Y))
    p = fig.add_subplot(223).contour(X, Y, f(X, Y), levels=np.arange(0,100,1))
    ax = fig.add_subplot(224)
    p = ax.pcolor(X, Y, f(X, Y))
    fig.colorbar(p)
    fig.show()


def plot_2d_array(A):
    M,N = A.shape
    X = np.linspace(0.0, 1.0, M)
    Y = np.linspace(0.0, 1.0, N)
    X,Y = np.meshgrid(X, Y)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    p = ax.pcolor(X, Y, A)
    fig.colorbar(p)
    fig.show()

#
# f(x+dx,y) - f(x,y)
# ------------------
#         h
#
# f(x+dx,y) - f(x,y)    f(x,y) - f(x-dx,y)
# ------------------ - -------------------
#         h                      h
#------------------------------------------
#                    h
# f(x+dx,y) - 2f(x,y) + f(x-dx,y)
# ------------------------------- = 0
#               h^2
#
# f(x+dx,y) + f(x-dx,y) + f(x,y+dy) + f(x,y-dy) - 4f(x,y)  
# --------------------------------------------------------- = 0
#                          h^2
#

def laplace(n, f):
    A = np.zeros((n,n,n,n))
    b = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            A[i,j,i,j] = -4.0
            if i > 0:
                A[i,j,i-1,j] = 1.0
            if i < n - 1:
                A[i,j,i+1,j] = 1.0
            if j > 0:
                A[i,j,i,j-1] = 1.0
            if j < n - 1:
                A[i,j,i,j+1] = 1.0
    # print A
    for j in range(n):
        b[0,  j] = -f(0.0,  j/float(n)) * 1.0/float(n * n)
        b[n-1,j] = -f(1.0,  j/float(n)) * 1.0/float(n * n)
    for i in range(n):
        b[i,0]   = -f(i/float(n),  0.0) * 1.0/float(n * n)
        b[i,n-1] = -f(j/float(n),  1.0) * 1.0/float(n * n)
    # print b
    b = b.reshape(n * n, 1)
    A = A.reshape(n * n, n * n)
    A = scipy.sparse.csr_matrix(A)
    print A.data
    # x = np.linalg.solve(A, b.reshape(n * n, 1))
    x = scipy.sparse.linalg.spsolve(A, b)
    plot_2d_array(x.reshape(n, n))


def boundary_condition(x, y):
    if x == 0.0 or y == 0.0:
        return 1 - x - y
    else:
        return 0.0

def main():
    #parabolic(np.linspace(0,math.pi/2.0,10))
    find_poly_and_plot()
    #laplace(100, boundary_condition)
    # return plot2(f, -10.0, 10.0, -10.0, 10.0)
    # return minimize3(f, 0, 0)
    # return minimize(f, -10, 10, -10, 10)
    #ball()


print "OK"
