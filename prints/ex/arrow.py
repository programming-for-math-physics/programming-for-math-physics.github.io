from visual import *

def show_comp(z):
    arrow(pos=(0,0,0),axis=(z.real,z.imag,0),
          shaftwidth=0.01)

def show_prod(x):
    show_comp(x)
    show_comp(x * x)
    show_comp(x * x * x)
    show_comp(x * x * x * x)

show_prod(1.0+1.0j)

