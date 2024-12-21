import sys
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

u0 = 0.2
l0 = 0.1
omega = 3

Re = oj.Rej(u0, l0)
print('Re_j = ', Re)
Ro = oj.Ro(u0, omega)
print('Ro = ', Ro)
Ek = oj.Ek(omega)
print('Ek = ', Ek)