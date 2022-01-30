import pandas as pd
import numpy as np
import math
from random import randint

def calcula_energia_host(correlaciones, array):
    energia = 0
    for i1 in range(array.shape[0]-1):
        for j1 in range(array.shape[1]):
            for i2 in range(array.shape[0]-1):
                for j2 in range(array.shape[1]):
                    if i1 != i2 or j1 != j2:
                        var1 = array[i1, j1]
                        var2 = array[i2, j2]
                        key = str(var1) + "-" + str(var2)
                        corr = correlaciones[key]
                        dist = math.pow((i1 - i2), 2) + math.pow((j1 - j2), 2)
                        energia = energia + abs(corr) * dist
    return energia


def calcula_energia_infor(correlaciones, array):
    energia = 0
    for i1 in range(array.shape[0]-1):
        for j1 in range(array.shape[1]):
            if i1 < 5 and (i1 < 4 or j1 < 3):
                for i2 in range(array.shape[0]-1):
                    for j2 in range(array.shape[1]):
                        if i2 < 5 and (i2 < 4 or j2 < 3):
                            if i1 != i2 or j1 != j2:
                                var1 = array[i1, j1]
                                var2 = array[i2, j2]
                                key = str(var1) + "-" + str(var2)
                                corr = correlaciones[key]
                                dist = math.pow((i1 - i2), 2) + math.pow((j1 - j2), 2)
                                energia = energia + abs(corr) * dist
    return energia

variables_host = pd.read_excel('datos_host/variables_finales.xlsx')
variables_infor = pd.read_excel('datos_infor/variables_finales.xlsx')

borrar = ['NOMBRE', 'GACELA']
variables_host.drop(borrar, inplace=True, axis=1)
variables_infor.drop(borrar, inplace=True, axis=1)

correlaciones_host = {}
correlaciones_infor = {}

columnas_host = variables_host.columns
columnas_infor = variables_infor.columns


# Calculamos las correlaciones de ambos grupos de variables
for i in range(len(columnas_host)):
    for j in range(len(columnas_host)):
        if i != j:
            key = str(i) + "-" + str(j)
            correlaciones_host[key] = variables_host[columnas_host[i]].corr(variables_host[columnas_host[j]])

for i in range(len(columnas_infor)):
    for j in range(len(columnas_infor)):
        if i != j:
            key = str(i) + "-" + str(j)
            correlaciones_infor[key] = variables_infor[columnas_infor[i]].corr(variables_infor[columnas_infor[j]])

array_host = np.zeros((7,7), int)
array_infor = np.zeros((6,6), int)
fila = 0
col = 0

# Disposicion inicial hosteleria
for i in range(len(columnas_host)):
    array_host[fila, col] = i
    if col == 6:
        col = 0
        fila = fila + 1
    else:
        col = col + 1

fila = 0
col = 0

# Disposicion inicial informatica
for i in range(len(columnas_infor)):
    array_infor[fila, col] = i
    if col == 5:
        col = 0
        fila = fila + 1
    else:
        col = col + 1

energia_final_host = calcula_energia_host(correlaciones_host,array_host)
energia_final_infor = calcula_energia_infor(correlaciones_infor,array_infor)

intentos = 1001
while intentos < 5:
    num1 = randint(0, 41)
    num2 = randint(0, 41)
    while num2 == num1:
        num2 = randint(0, 41)
    copia = array_host.copy()
    i1 = int(num1 / 7)
    j1 = num1 % 7
    i2 = int(num2 / 7)
    j2 = num2 % 7
    copia[i1, j1] = array_host[i2, j2]
    copia[i2, j2] = array_host[i1, j1]

    energia_nueva = calcula_energia_host(correlaciones_host,copia)
    if energia_nueva < energia_final_host:
        array_host = copia
        energia_final_host = energia_nueva
        intentos = 1
        print(array_host)
        print(energia_final_host)
    else:
        intentos = intentos + 1


intentos = 1001
while intentos < 2:
    num1 = randint(0, 26)
    num2 = randint(0, 26)
    while num2 == num1:
        num2 = randint(0, 26)
    copia = array_infor.copy()
    i1 = int(num1 / 6)
    j1 = num1 % 6
    i2 = int(num2 / 6)
    j2 = num2 % 6
    copia[i1, j1] = array_infor[i2, j2]
    copia[i2, j2] = array_infor[i1, j1]

    energia_nueva = calcula_energia_infor(correlaciones_infor,copia)
    if energia_nueva < energia_final_infor:
        array_infor = copia
        energia_final_infor = energia_nueva
        intentos = 1
        print(array_infor)
        print(energia_final_infor)
    else:
        intentos = intentos + 1
