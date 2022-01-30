import pandas as pd
import numpy as np

# Columnas en las que si faltan datos borrar las filas
columnas = ['VENTAS_2016', 'VENTAS_2017', 'VENTAS_2018', 'VENTAS_2019']

# Lectura de los datos de ventas de las empresas
empresas_infor = pd.read_excel(r'datos_infor\ventas.xlsx').dropna(subset=columnas).reset_index(drop=True)
empresas_host = pd.read_excel(r'datos_host\ventas.xlsx').dropna(subset=columnas).reset_index(drop=True)

# Cambia los n.d. por n.a y borramos los datos faltantes
empresas_infor.replace({'n.d.': np.NAN}, inplace=True)
empresas_host.replace({'n.d.': np.NAN}, inplace=True)
empresas_infor = empresas_infor.dropna(subset=columnas).reset_index(drop=True)
empresas_host = empresas_host.dropna(subset=columnas).reset_index(drop=True)

# Para recorrer los listados de empresas
empresas = [empresas_host, empresas_infor]

# Creamos una lista con los resultados de ambos tipos de empresas
gacelas_infor = pd.DataFrame(columns=('NIF',))
gacelas_host = pd.DataFrame(columns=('NIF',))
no_gacelas_infor = pd.DataFrame(columns=('NIF',))
no_gacelas_host = pd.DataFrame(columns=('NIF',))
gacelas = [gacelas_host, gacelas_infor]
no_gacelas = [no_gacelas_host, no_gacelas_infor]
count_gacelas = [0,0]
count_no_gacelas = [0,0]

for i in range(len(empresas)):
    for fila in range(len(empresas[i])):
        ventas_16 = empresas[i]['VENTAS_2016'][fila]
        ventas_17 = empresas[i]['VENTAS_2017'][fila]
        ventas_18 = empresas[i]['VENTAS_2018'][fila]
        ventas_19 = empresas[i]['VENTAS_2019'][fila]
        crec1 = (ventas_17 - ventas_16) / ventas_16
        crec2 = (ventas_18 - ventas_17) / ventas_17
        crec3 = (ventas_19 - ventas_18) / ventas_18
        if crec1 >= 0.2 and crec2 >= 0.2 and crec3 >= 0.2:
            gacelas[i] = gacelas[i].append({'NIF': empresas[i]['NIF'][fila]}, ignore_index=True)
            count_gacelas[i] = count_gacelas[i] + 1
        else:
            no_gacelas[i] = no_gacelas[i].append({'NIF': empresas[i]['NIF'][fila]}, ignore_index=True)
            count_no_gacelas[i] = count_no_gacelas[i] + 1

gacelas[0].to_csv(r'datos_host\nif_gacelas.csv', index=False, header=False)
no_gacelas[0].to_csv(r'datos_host\nif_no_gacelas.csv', index=False, header=False)
gacelas[1].to_csv(r'datos_infor\nif_gacelas.csv', index=False, header=False)
no_gacelas[1].to_csv(r'datos_infor\nif_no_gacelas.csv', index=False, header=False)


print("Sector de la hostelería:")
print('Nº de gacelas: ', count_gacelas[0])
print('Nº de no gacelas: ', count_no_gacelas[0])
print("Total de empresas: ", count_gacelas[0] + count_no_gacelas[0])

print("##################################")

print("Sector de los servicios informáticos:")
print('Nº de gacelas: ', count_gacelas[1])
print('Nº de no gacelas: ', count_no_gacelas[1])
print("Total de empresas: ", count_gacelas[1] + count_no_gacelas[1])