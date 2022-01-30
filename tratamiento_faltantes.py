import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import ExtraTreesRegressor

empresas_host = pd.read_excel('datos_host/datos_iniciales.xlsx')
empresas_infor = pd.read_excel('datos_infor/datos_iniciales.xlsx')
empresas = [empresas_host, empresas_infor]
destinos = ['datos_host/datos_sin_faltantes', 'datos_infor/datos_sin_faltantes']

# Columnas a las que no hay que analizar los faltantes
columnas_borrar = ['NOMBRE', 'GACELA', 'NIF', 'NOMBRE_ACCIONISTAS', 'ACCIONISTA_ES_DIRECTOR',
                    'ACCIONISTAS_PROPIEDAD', 'NOMBRE_DIRECTORES', 'EMPRESAS_GRUPO',
                    'EXPORTADOR', 'TIPO_MATRIZ', 'FECHA']

for i in range(len(empresas)):
    copia = empresas[i].copy()
    empresas[i].drop(columnas_borrar, inplace=True, axis=1)

    # Sustituimos los valores n.d. y n.s. para que puedan ser interpretados como nan
    for j in range(len(empresas[i])):
        for column in empresas[i].columns:
            if empresas[i][column][j] == 'n.d.' or empresas[i][column][j] == 'n.s.':
                empresas[i][column][j] = np.NaN

    # Columnas en que se considera que los valores faltantes son 0
    columnas_rellenar_ceros = ['PROVISIONES_CP', 'PERIODIFICACIONES_CP', 'DEUDAS_CREDITO_LP', 'ACTIVO_INTANGIBLE',
                               'INVERSIONES_FINANCIERAS_CP', 'DEUDAS_CREDITO_CP', 'DEUDAS_CP', 'DEUDAS_LP',
                               'PASIVO_NO_CORRIENTE', 'RESERVAS', 'GASTOS_FIN', 'EXISTENCIAS']

    for column in columnas_rellenar_ceros:
        empresas[i][column] = empresas[i][column].fillna(0)

    # Columnas a las con las que queremos hacer el calculo de las multiples imputaciones
    columnas = ['VENTAS_2016', 'VENTAS_2015', 'ACTIVO_2016', 'ACTIVO_2015',
                'ACTIVO_CORRIENTE', 'ACTIVO_NO_CORRIENTE', 'PATRIMONIO_NETO',
                'PASIVO_CORRIENTE', 'PASIVO_NO_CORRIENTE', 'EMPLEADOS_2016',
                'EMPLEADOS_2015', 'FLUJO_EFECTIVO', 'FONDO_MANIOBRA', 'APALANCAMIENTO',
                'ROA', 'ROTACION', 'ROE', 'EBIT', 'MARGEN', 'EFECTIVO', 'EXISTENCIAS',
                'DEUDORES', 'PROVISIONES_CP', 'ACREEDORES', 'PERIODIFICACIONES_CP',
                'DEUDAS_CREDITO_CP', 'DEUDAS_CREDITO_LP', 'DEUDAS_CP', 'DEUDAS_LP',
                'GASTOS_FIN', 'GASTO_PERSONAL', 'ACTIVO_INTANGIBLE',
                'INVERSIONES_FINANCIERAS_CP', 'RESERVAS']

    datos_calcular = empresas[i][columnas]
    imputations = []

    # Realizamos las imputaciones 10 veces distintas
    for j in range(10):

        # Se crea el imputador asignando unos valores minimos que se pueden imputar a cada variables, y escogiendo 8 variables explicativas
        imp = IterativeImputer(estimator=ExtraTreesRegressor(), sample_posterior=False, max_iter=10, random_state=j,
                               n_nearest_features=8, min_value=[0, 0, 1, 1, 1, 1, -np.inf, -np.inf, -np.inf, -np.inf,
                               -np.inf, 0, 0, 0, 0, 0, 0, 0, 0, 0, -np.inf, 0, -np.inf, 0, 1, 0, 1, 1, -np.inf,
                               -np.inf, 1,0, 0, 0], verbose=1)

        # Se realiza el cálculo de los valores
        imp.fit(datos_calcular)
        imputations.append(imp.transform(datos_calcular))

    # Una vez se han hecho los 10 modelos de imputación, se imputal finalmente la media de los mismos
    for j in range(len(datos_calcular)):
        for k in range(len(columnas)):
            if np.isnan(datos_calcular[columnas[k]][j]):
                media = 0
                for m in range(10):
                    media = media + imputations[m][j, k]
                datos_calcular[columnas[j]][i] = media / 10

    # Finalmente se añaden aquellos datos que no fueron usados en las imputaciones
    col_añadir = ['NOMBRE', 'GACELA', 'CNAE', 'CIUDAD', 'NIF', 'NOMBRE_ACCIONISTAS', 'ACCIONISTA_ES_DIRECTOR',
                  'ACCIONISTAS_PROPIEDAD', 'NOMBRE_DIRECTORES', 'COTIZA', 'EMPRESAS_GRUPO', 'RATIO_COBERTURA_INTERESES',
                  'EXPORTADOR', 'TIPO_MATRIZ', 'FECHA', 'SOLVENCIA', 'LIQUIDEZ', 'LIQUIDEZ_INMEDIATA']

    for column in col_añadir:
        datos_calcular[column] = copia[column].values

    datos_calcular.to_excel(destinos[i], index=False)



