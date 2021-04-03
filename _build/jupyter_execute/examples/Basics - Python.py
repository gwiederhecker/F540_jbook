# Python basics



## Loading packages

import numpy as np
import matplotlib.pyplot as plt

## Arrays

# Python arrays - []

x = [1, 2, 3]
y = 2*x
print(x)
print(y)

x+x

x[2] # elementos de x



Numpy arrays

x = np.array([1, 2, 3])
y = 2*x
print(x)
print(y)
print(x+y)

x+y

**As you see above, native Python and Numpy arrays behave very differently, so be careful!**

# Flow control

list(range(3))

for i in range(3):
  print(i)
  print(i+1)
2+5

for i in range(4):
  print(i)
  if i==2:
    print("2 is great")
  else:
    print("others are also great")

for i in range(4):
  print(i)
  if i==2:
    print("2 is great")
  elif i==3: # else if
    print("3 is also great")
print(2+2)

i=0
while i < 5:
  print(i)
  i += 1 #increase i by 1


## Other forms of iteration

np.array([i+2 for i in range(4)])

# Functions

def helloworld():
  print('helloworld')
def soma(x,y):
  return x+y
def reta(x,a,b):
  return a*x+b


helloworld()
soma(2,3)

x = np.linspace(0,6,10)
for a in range(0,5):
  plt.plot(x,reta(x,a,2))

## Simple plots

x = np.linspace(0,6,1000)
plt.plot(x,np.exp(x),'*')

Adjusting standard plot configurations

#****************************
# Setting up plot configurations
# Configurando gráficos
#****************************
#Adjusting fonts pattern
#Ajsutando fontes padrão dos gráficos
font = { 'weight' : 'normal',
        'size'   : 12}

plt.rc('font', **font)
#Ajsutando espessura das linhas padrão dos gráficos
plt.rcParams['lines.linewidth'] = 2;
plt.locator_params(nticks=4)



# Loading data (Google colab)

import glob
import pandas as pd

# Para usuários do Google Cola
from google.colab import drive
drive.mount('/content/drive')

files = glob.glob('drive/My Drive/Colab Notebooks/F540/2021_1s/*')
print(files)

dataG = pd.read_csv(files[0],sep=';')
dataG.head() # visualize first lines

dataG.columns # list column names

plt.plot(dataG['acfrequency'],dataG['r Gv'],'o-')

plt.semilogx(dataG['acfrequency'],dataG['r Gv'],'o-')

