import pandas as pd
import math

dfs = pd.read_excel("Pasta1.xlsx", sheet_name='Pasta1')

voltage = dfs['Tensão'].T.array._ndarray
decibel = dfs['Db'].T.array._ndarray
decibel_calculate = [(13.904*math.log(x)+92.459) for x in voltage]
error = []
equations = []

for x in range(len(decibel_calculate)):
    error.append((decibel_calculate[x] - decibel[x]).round(4))

print("Voltage Measure, Error")

for i in range(len(error)-1):
    #print("%.4f,          %.4f" %(voltage[i],error[i]))
    x = -error[i+1] + error[i]
    y = -voltage[i] + voltage[i+1]
    const = -voltage[i+1]*error[i] + voltage[i]*error[i+1]

    equation = ("y = (%.4fx + %.4f) / %.4f" %(-x,-const,y))
    print(equation)
    equations.append(equation)

