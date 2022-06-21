
import cmath, math

def proot(n):
    a = math.cos(2.0 * math.pi / n)
    b = math.sin(2.0 * math.pi / n)
    return a + b * 1.0j

x = proot(5)
print x * x * x * x * x
