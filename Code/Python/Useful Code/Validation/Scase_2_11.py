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

# now calculate for sigma <= 1
        

levels = np.linspace(-10, 10, 51)
#surf(r,z,Psi)
f1, ax1 = plt.subplots()
cont = ax1.contour(r,z,Psi,levels, colors = 'black')# cmap = 'bwr')#, colors = 'black')#,'k-')
# f1.colorbar(cont, ax = ax1)
# ax1. imshow(Psi, extent=[0, 4, -4, 4], origin='lower', cmap='RdGy')
ax1.set_xlim([0, 4])
ax1.set_ylim([-4, 4])
ax1.set_xlabel('r')
ax1.set_ylabel('z')
plt.title(r'Contour plot of $\Psi$ with contour levels set to every 0.2')


levels = np.linspace(-10, 10, 75)
# print(levels)
#surf(r,z,Psi)
f1, ax1 = plt.subplots()
cont = ax1.contour(r,z,Psi,levels, colors = 'black')# cmap = 'bwr')
# f1.colorbar(cont, ax = ax1)
# ax1. imshow(Psi, extent=[0, 4, -4, 4], origin='lower', cmap='RdGy')
ax1.set_xlim([0, 4])
ax1.set_ylim([-4, 4])
ax1.set_xlabel('r')
ax1.set_ylabel('z')
# plt.title(r'Contour plot of $\Psi$ with contour levels set to ~ every 0.27')


f2, ax2 = plt.subplots()
ax2.contour(r,z,Psi,levels, colors = 'black')
ax2.set_xlim([0, 3])
ax2.set_ylim([-1.25, 1.25])
plt.title(r'Contour plot of $\Psi$')
plt.show()
