import numpy as np
import matplotlib.pyplot as plt
import sys

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def draw_mandelbrot(xmin,xmax,ymin,ymax,width,height,max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (r1,r2,np.array([[mandelbrot(complex(r, i),max_iter) for r in r1] for i in r2]))

xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
resolution = 10000
width, height = resolution, resolution
max_iter = 512

oj.tic()
xset, yset, mandelbrot_set = draw_mandelbrot(xmin,xmax,ymin,ymax,width,height,max_iter)
oj.toc()

plt.contourf(mandelbrot_set, extent=(xmin, xmax, ymin, ymax), cmap = 'Greys')
plt.show()