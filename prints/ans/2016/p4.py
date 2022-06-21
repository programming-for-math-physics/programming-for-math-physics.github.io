
def ode_solve(f, a, b, c):
    x = a
    y = c
    n = 1000000
    h = (b - a) / n
    for i in range(n):
        y = y + f(x, y) * h
        x = x + h
    return y

def f(x, y):
    return 1.0 / y

ode_solve(f, 1.0, 2.5, 1.0)
ode_solve(f, 1.0, 5.0, 1.0)
