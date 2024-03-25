# import numpy as np
# import matplotlib.pyplot as plt

# @np.vectorize
# def hills_vortex(x, y):
#     # Define the Hill's vortex potential
#     psi = x**2 + y**2 - 3 * (x*x + y*y)**(1/2)

#     # Calculate the streamfunction
#     streamfunction = np.arctan2(y, x)

#     # Calculate the velocity components
#     u = -np.gradient(psi, np.array([1, 0]))
#     v =  np.gradient(psi, np.array([0, 1]))

#     return psi, streamfunction, u, v

# # Create the grid
# Nx = 100
# Ny = 100
# x, y = np.linspace(-2, 2, Nx), np.linspace(-2, 2, Ny)

# # Evaluate the Hill's vortex potential, streamfunction, and velocity components
# psi, streamfunction, u, v = hills_vortex(x, y)

# # Plot the streamfunction using quiver
# fig, ax = plt.subplots(figsize=(8, 6))
# ax.quiver(x, y, u, v, scale_arrows=True, cmap='coolwarm')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_title('Hill\'s Vortex Streamfunction')

# plt.show()


import numpy as np
import matplotlib.pyplot as plt

def Hills_vortex(r, theta, U, a = 1):
    #upper equation - r <= 1
    if r <= a:
        psi =  3*U/4 * (1 - r**2/a**2) * r**2 * (np.sin(theta))**2
        print('r <= 1')
    #lower equation - r>1
    else:
        psi = - U/2 * (1 - a**3/r**3) * r**2 * (np.sin(theta))**2
        print('r > 1')
    return psi

def pol2cart(r, theta, x, y):
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    return(x, y)


def Scase_psi(r, theta):
    #upper equation - r <= 1
    if r <= 1:
        psi =  (3*r**2 * (1 - r**2))/4 * (np.sin(theta))**2
        print('r <= 1')
    #lower equation - r>1
    else:
        psi = - (r**3 - 1)/2*r * (np.sin(theta))**2
        print('r > 1')
    return psi    

r = np.linspace(0, 4, 100)
theta = np.linspace(0, np.pi, 20)

x = np.linspace(0, r[-1], 100)
y = np.linspace(-r[-1], r[-1], 20)

X, Y = np.meshgrid(y, x)

U = 1
a = 1

psi = np.zeros((len(r), len(theta)))
psi[:,:] = 1
print('psi')
print(psi.shape)
print('r')
print(r.shape)
print('theta')
print(theta.shape)

for i in range(len(r)):
    print(i)
    for j in range(len(theta)):
        psi[i, j] = Hills_vortex(r[i], theta[j], U, a)



f1, ax1 = plt.subplots()
ax1.contourf(psi)
plt.show()

# x, y = pol2cart(r, theta, x, y)


f2, ax2 = plt.subplots() # pretty sure that this plot is theta on the x-axis and r on the y-axis
cont = ax2.contourf(X, Y, psi)
plt.colorbar(cont, ax = ax2)
plt.show()