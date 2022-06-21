from visual import *

def two_bodies(m0, x0, v0, m1, x1, v1):
    dt = 0.01
    xc = (m0 * x0 + m1 * x1) / (m0 + m1)
    vc = (m0 * v0 + m1 * v1) / (m0 + m1)
    b0 = sphere(radius=0.1, pos=x0 - xc, vel=v0 - vc, m=m0, color=color.red)
    b1 = sphere(radius=0.1, pos=x1 - xc, vel=v1 - vc, m=m1, color=color.blue)
    w0 = sphere(radius=b0.radius, pos=b0.pos)
    w1 = sphere(radius=b1.radius, pos=b1.pos)
    for i in range(3000):
        rate(int(1 / dt))
        dx = b0.pos - b1.pos
        b0.acc = - b0.m * dx / (dx.mag * dx.mag2)
        b1.acc =   b0.m * dx / (dx.mag * dx.mag2)
        b0.vel = b0.vel + b0.acc * dt
        b1.vel = b1.vel + b1.acc * dt
        b0.pos = b0.pos + b0.vel * dt
        b1.pos = b1.pos + b1.vel * dt

def two_bodies(m0, x0, v0, m1, x1, v1):
    dt = 0.01
    xc = (m0 * x0 + m1 * x1) / (m0 + m1)
    vc = (m0 * v0 + m1 * v1) / (m0 + m1)
    b0 = sphere(radius=0.1, pos=x0 - xc, vel=v0 - vc, m=m0, color=color.red)
    b1 = sphere(radius=0.1, pos=x1 - xc, vel=v1 - vc, m=m1, color=color.blue)
    traj0 = curve(color=color.red)
    traj1 = curve(color=color.blue)
    for i in range(3000):
        rate(int(1 / dt))
        traj0.append(b0.pos)
        traj1.append(b1.pos)
        dx = b0.pos - b1.pos
        b0.acc = - b0.m * dx / (dx.mag * dx.mag2)
        b1.acc =   b0.m * dx / (dx.mag * dx.mag2)
        b0.vel = b0.vel + b0.acc * dt
        b1.vel = b1.vel + b1.acc * dt
        b0.pos = b0.pos + b0.vel * dt
        b1.pos = b1.pos + b1.vel * dt

def main():
    two_bodies(2.0, vector(1,0,0),  vector(0,0.5,0),
               1.0, vector(-1,0,0), vector(0,0,0))
main()
