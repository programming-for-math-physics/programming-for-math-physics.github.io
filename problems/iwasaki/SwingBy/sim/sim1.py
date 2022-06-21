
import visual
import math
import sys

# meter
EARTH_RADIUS = 6356.752 * 1000
# kg
EARTH_MASS = 5.972 * (10 ** 13)
# kg
PROBE_MASS = 1000.0
# mmm/kg/ss -11
G = 6.67384
# m/s
PROBE_SPEED = 8.0 * 1000

# m/s
EARTH_SPEED = 29.78 * 1000 * 0

# DAY PER FRAME
DPF = 0.001 / 30.0
STEP_DIV = 1000

# SHOW SCALE
VIEWSCALE = 1.0 / 2000000

day = 0
earth_pos = (0.0, 0.0)
probe_pos = (EARTH_RADIUS * 1.5, -EARTH_RADIUS * 1.5)
probe_vel = (0.0, 0.0)
probe_acc = (0.0, 0.0)

def sim_setup(angle):
    global probe_pos
    global probe_vel
    global probe_acc
    global earth_pos
    probe_pos = (EARTH_RADIUS * 1.5, -EARTH_RADIUS * 1.5)
    probe_vel = (PROBE_SPEED * math.sin(angle), PROBE_SPEED * math.cos(angle))
    probe_acc = (0.0,0.0)

def sim_step():
    global probe_pos
    global probe_vel
    global probe_acc
    global earth_pos
    # f = GMm/r^2
    distance = math.sqrt((probe_pos[0] - earth_pos[0]) ** 2 + (probe_pos[1] - earth_pos[1]) ** 2)
    force = G * EARTH_MASS * PROBE_MASS / (distance * distance)
    force_vec = (force * (earth_pos[0] - probe_pos[0]) / distance, force * (earth_pos[1] - probe_pos[1]) / distance)
    probe_acc = (force_vec[0] / PROBE_MASS, force_vec[1] / PROBE_MASS)
    probe_vel = (probe_vel[0] + probe_acc[0] * DPF / STEP_DIV * 24 * 3600, probe_vel[1] + probe_acc[1] * DPF / STEP_DIV * 24 * 3600)
    probe_pos = (probe_pos[0] + probe_vel[0] * DPF / STEP_DIV * 24 * 3600, probe_pos[1] + probe_vel[1] * DPF / STEP_DIV * 24 * 3600)
    earth_vel_angle = 0
    earth_pos = (earth_pos[0] + EARTH_SPEED * math.cos(earth_vel_angle * math.pi / 180) * DPF / STEP_DIV * 24 * 3600, earth_pos[1] + EARTH_SPEED * math.sin(earth_vel_angle * math.pi / 180) * DPF / STEP_DIV * 24 * 3600)

argv = sys.argv
argc = len(argv)

sim_setup(0 / 180 * math.pi)

counter = 0
visual.sphere(radius = 0.01, pos = (EARTH_RADIUS * 15 * VIEWSCALE, EARTH_RADIUS * 15 * VIEWSCALE))
visual.sphere(radius = 0.01, pos = (EARTH_RADIUS * -15 * VIEWSCALE, EARTH_RADIUS * -15 * VIEWSCALE))

earth = visual.sphere(color = visual.color.blue, radius = EARTH_RADIUS * VIEWSCALE)
while(1):
    earth.pos = (earth_pos[0] * VIEWSCALE, earth_pos[1] * VIEWSCALE)
    if(counter % 20 == 0):
        probe = visual.sphere(color = visual.color.white, radius = 0.40)
        probe.pos = (probe_pos[0] * VIEWSCALE, probe_pos[1] * VIEWSCALE)
    for i in range(0, STEP_DIV):
        sim_step()
    day += DPF
    visual.rate(1/DPF)
    counter += 1
    if(counter % 60 == 0):
        vel = math.sqrt(probe_vel[0] ** 2 + probe_vel[1] ** 2)
        distance = math.sqrt((probe_pos[0] - earth_pos[0]) ** 2 + (probe_pos[1] - earth_pos[1]) ** 2)
        energy = 0.5 * PROBE_MASS * vel * vel - G * EARTH_MASS * PROBE_MASS / distance
        print(str(vel/1000) + "[km/s], " + str(energy/1000/1000) + "[MJ]")
