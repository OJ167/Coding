### Code to create an eulerian vortex ring model based on two Rankine vortex cores
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.ndimage import gaussian_filter
import matplotlib.colors as colors
import matplotlib.cm

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
oj.thesis_plot_settings()


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
# plt.style.use(["science", "vibrant", "no-latex"])
# matplotlib.rc('xtick', labelsize=8) 
# matplotlib.rc('ytick', labelsize=8) 


#Create the field
Nx = 239                               # Number of points in each direction
Ny = 149
Nx = 100                               # Number of points in each direction
Ny = 100
x_start, x_end = 0, 100.0             # x-direction boundaries
y_start, y_end = -50.0, 50.0          # y-direction boundaries
x = np.linspace(x_start, x_end, Nx)    # computes a 1D-array for x
y = np.linspace(y_start, y_end, Ny)    # computes a 1D-array for y
X, Y = np.meshgrid(x, y)              # generates a mesh grid

### Create one core
Gamma1 = -1 #strength of the first vortex core
x01, y01 = 0, 10 #core locations of the first core
u1 =  (Gamma1 / (2 * np.pi)) * (Y - y01) / ((X - x01)**2 + (Y - y01)**2)
v1 = -(Gamma1 / (2 * np.pi)) * (X - x01) / ((X - x01)**2 + (Y - y01)**2)


### Create the second core
Gamma2 = 1 #strength of the first vortex core
x02, y02 = 0, -10 #core locations of the first core
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

u = np.zeros([t_length, Ny, Nx])
v = np.zeros([t_length, Ny, Nx])

for i in range(t_length):
    #Core 1
    u1 =  (Gamma1 / (2 * np.pi)) * (Y - y01) / ((X - (x01+i))**2 + (Y - y01)**2)
    v1 = -(Gamma1 / (2 * np.pi)) * (X - (x01+i)) / ((X - (x01+i))**2 + (Y - y01)**2)
    #Core 2
    u2 =  (Gamma2 / (2 * np.pi)) * (Y - y02) / ((X - (x02+i))**2 + (Y - y02)**2)
    v2 = -(Gamma2 / (2 * np.pi)) * (X - (x02+i)) / ((X - (x02+i))**2 + (Y - y02)**2)
    u[i,:,:], v[i,:,:] = u1+u2, v1+v2

u = gaussian_filter(u, 1)
v = gaussian_filter(v, 1)

frame = 50 
f1, ax1 = plt.subplots(figsize=(5.5, 3.5))
# ax1.set_title('Simulated Vortex Ring Streamlines')
ax1.streamplot(X, Y, u[frame,:,:], v[frame,:,:], density=2, linewidth=1, arrowsize=2, arrowstyle='->', color="k")
ax1.plot(x01+frame, y01, 'bo')  # Red dot for core 1 center
ax1.plot(x02+frame, y02, 'ro')  # Black dot for core 2 centre
ax1.set_xlabel(r'$z$')
ax1.set_ylabel(r'$r$')
plt.xlim(0, 100)
plt.ylim(-50, 50)
# f1.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Thesis Images/Ch5_Intial_and_Validation/Simulated flows/PLACEHOLDER_Sim_Ring_streamplot.png', dpi = 400)
# f1.savefig('C:/Coding/Sim_Ring_streamplot.png', dpi = 400)



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
ax3.contourf(X, Y, vorticity[frame,:,:], cmap = 'seismic')
# ax3.contourf(X, Y, v[frame,:,:], cmap = 'copper')
# plt.colorbar(cmap = 'seismic')



f4, ax4 = plt.subplots(figsize=(5.5, 4))
ax4.plot(u[frame,:,frame], 'k')
ax4.set_xlabel(r'$r$')
ax4.set_ylabel(r'$u$')
# f4.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Thesis Images/Simulated flows/PLACEHOLDER_Sim_Ring_u_Profile.png', dpi = 400)
# plt.show()

# oj.animate_cube_quiver(u, v, u,)
# oj.animate_cube_contourf(u)

Circulation = oj.sum_Vorticity(u, v)
print(Circulation.shape)

f5, ax5 = plt.subplots()
ax5.set_title('Circulation Against Time')
ax5.plot(Circulation)
# ax5.set_ylim(0, 3)
# plt.show()

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u, v)
print(VortLocMax.shape)

f6, ax6 = plt.subplots(figsize=(5.5, 3.5))
# ax6.set_title('Simulated Vortex Ring Tracking')
ax6.plot(VortLocMax[:,1]+5, 'o-',label = 'local maximum', color = 'r')
ax6.plot(VortLocMin[:,1], 'o-',label = 'local minimum', color = 'b')
ax6.set_xlabel(r'$t$')
ax6.set_ylabel(r'$z$')
plt.legend()
# f6.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Thesis Images/Simulated flows/Sim_Ring_tracking.png', dpi = 400)
# f6.savefig('C:/Coding/Sim_Ring_tracking.png', dpi = 400)
# plt.show()


#remaking the plots for my thesis

fig, ax = plt.subplots(1, 3, sharex=True, figsize=(5.5, 3.5), layout='constrained')
ax[0].set_title('u', fontsize=9)
ax[0].plot(x-50, u[frame,:,frame], color = 'b')
ax[0].set_xlabel(r"$r$")
ax[1].set_title('v', fontsize=9)
ax[1].plot(x-50, v[frame,:,frame], color = 'b')
ax[1].set_xlabel(r"$r$")
ax[2].set_title(r'$\omega_{z}$', fontsize=9)
ax[2].plot(x-50, vorticity[frame,:,frame], color = 'b')
ax[2].set_xlabel(r"$r$")
fig.savefig('C:/Coding/Sim_Ring_profiles.png', dpi = 400)
plt.show()

