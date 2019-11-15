import matplotlib.pyplot as plt
import numpy as np 
import math

array = np.zeros(200)
fs = 1/len(array)

for i in range(len(array)):
    vref = 0.03887
    vi = (i+1) * vref
    array[i] = 20 * math.log10(vi/vref) + 40

plt.plot(array)
plt.show()
print(array)