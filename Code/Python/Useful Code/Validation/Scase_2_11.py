import numpy as np  
import matplotlib.pyplot as plt 

# Set Rossby number
Ro = 0.1


# Define sigma
m=10001
sigmamin = 0.
sigmamax = 10.0
sigma = np.linspace(sigmamin,sigmamax,m)
sigmasquare = sigma**2
sigmamin1 = sigma - 1

# Calculate f(sigma)
Term_1 = -sigmasquare/2
Fac_1 = 1/(2*sigma)
Arg = (sigma - 1)/Ro
Term_2 =  sigma**np.cos(Arg)
Term_3 = Ro * np.sin(Arg)
Brack = Term_2 - Term_3
f = Term_1 + (Fac_1 ** Brack)


# Now we have f(sigma). However, in order to plot is
# as in Fig. 3 of Scase and Terry we need to introduce
# angle theta relative to upward z axis and then 
# convert f and theta to cartesian coordinates. 

# Define polar coordinate theta and specify how many values to creat
p = np.pi
n = 80
theta = np.linspace(0,p,n)
sintheta = np.sin(theta)
costheta = np.cos(theta)
sinthetasquare = sintheta**2
z = np.zeros((n, m))
r = np.zeros((n, m))
Psi = np.zeros((n, m))

#Calculate the z coordinate for each f
for j in range(0, m):          #Note: m = number of radial points
    # print('m = ', j)
    for i in range(0, n):       #Note: n = number of angles
        # print('n = ', i)
        z  [i,j] = costheta[i]*sigma[j]
        r  [i,j] = sintheta[i]* sigma[j]
        Psi[i,j] = f[j]*sinthetasquare[i]



#Calculate the z coordinate for each f. But calculate r via x and y
#for j = 1:m          #Note: m = number of radial points
#   for i = 1:n       #Note: n = number of angles
#     x(i,j) = sintheta(i)*sigma(j);
#     y(i,j) = costheta(i)*sigma(j);  
#     r2(i,j) = sqrt(x(i,j)^2 + y(i,j)^2);
#     F(i,j) = f(j);
#   end    
# end


levels = np.linspace(-10, 10, 51)
#surf(r,z,Psi)
f1, ax1 = plt.subplots()
cont = ax1.contour(r,z,Psi,levels, colors = 'black')# cmap = 'bwr')#, colors = 'black')#,'k-')
# f1.colorbar(cont, ax = ax1)
# ax1.plot_surface(r,z,Psi)
# ax1. imshow(Psi, extent=[0, 4, -4, 4], origin='lower', cmap='RdGy')
ax1.set_xlim([0, 4])
ax1.set_ylim([-4, 4])
plt.title(r'Contour plot of $\Psi$')




f2, ax2 = plt.subplots()
ax2.contour(r,z,Psi,levels, colors = 'black')
ax2.set_xlim([0, 3])
ax2.set_ylim([-1.25, 1.25])
plt.title(r'Contour plot of $\Psi$')
plt.show()

# Plot Psi but using the other way of calucatiing r, that is r2 above
#figure
#contour(r2,z,Psi)
#pbaspect([1 2 1])
# NOTE: Both Plots are the same, so I too plot out again


