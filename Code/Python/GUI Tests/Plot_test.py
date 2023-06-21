import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1000, 1000, 1000)

#plt.plot(x, np.sin(x))
#plt.plot(x, np.cos(x))
plt.plot(x, x**3 + 3*x +17)

# fig, ax = plt.subplots()  # Create a figure containing a single axes.
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);  # Plot some data on the axes ([x], [y]).
# plt.title("plot test")



plt.show()