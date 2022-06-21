import math
from matplotlib.pyplot import plot,show
import visual

def integrate(x0, x1, y0, f, dx):
    x = x0
    y = y0
    visual.sphere(pos=(x0, y0, 0), radius=10*dx, color=visual.color.yellow)
    visual.sphere(pos=(x1, math.sqrt(2*x1-1), 0), radius=10*dx, color=visual.color.blue)
    visual.arrow(pos=(0,0,0), axis=(1,0,0), shaftwidth=0.05)
    visual.arrow(pos=(0,0,0), axis=(0,1,0), shaftwidth=0.05, color=visual.color.yellow)
    while x < x1:
        visual.rate(300)
        visual.sphere(pos=(x, y, 0), radius=dx)
        dy_dx = f(x, y)
        x += dx
        y += dy_dx * dx


#
# y(1) = 1
# dy/dx = 1 / y
#

def mintegrate(x0, x1, y0, f, dx):
    x = x0
    y = y0
    X = []
    Y = []
    while x < x1:
        dy_dx = f(x, y)
        x += dx
        y += dy_dx * dx
        X.append(x)
        Y.append(y)
    plot(X, Y)
    show()

def f(x, y):
    return 1.0 / y

print "OK"

integrate(1, 5, 1, f, 0.01)
