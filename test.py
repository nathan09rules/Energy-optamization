"""from math import cos , sin
import numpy as np

pi = np.pi

x = np.linspace(0 , pi , 4)
s = [sin(i) for i in x]
c = [cos(i) for i in x]

for i in range(len(x)):
    print(x[i] , "|" , s[i] , "|" , c[i] , "|" , i + 1)"""

from math import cos , sin
import math 
import numpy as np

a = [math.pi * 2]

for i in a:
    print(f"{sin(i):.3f} , {cos(i):.3f} , {i}")