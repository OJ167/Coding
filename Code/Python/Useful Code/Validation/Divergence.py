import numpy as np  
import matplotlib.pyplot as plt 
import math as maths
from scipy.ndimage import gaussian_filter


y = np.linspace(-10, 10, 101)
x = np.linspace(-10, 10, 101)
X, Y = np.meshgrid(x, y)


x0, y0 = 0, 0 # source location
Gamma = 1 # strength of the source. Negative for a sink

# compute the velocity field on the mesh grid
u = (Gamma / (2 * maths.pi) * (X - x0) / ((X - x0)**2 + (Y - y0)**2))
v = (Gamma / (2 * maths.pi) * (Y - y0) / ((X - x0)**2 + (Y - y0)**2))


f1, ax1 = plt.subplots()
# cont = ax1.contour(x, y, Psi, colors = 'black')# cmap = 'bwr')#, colors = 'black')#,'k-')
# ax1.quiver(X, Y, Psi[:,:])
# ax1.contour(Psi)
ax1.quiver(X, Y, u, v)


f2, ax2 = plt.subplots()
ax2.streamplot(X, Y, u, v, color = 'black', broken_streamlines = False)
ax2.scatter(x0, y0, color = 'red')
# plt.show()



def calculate_divergence(u, v):
    """
    calculates divergence of velocity field
     
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        divergence   : 3D Numpy tensor containing divergence data
        divergence_gauss : 3D Numpy tensor containing divergence data after a gausian filter

    """
    du = np.gradient(u, axis = 1)
    dv = np.gradient(v, axis = 0)
    divergence = du + dv
    divergence_gauss = gaussian_filter(divergence, sigma = 0.7)
    return divergence, divergence_gauss

divergence, divergence_gauss = calculate_divergence(u, v)

f3, ax3 = plt.subplots()
ax3.imshow(divergence)
# plt.show()

f4, ax4 = plt.subplots()
ax4.plot(divergence[50, :])
plt.show()
