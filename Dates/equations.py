import pandas as pd
import math

dfs = pd.read_excel("Pasta1.xlsx", sheet_name='Sheet1')

voltage = dfs['Tensão'].T.array._ndarray
decibel = dfs['Db'].T.array._ndarray
decibel_calculate = [(13.904*math.log(x)+92.459) for x in voltage]
error = []
equations = []

for x in range(len(decibel_calculate)):
    error.append((decibel_calculate[x] - decibel[x]).round(4))

x = -error[1] + error[0]
y = -voltage[0] + voltage[1]
const = -voltage[1]*error[0] + voltage[0]*error[1]

equation = ("\n  dB = y - (%.2f * maxVal + (%.6f)) / %.4f);" %(-x,-const,y))
string = ("if(maxVal <= %s){" %(voltage[1]))
string += equation + "\n}"
equations.append(string)

for i in range(1,len(error)-2):
    x = -error[i+1] + error[i]
    y = -voltage[i] + voltage[i+1]
    const = -voltage[i+1]*error[i] + voltage[i]*error[i+1]

    equation = ("\n  dB = y - (%.2f * maxVal + (%.6f)) / %.4f);" %(-x,-const,y))
    string = ("else if(maxVal <= %s){" %(voltage[i+1]))
    string += equation + "\n}"
    equations.append(string)

x = -error[len(error)-1] + error[len(error)-2]
y = -voltage[len(error)-1] + voltage[len(error)-2]
const = -voltage[len(error)-2]*error[len(error)-1] + voltage[len(error)-1]*error[len(error)-2]

equation = ("\n  dB = y - (%.2f * maxVal + (%.6f)) / %.4f);" %(-x,-const,y))
string = ("else{" %(voltage[1]))
string += equation + "\n}"
equations.append(string)

for i in equations:
    print(i)

