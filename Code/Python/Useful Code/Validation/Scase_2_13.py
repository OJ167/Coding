import numpy as np
import matplotlib.pyplot as plt

# Set Rossby number
Ro = 0.1
alpha = 1/Ro

alpha = np.pi/2
lamda = 15

# Define sigma
m=10001
sigmamin = 0.01
sigmamax = 7
sigma = np.linspace(sigmamin,sigmamax,m)
sigmasquare = sigma**2
sigmamin1 = sigma - 1

# Calculate F(sigma)

Term_1 = lamda/(alpha**2)
numerator = (sigma * alpha * np.cos(sigma*alpha)) - np.sin(sigma*alpha)
denominator = sigma * ((alpha * np.cos(alpha)) - np.sin(alpha))
frac = numerator/denominator - sigmasquare
F = Term_1 * frac




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
        Psi[i,j] = F[j]*sinthetasquare[i]


levels = np.linspace(-10, 10, 501)
#surf(r,z,Psi)
f1, ax1 = plt.subplots()
cont = ax1.contour(r, z, Psi, levels, colors = 'black')# cmap = 'bwr')#, colors = 'black')#,'k-')
# f1.colorbar(cont, ax = ax1)
# ax1. imshow(Psi, extent=[0, 4, -4, 4], origin='lower', cmap='RdGy')
ax1.set_xlim([0, 4])
ax1.set_ylim([-4, 4])
plt.title(r'Contour plot of $\Psi$ with contour levels set to every 0.2')
plt.show()