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
destino = ['datos_host/estadisticos.xlsx', 'datos_infor/estadisticos.xlsx']

for i in range(len(variables)):

    # Creamos el dtaframe donde guardamos los estadisticos
    estadisticos = pd.DataFrame(columns=('VARIABLE', 'MEDIA', 'DESV'))

    for column in columnas[i]:
        # Calculamos los outliers
        q1 = variables[i][column].quantile(0.25)
        q3 = variables[i][column].quantile(0.75)
        ric = q3 - q1
        lim1 = q1 - 3 * ric
        lim2 = q3 + 3 * ric

        # Calculamos los estadísticos sin contar los outliers
        media = variables[i][column][(variables[i][column] > lim1) & (variables[i][column] < lim2)].mean()
        desv = variables[i][column][(variables[i][column] > lim1) & (variables[i][column] < lim2)].std()
        row = {'VARIABLE': column, 'MEDIA': media, 'DESV': desv}
        estadisticos = estadisticos.append(row, ignore_index=True)

    estadisticos.to_excel(destino[i], index=False)