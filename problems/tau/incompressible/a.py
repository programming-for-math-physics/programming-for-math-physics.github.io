import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100) * 1.0
y = np.arange(50) * 1.0
x,y = np.meshgrid(x, y, indexing='ij')
z = x
print(z.shape)
plt.pcolor(x, y, z)
plt.show()

