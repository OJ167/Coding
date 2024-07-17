### Code to create an eulerian vortex ring model based on two Rankine vortex cores
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.ndimage import gaussian_filter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])


#Create the field
N = 100                               # Number of points in each direction
x_start, x_end = 0, 100.0             # x-direction boundaries
y_start, y_end = -50.0, 50.0          # y-direction boundaries
x = np.linspace(x_start, x_end, N)    # computes a 1D-array for x
y = np.linspace(y_start, y_end, N)    # computes a 1D-array for y
X, Y = np.meshgrid(x, y)              # generates a mesh grid

### Create one core
Gamma1 = -1 #strength of the first vortex core
x01, y01 = 0, 5 #core locations of the first core
u1 =  (Gamma1 / (2 * np.pi)) * (Y - y01) / ((X - x01)**2 + (Y - y01)**2)
v1 = -(Gamma1 / (2 * np.pi)) * (X - x01) / ((X - x01)**2 + (Y - y01)**2)


### Create the second core
Gamma2 = 1 #strength of the first vortex core
x02, y02 = 0, -5 #core locations of the first core
u2 =  (Gamma2 / (2 * np.pi)) * (Y - y02) / ((X - x02)**2 + (Y - y02)**2)
v2 = -(Gamma2 / (2 * np.pi)) * (X - x02) / ((X - x02)**2 + (Y - y02)**2)


### Superpose the cores

u, v = u1+u2, v1+v2



### Plot the flow
# plt.figure(figsize=(8, 6))
plt.streamplot(X, Y, u, v, density=2, linewidth=1, arrowsize=2, arrowstyle='->', color="b")


# Plot the vortex center
plt.plot(x01, y01, 'ro')  # Red dot for core 1 center
plt.plot(x02, y02, 'ko')  # Black dot for core 2 centre

# Set plot limits and labels
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('2D Vortex Flow Field')
plt.grid(True)
# plt.show()

#### Making a time series

t_length = 100

u = np.zeros([t_length, N, N])
v = np.zeros([t_length, N, N])

for i in range(t_length):
    #Core 1
    u1 =  (Gamma1 / (2 * np.pi)) * (Y - y01) / ((X - (x01+i))**2 + (Y - y01)**2)
    v1 = -(Gamma1 / (2 * np.pi)) * (X - (x01+i)) / ((X - (x01+i))**2 + (Y - y01)**2)
    #Core 2
    u2 =  (Gamma2 / (2 * np.pi)) * (Y - y02) / ((X - (x02+i))**2 + (Y - y02)**2)
    v2 = -(Gamma2 / (2 * np.pi)) * (X - (x02+i)) / ((X - (x02+i))**2 + (Y - y02)**2)
    u[i,:,:], v[i,:,:] = u1+u2, v1+v2

# u = gaussian_filter(u, 1)
# v = gaussian_filter(v, 1)

frame = 50 
f1, ax1 = plt.subplots()
ax1.streamplot(X, Y, u[frame,:,:], v[frame,:,:], density=2, linewidth=1, arrowsize=2, arrowstyle='->', color="b")
ax1.plot(x01+frame, y01, 'ro')  # Red dot for core 1 center
ax1.plot(x02+frame, y02, 'ko')  # Black dot for core 2 centre
plt.xlim(0, 100)
plt.ylim(-50, 50)




f2, ax2 = plt.subplots()
ax2.quiver(X, Y, u[frame,:,:], v[frame,:,:])
ax2.plot(x01+frame, y01, 'ro')  # Red dot for core 1 center
ax2.plot(x02+frame, y02, 'ko')  # Black dot for core 2 centre
plt.xlim(0, 100)
plt.ylim(-50, 50)
# plt.show()

vorticity, vorticity_gauss = oj.calculate_vorticity(u, v)

f3, ax3 = plt.subplots()
ax3.set_title('vorticity plot')
# ax3.contourf(X, Y, vorticity[frame,:,:], cmap = 'seismic')
ax3.contourf(X, Y, v[frame,:,:], cmap = 'copper')
# plt.colorbar(cmap = 'seismic')



f4, ax4 = plt.subplots()
ax4.plot(u[frame,:,frame], 'k')
ax4.plot(49, 0.15, 'ro')
# plt.show()

oj.animate_cube_quiver(u, v, u,)

Circulation = oj.sum_Vorticity(u, v)
print(Circulation.shape)

f5, ax5 = plt.subplots()
ax5.set_title('Circulation Against Time')
ax5.plot(Circulation)
ax5.set_ylim(0, 3)
plt.show()