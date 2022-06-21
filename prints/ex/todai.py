def p(n):
    a = 1.0
    b = 2.0
    for i in range(n):
        c = (b * b + 1) / a
        a = b
        b = c
    return a

def x(n):
    a = p(n+1)
    b = p(n)
    return (a*a + b*b + 1) / (a * b)


