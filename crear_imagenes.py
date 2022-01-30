import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

plt.rcParams['image.cmap'] = 'gray'

variables_host = pd.read_excel('datos_host/variables_finales.xlsx')
variables_infor = pd.read_excel('datos_infor/variables_finales.xlsx')
variables = [variables_host, variables_infor]

estadisticos_host = pd.read_excel('datos_host/estadisticos_finales.xlsx')
estadisticos_infor = pd.read_excel('datos_infor/estadisticos_finales.xlsx')
estadisticos = [estadisticos_host, estadisticos_infor]

borrar = ['NOMBRE', 'GACELA']
variables[0].drop(borrar, inplace=True, axis=1)
variables[1].drop(borrar, inplace=True, axis=1)

columnas = [variables[0].columns, variables[1].columns]

# Imagen para hosteleria
list_host = [[19,  2, 15, 25,  3, 20, 21],
             [18, 14,  0, 24, 40, 13, 41],
             [17, 16,  1,  5,  9, 32, 33],
             [ 4, 26, 12, 38, 11,  8, 31],
             [22,  6, 28, 39, 36, 30, 34],
             [23, 27,  7, 29, 37, 10, 35],
             [ 0,  0,  0,  0,  0,  0,  0]]

list_infor = [[18,  4, 10, 11, 12, 21],
              [17, 14, 13,  9,  1, 22],
              [25,26,  2, 0,  6, 19],
              [ 3, 16, 23,  7,  5, 20],
              [15,  8, 24,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0]]


listas = [list_host, list_infor]
coords = [{}, {}]

for i in range(len(coords)):
    for j in range(len(listas[i])):
        for k in range(len(listas[i][0])):
            coords[i][(j, k)] = listas[i][j][k]


array_host = np.full((7,7), 128)
array_infor = np.full((6,6), 128)
arrays = [array_host, array_infor]

for i in range(len(variables)):
    for j in range(len(variables[i])):
        for key in coords[i].keys():
            pos = coords[i].get(key)
            media = estadisticos[i]['MEDIA'][estadisticos[i]['VARIABLE'] == columnas[i][pos]].tolist()[0]
            desv = estadisticos[i]['DESV'][estadisticos[i]['VARIABLE'] == columnas[i][pos]].tolist()[0]
            variable = variables[i][columnas[i][pos]][j]
            val = ((variable - media) / desv) * 100 + 128
            if val > 255:
                val = 255
            elif val < 0:
                val = 0
            arrays[i][key[0], key[1]] = val
            im = Image.fromarray(arrays[i])
            im = im.resize((224, 224))
            im = im.convert("L")
            if i == 0:
                if j < 6272:
                    im.save('imagenes/host/train/0_no_gacela/im' + str(j) + '.jpeg')
                elif j < 9409:
                    im.save('imagenes/host/test/0_no_gacela/im' + str(j) + '.jpeg')
                elif j < 9513:
                    im.save('imagenes/host/train/1_gacela/im' + str(j) + '.jpeg')
                else:
                    im.save('imagenes/host/test/1_gacela/im' + str(j) + '.jpeg')
            else:
                if i < 1193:
                    im.save('imagenes/infor/train/0_no_gacela/im' + str(j) + '.jpeg')
                elif j < 1791:
                    im.save('imagenes/infor/test/0_no_gacela/im' + str(j) + '.jpeg')
                elif j < 1935:
                    im.save('imagenes/infor/train/1_gacela/im' + str(j) + '.jpeg')
                else:
                    im.save('imagenes/infor/test/1_gacela/im' + str(j) + '.jpeg')