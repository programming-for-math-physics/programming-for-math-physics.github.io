import math

def inner(a, b, c, d):
    return a * c + b * d

def solve_q(a, b, c):
    D = b * b - 4 * a * c
    return (-b + math.sqrt(D)) / (2.0 * a)

def check_q(a, b, c):
    x = solve_q(a, b, c)
    y = a * x * x + b * x + c
    return abs(y) < 1.0e-5

def dist_lp(a, b, c, p, q):
    s = a * p + b * q + c
    t = math.sqrt(a * a + b * b)
    return s / t


def f(x):
    return math.e - (1 + 1.0/x) ** x

def g(x):
    return (1 + 1.0/x) ** (x + 0.5) - math.e

def h(a):
    dx = 1.0e-9
    return (math.log(a + dx) - math.log(a)) / dx

def deriv(f, a):
    dx = 1.0e-9
    return (f(a + dx) - f(a)) / dx

def proot(n):
    theta = 2.0 * math.pi / n
    return math.cos(theta) + 1.0j * math.sin(theta)

def check_proot(n):
    z = proot(n)
    return abs(z ** n - 1.0)

