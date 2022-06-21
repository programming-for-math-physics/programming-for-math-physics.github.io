import visual
import random

for i in range(5000):
    x = -1.0 + 2.0 * random.random()
    y = -1.0 + 2.0 * random.random()
    z = -1.0 + 2.0 * random.random()
    if x*x + y*y + z*z < 1.0:
        visual.sphere(pos=(x, y, z),radius=0.02, color=visual.color.yellow)
    else:
        visual.sphere(pos=(x, y, z),radius=0.01)

