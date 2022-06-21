from visual import *

def axes():
    x = arrow(axis=(1,0,0), color=color.red)
    y = arrow(axis=(0,1,0), color=color.blue)
    z = arrow(axis=(0,0,1), color=color.yellow)

from visual import *

def mass_spring():
    h = 10
    r = 0.5
    b = sphere()
    s = helix(pos=(0,h,0), axis=(0,-h,0), radius=r, thickness=r/4.0)
    ceil = box(pos=(0,h,0), length=10, height=0.1, width=10)
    
from visual import *

def methane():
    a = 10.0
    H1 = vector(0,a,a)
    H2 = vector(a,0,a)
    H3 = vector(a,a,0)
    H4 = vector(0,0,0)
    C  = vector(a/2,a/2,a/2)
    r = 0.3
    sphere(pos=H1)
    sphere(pos=H2)
    sphere(pos=H3)
    sphere(pos=H4)
    sphere(pos=C)
    cylinder(pos=C, axis=H1-C, radius=r)
    cylinder(pos=C, axis=H2-C, radius=r)
    cylinder(pos=C, axis=H3-C, radius=r)
    cylinder(pos=C, axis=H4-C, radius=r)

def methane():
    a = 10.0
    H1 = vector(0,a,a)
    H2 = vector(a,0,a)
    H3 = vector(a,a,0)
    H4 = vector(0,0,0)
    C  = vector(a/2,a/2,a/2)
    r = 0.3
    for p in [ H1, H2, H3, H4, C ]:
        sphere(pos=p)
    for p in [ H1, H2, H3, H4 ]:
        cylinder(pos=C, axis=p-C, radius=r)


    
def area(A, B, C):
    b = B - A
    c = C - A
    return 0.5 * math.sqrt(b.dot(b) * c.dot(c) - (b.dot(c))**2)

def intersect_xy(A, B):
    b = B - A
    t = - A.z / b.z
    return A + b * t

def S(a):
    P1 = vector(1,0,1)
    P2 = vector(1,1,1)
    P3 = vector(1,0,3)
    Q = vector(0,0,a)
    R1 = intersect_xy(P1, Q)
    R2 = intersect_xy(P2, Q)
    R3 = intersect_xy(P3, Q)
    return area(R1, R2, R3)


    
    
    
    
