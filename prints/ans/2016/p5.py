from visual import *

def point_mass(x0, v0, T):
    xy = box(length=200.0, height=1.0, width=50.0)
    s = sphere(pos=x0, radius=5, color=color.red)
    s.vel = v0
    n = 10000
    dt = T / n
    g = vector(0.0, -9.8, 0.0)
    scene.autocenter = 0
    while s.pos.y >= 0.0:
        rate(1.0 / dt)
        alpha = g - s.vel * 0.5
        s.vel = s.vel + alpha * dt
        s.pos = s.pos + s.vel * dt
    print s.pos.x

def run5_1(theta):
    v = 50.0
    vx = v * math.cos(theta)
    vy = v * math.sin(theta)
    point_mass(vector(0,0,0), vector(vx,vy,0), 10.0)

# run5_1(math.pi / 3.0)

def point_mass2(m0, x0, v0, m1, x1, v1, T):
    s0 = sphere(pos=x0, vel=v0, m=m0, radius=10, color=color.yellow)
    s1 = sphere(pos=x1, vel=v1, m=m1, radius=1, color=color.red)
    scene.autocenter = 0
    dt = 1.0/300
    n = int(T / dt)
    for i in range(n):
        rate(1.0 / dt)
        r = s1.pos - s0.pos
        a = - 1.0 / r.mag ** 3
        alpha1 =  a * s0.m * r 
        alpha0 = -a * s1.m * r
        s0.vel = s0.vel + alpha0 * dt
        s0.pos = s0.pos + s0.vel * dt
        s1.vel = s1.vel + alpha1 * dt
        s1.pos = s1.pos + s1.vel * dt
        
def run5_2():
    point_mass2(1000.0,  vector(0,0,0),  vector(0,0,0),
                1.0,     vector(40,0,0), vector(0,5,0), 100.0)
        
run5_2()

#
#   p-----> x
#   |
#   |
#   |
#   |
#   |
#   |
# b |
#   z

def baseball():
    pitcher_height = 1.4
    batter_height = 1.7
    pitcher_to_batter = 18.44
    batter_to_homeplate = 0.5
    batter_foot = vector(-batter_to_homeplate, 0, pitcher_to_batter)
    batter_eye = batter_foot + vector(0, batter_height, 0)
    kmph = 140.0
    xy = box(pos=(0, 0, pitcher_to_batter/2),
             length=batter_to_homeplate * 4,
             height=0.1, width=pitcher_to_batter,
             color=color.yellow)
    pitcher = arrow(axis=(0, pitcher_height, 0))
    batter = arrow(pos=batter_foot, axis=batter_eye - batter_foot)
    mound = ellipsoid(length=1.0, height=0.5, width=1.0, color=color.yellow)
    b = sphere(pos=(0,pitcher_height,0), radius=0.07, color=color.white)
    b.vel = vector(0, 0, kmph * 1000.0 / 3600.0)
    t = 0.0
    dt = 1.0 / 30.0
    g = vector(0.0, -9.8, 0.0)
    # g = vector(0.0, 0.0, 0.0)
    scene.autoscale = 0
    scene.autocenter = 0
    scene.center = b.pos
    scene.forward = (b.pos - batter_eye) * 20.0
    scene.fov = 0.5
    rate(0.3)
    while b.z < pitcher_to_batter * 2:
        rate(1.0 / dt)
        alpha = g - b.vel * 0.5
        b.vel = b.vel + alpha * dt
        b.pos = b.pos + b.vel * dt
