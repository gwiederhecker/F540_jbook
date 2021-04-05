import pylef   # importar pylef 
import visa    # importar a bilioteca pyVISA para lidar com virtualização de instrumentos
import matplotlib.pyplot as plt  # importar a bilioteca pyplot para fazer gráficos
import numpy as np   # importar a biblioteca Numpy para lidar com matrizes
import time          # importar a bilioteca para funções temporais
import pandas as pd   # importa bilioteca pandas para  lidar com processamento de dados
import os
# próxima linha faz plotar o gráfico dentro do notebook
# %matplotlib inline   

def screenshot(filename):
    #setting up hardcopy
#     scope.instr.timeout = 20000 # set timeout to 10 seconds
    strings = ['SAVE:IMAGE:FILEFORMAT BMP',
               'HARDCOPY:BUTTON PRINTS',
              'HARDCopy:PORT']
    for string in strings:
        scope.write(string)
        scope.wait()
    #screen shot
    scope.instr.write('HARDCOPY START')
    values = scope.instr.read_raw() 
    scope.wait()
    newFile = open(filename+'.bmp', 'wb')
    newFileByteArray = bytearray(values)
    newFile.write(newFileByteArray)
    newFile.close()
    return filename+'.bmp'+ ' saved!'