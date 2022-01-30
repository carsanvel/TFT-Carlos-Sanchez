import pandas as pd

variables_host = pd.read_excel('datos_host/variables.xlsx')
variables_infor = pd.read_excel('datos_infor/variables.xlsx')
variables = [variables_host, variables_infor]

# Variables finalmente escogidas para ambos modelos
columnas_host = ['VENTAS', 'ACTIVOS', 'EMPLEADOS', 'CREC_VENTAS', 'CREC_ACTIVOS', 'EDAD', 'MARGEN', 'MARGEN_OPERATIVO',
                 'COSTE_EMPLEADO', 'VENTAS_EMPLEADO', 'VENTAS_FONDO_MANIOBRA', 'GASTOS_PERSONAL_VENTAS',
                 'ACT_CP_SIN_EXIST_VENTAS', 'CREC_VENTAS_EMPLEADO']

columnas_infor = ['VENTAS', 'ACTIVOS', 'EMPLEADOS', 'CREC_VENTAS', 'CREC_ACTIVOS', 'CREC_EMPLEADOS', 'EDAD',
                 'COSTE_EMPLEADO', 'CREC_VENTAS_EMPLEADO']

columnas = [columnas_host, columnas_infor]

# Donde se guardaran los ficheros con los estadísticos
destino = ['datos_host/variables_finales.xlsx', 'datos_infor/variables_finales.xlsx']

dir_estadisticos = ['datos_host/estadisticos.xlsx', 'datos_infor/estadisticos.xlsx']
destino_estadisticos = ['datos_host/estadisticos_finales.xlsx', 'datos_infor/estadisticos_finales.xlsx']

for i in range(len(variables)):
    estadisticos = pd.read_excel(dir_estadisticos[i])
    variables_finales = variables[i][columnas[i]]
    for j in range(len(columnas[i])):
        column = columnas[i][j]

        var1 = 'DIST_MEDIA_' + column
        var2 = 'NORM_CUADRADO_' + column
        media = estadisticos['MEDIA'][estadisticos['VARIABLE'] == column].tolist()[0]
        desv = estadisticos['DESV'][estadisticos['VARIABLE'] == column].tolist()[0]
        variables_finales[var1] = (variables_finales[column] - media).abs()
        variables_finales[var2] = ((variables_finales[column] - media) / desv) * ((variables_finales[column] - media) / desv)

        row = {'VARIABLE': var1, 'MEDIA': variables_finales[var1].mean(), 'DESV': variables_finales[var1].std()}
        estadisticos = estadisticos.append(row, ignore_index=True)
        row = {'VARIABLE': var2, 'MEDIA': variables_finales[var2].mean(), 'DESV': variables_finales[var2].std()}
        estadisticos = estadisticos.append(row, ignore_index=True)


    variables_finales.to_excel(destino[i], index=False)
    estadisticos.to_excel(destino_estadisticos[i], index=False)

