import numpy as np
import matplotlib.pyplot as plt

@np.vectorize
def hills_vortex(x, y):
    # Define the Hill's vortex potential
    psi = x**2 + y**2 - 3 * (x*x + y*y)**(1/2)

    # Calculate the streamfunction
    streamfunction = np.arctan2(y, x)

    # Calculate the velocity components
    u = -np.gradient(psi, np.array([1, 0]))
    v =  np.gradient(psi, np.array([0, 1]))

    return psi, streamfunction, u, v

# Create the grid
Nx = 100
Ny = 100
x, y = np.linspace(-2, 2, Nx), np.linspace(-2, 2, Ny)

# Evaluate the Hill's vortex potential, streamfunction, and velocity components
psi, streamfunction, u, v = hills_vortex(x, y)

# Plot the streamfunction using quiver
fig, ax = plt.subplots(figsize=(8, 6))
ax.quiver(x, y, u, v, scale_arrows=True, cmap='coolwarm')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Hill\'s Vortex Streamfunction')

plt.show()