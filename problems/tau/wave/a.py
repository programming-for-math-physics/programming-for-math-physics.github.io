import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anm
import numpy as np

def generate_plot3d(fig):
    X = np.linspace(-1,1,101)
    Y = np.linspace(-1,1,101)
    X,Y = np.meshgrid(X, Y)
    axis = fig.add_subplot(111, projection="3d")
    for k in np.linspace(0,2 * np.pi,101):
        print("step %f" % k)
        Z = 2 - np.cos(k) * (X * X + Y * Y)
        axis.clear()
        sfc = axis.plot_surface(X, Y, Z)
        axis.set_zlim(0,4)
        yield


def animate_plot3d():
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x,  repeat=0,
                            frames=generate_plot3d(fig),
                            interval=30)
    plt.show()
    return ani

animate_plot3d()
