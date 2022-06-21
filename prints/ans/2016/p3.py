import math

def a(c, n):
    x = c
    for i in range(n):
        x = (2 * x + c / (x * x)) / 3.0
    return x

a(5, 100000) ** 3

def integrate(f, a, b, n):
    s = 0.0
    dx = (b - a) / n
    x = a
    for i in range(n):
        s = s + f(x + 0.5 * dx) * dx
        x = x + dx
    return s

def circ(x):
    return math.sqrt(1.0 - x * x)

integrate(circ, 0.0, 1.0, 1000000)

def acute_abc(a, b, c):
    if a + b <= c:
        return 0
    if a + c <= b:
        return 0
    if b + c <= a:
        return 0
    if a*a + b*b > c*c:
        return 1
    if a*a + c*c > b*b:
        return 1
    if b*b + c*c > a*a:
        return 1
    return 0

def acute_z(z):
    a = (z - 1).mag
    b = (z*z - 1).mag
    c = (z*z - z).mag
    return acute_abc(z)

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


def min_S():
    n = 100000
    m = 1
    for i in range(2, n):
        x = 1 + 2.0 * i / float(n)
        y = 1 + 2.0 * m / float(n)
        if S(x) < S(y):
            m = i
    return 1 + 2.0 * m / float(n)
    
def newton(f, c, eps):
    def deriv_f(x):
        h = 1.0e-7
        return (f(x+h) - f(x)) / h
    a = c
    for i in range(100000):
        a = a - f(a) / deriv_f(a)
    return a

def poly(x):
    return (x - 2) * (x - 3) * (x - 4)


    
