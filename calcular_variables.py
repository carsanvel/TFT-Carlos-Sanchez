import pandas as pd
import numpy as np
import detectar_empresas_familiares
import diversidad_genero
import porcentaje_propiedad
import propietario_directivo
import math


datos_host = pd.read_excel('datos_host/datos_sin_faltantes.xlsx')
datos_infor = pd.read_excel('datos_infor/datos_sin_faltantes.xlsx')
datos = [datos_host, datos_infor]

columnas = ['NOMBRE', 'GACELA', 'VENTAS', 'ACTIVOS', 'EMPLEADOS', 'CREC_VENTAS', 'CREC_ACTIVOS', 'CREC_EMPLEADOS', 'INDICE_BS', 'EDAD', 'LIQUIDEZ',
           'LIQUIDEZ_INMEDIATA', 'SOLVENCIA', 'LOG_FLUJO_EFECTIVO', 'LOG_FONDO_MANIOBRA', 'APALANCAMIENTO', 'ROA', 'ROE',
           'MARGEN', 'MARGEN_OPERATIVO', 'CAP_CORR_EXP_VENTAS', 'DEUDA_BANC_ACTIVO', 'DEUDA_CP_DEUDA_TOTAL', 'PATRIMONIO_ACTIVO',
           'PATRIMONIO_DEUDA', 'COBERTURA_GASTOS_FINANCIEROS', 'COSTE_EMPLEADO', 'VENTAS_EMPLEADO', 'RATIO_ACTIVO_FIJO',
           'ROTACION', 'ENDEUDAMIENTO', 'RATIO_ACTIVO_CORRIENTE', 'PASIVO_CORRIENTE_PATRIMONIO', 'RESERVAS_ACTIVOS', 'VENTAS_FONDO_MANIOBRA',
           'RATIO_ACTIVO_INTANGIBLE', 'FAMILIAR', 'INTERESES_VENTAS', 'LOG_CAP_CORR_EXP', 'DEUDA_NETA', 'GASTOS_PERSONAL_VENTAS',
            'PATRIMONIO_ACTIVO_FIJO', 'EXPORTADOR', 'PROPIETARIO_DIRECTIVO', 'DIVERSIDAD_GENERO', 'VENTAS_ACTIVOS', 'ACT_CP_SIN_EXIST_VENTAS',
            'PORCENTAJE_PROPIEDAD', 'GRUPO_EMPRESARIAL', 'CREC_VENTAS_EMPLEADO']

res_host = pd.DataFrame(columns=columnas)
res_infor = pd.DataFrame(columns=columnas)
resultados = [res_host, res_infor]

accionistas_directivos_host = pd.read_excel('datos_host/accionistas_directivos.xlsx').fillna('')
accionistas_directivos_infor = pd.read_excel('datos_infor/accionistas_directivos.xlsx').fillna('')
accionistas_directivos = [accionistas_directivos_host, accionistas_directivos_infor]

nombres_hombres = pd.read_csv(r'spanish-names\hombres.csv')
nombres_mujeres = pd.read_csv(r'spanish-names\mujeres.csv')

for i in range(len(datos)):

    row = {}

    for firm in range(len(datos[i])):
        print(firm)
        # Extraemos los datos que son necesarios para calcular más de una variable
        fecha = datos[i]['FECHA'][firm]
        vent_16 = datos[i]['VENTAS_2016'][firm]
        vent_15 = datos[i]['VENTAS_2015'][firm]
        act_16 = datos[i]['ACTIVO_2016'][firm]
        act_15 = datos[i]['ACTIVO_2015'][firm]
        emp_16 = datos[i]['EMPLEADOS_2016'][firm]
        emp_15 = datos[i]['EMPLEADOS_2015'][firm]
        pasivo_cp = datos[i]['PASIVO_CORRIENTE'][firm]
        pasivo_lp = datos[i]['PASIVO_NO_CORRIENTE'][firm]
        activo_corriente = datos[i]['ACTIVO_CORRIENTE'][firm]
        efectivo = datos[i]['EFECTIVO'][firm]
        deudores = datos[i]['DEUDORES'][firm]
        inversiones_fin = datos[i]['INVERSIONES_FINANCIERAS_CP'][firm]
        flujo_efectivo = datos[i]['FLUJO_EFECTIVO'][firm]
        fondo_maniobra = datos[i]['FONDO_MANIOBRA'][firm]
        roa = datos[i]['ROA'][firm]
        roe = datos[i]['ROE'][firm]
        margen = datos[i]['MARGEN'][firm]
        ebit = datos[i]['EBIT'][firm]
        existencias = datos[i]['EXISTENCIAS'][firm]
        prov_cp = datos[i]['PROVISIONES_CP'][firm]
        acreedores = datos[i]['ACREEDORES'][firm]
        period_cp = datos[i]['PERIODIFICACIONES_CP'][firm]
        deuda_banc_cp = datos[i]['DEUDAS_CREDITO_CP'][firm]
        deuda_banc_lp = datos[i]['DEUDAS_CREDITO_LP'][firm]
        deuda_cp = datos[i]['DEUDAS_CP'][firm]
        deuda_lp = datos[i]['DEUDAS_LP'][firm]
        patrimonio = datos[i]['PATRIMONIO_NETO'][firm]
        gasto_personal = datos[i]['GASTO_PERSONAL'][firm]
        act_fijos = datos[i]['ACTIVO_NO_CORRIENTE'][firm]
        activo_intangible = datos[i]['ACTIVO_INTANGIBLE'][firm]
        deuda_total = deuda_cp + deuda_lp
        ccexp = efectivo + existencias + deudores - prov_cp - acreedores - period_cp
        ccexp_ventas = ccexp / vent_16
        ventas_empleado = vent_16 / emp_16
        ventas_empleado_15 = vent_15 / emp_15


        # Calculamos las variables y las guardamos en la nueva fila del dataframe
        row['NOMBRE'] = datos[i]['NOMBRE'][firm]
        row['GACELA'] = datos[i]['GACELA'][firm]
        row['VENTAS'] = vent_16
        row['CREC_VENTAS'] = (vent_16 - vent_15) / vent_15
        row['ACTIVOS'] = act_16
        row['CREC_ACTIVOS'] = (act_16 - act_15) / act_15
        row['VENTAS_ACTIVOS'] = vent_16 / act_16
        row['EMPLEADOS'] = emp_16
        row['CREC_EMPLEADOS'] = (emp_16 - emp_15) / emp_15
        row['INDICE_BS'] = (emp_16 - emp_15) * (emp_16 / emp_15)
        row['LIQUIDEZ'] = activo_corriente / pasivo_cp
        row['SOLVENCIA'] = act_16 / (pasivo_cp + pasivo_lp)
        row['LIQUIDEZ_INMEDIATA'] = (efectivo + deudores + inversiones_fin) / pasivo_cp
        row['APALANCAMIENTO'] = datos[i]['APALANCAMIENTO'][firm]
        row['ROE'] = roe
        row['ROA'] = roa
        row['MARGEN'] = margen
        row['MARGEN_OPERATIVO'] = ebit / vent_16
        row['CAP_CORR_EXP_VENTAS'] = ccexp_ventas
        row['ACT_CP_SIN_EXIST_VENTAS'] = (activo_corriente - existencias) / vent_16
        row['DEUDA_BANC_ACTIVO'] = (deuda_banc_lp + deuda_banc_cp) / act_16
        row['DEUDA_NETA'] = deuda_cp + deuda_lp - efectivo - inversiones_fin
        row['PATRIMONIO_ACTIVO'] = patrimonio / act_16
        row['COSTE_EMPLEADO'] = gasto_personal / emp_16
        row['GASTOS_PERSONAL_VENTAS'] = gasto_personal / vent_16
        row['RATIO_ACTIVO_FIJO'] = act_fijos / act_16
        row['VENTAS_EMPLEADO'] = ventas_empleado
        row['CREC_VENTAS_EMPLEADO'] = (ventas_empleado - ventas_empleado_15) / ventas_empleado_15
        row['ROTACION'] = datos[i]['ROTACION'][firm]
        row['ENDEUDAMIENTO'] = (deuda_total) / (pasivo_lp + pasivo_cp)
        row['RATIO_ACTIVO_CORRIENTE'] = activo_corriente / act_16
        row['PASIVO_CORRIENTE_PATRIMONIO'] = pasivo_cp / patrimonio
        row['RATIO_ACTIVO_INTANGIBLE'] = activo_intangible / act_16
        row['INTERESES_VENTAS'] = datos[i]['GASTOS_FIN'][firm] / vent_16
        row['RESERVAS_ACTIVOS'] = datos[i]['RESERVAS'][firm] / act_16

        # Cálculo de la edad de la empresa y la guardamos en la fila del dataframe
        if type(fecha) == str:
           row['EDAD'] = 2022 - int(fecha[6:10])
        else:
           row['EDAD'] = 2022 - int(fecha.strftime("%d %b %Y ")[7:11])


        # Aplicamos logaritmos a aquellas variables que lo necesitan y las guardamos en la fila del dataframe
        variables_finales = ['LOG_FLUJO_EFECTIVO', 'LOG_FONDO_MANIOBRA', 'LOG_CAP_CORR_EXP']
        datos_iniciales = [datos[i]['FLUJO_EFECTIVO'][firm], fondo_maniobra, ccexp]
        for col in range(len(variables_finales)):
            var = datos_iniciales[col]
            if var < 0:
                row[variables_finales[col]] = -1 * np.log(-1 * var)
            elif var > 0:
                row[variables_finales[col]] = np.log(var)
            else:
                row[variables_finales[col]] = np.log(0.1)


        # Calculo de variables conflictivas por posible división por 0
        variables_finales = ['DEUDA_CP_DEUDA_TOTAL', 'PATRIMONIO_DEUDA', 'PATRIMONIO_ACTIVO_FIJO', 'VENTAS_FONDO_MANIOBRA']
        divisiones = [(deuda_cp, deuda_total), (patrimonio, deuda_total), (patrimonio, act_fijos), (vent_16, fondo_maniobra)]
        for col in range(len(variables_finales)):
            ####### Falta comprobar que hacemos con divisiones negativas
            if divisiones[col][1] == 0:
                row[variables_finales[col]] = divisiones[col][0]
            else:
                row[variables_finales[col]] = divisiones[col][0] / divisiones[col][1]


        # Si faltaba esta ratio es porque los intereses eran 0 (seguimos el mismo protocolo de antes) RECORDAR LO DE CALCULAR LAS MEDIAS
        if datos[i]['RATIO_COBERTURA_INTERESES'][firm] == 'n.s.':
            row['COBERTURA_GASTOS_FINANCIEROS'] = ebit
        else:
            row['COBERTURA_GASTOS_FINANCIEROS'] = datos[i]['RATIO_COBERTURA_INTERESES'][firm]



        # Determinamos si la empresa exporta
        if datos[i]['EXPORTADOR'][firm] == 'Exportador' or datos[i]['EXPORTADOR'][firm] == 'Importador / Exportador':
            row['EXPORTADOR'] = 1
        else:
            row['EXPORTADOR'] = 0

        # Llamamos a la función que determina si el propietario es directivo
        row['PROPIETARIO_DIRECTIVO'] = propietario_directivo.propietario_es_directivo(datos[i]['ACCIONISTA_ES_DIRECTOR'][firm],
                                                                                         datos[i]['ACCIONISTAS_PROPIEDAD'][firm])

        # Identificación de si la empresa es failiar
        tipo_matriz = datos[i]['TIPO_MATRIZ'][firm]
        empresa = datos[i]['NOMBRE'][firm]
        nombres = accionistas_directivos[i][accionistas_directivos[i]['EMPRESA'] == empresa]
        accionistas = []
        directivos = []
        for j in nombres.index:
            tipo = nombres['TIPO'][j]
            nombre = [nombres['NOMBRE'][j], nombres['APELLIDO_1'][j], nombres['APELLIDO_2'][j]]
            if tipo == 'ACCIONISTA':
                accionistas.append(nombre)
            else:
                directivos.append(nombre)
        empresa_familiar = detectar_empresas_familiares.es_empresa_familiar(accionistas, directivos, tipo_matriz, nombres_hombres, nombres_mujeres)
        row['FAMILIAR'] = empresa_familiar

        # Llamamos a la función que calcula la diversidad de genero en los directivos
        row['DIVERSIDAD_GENERO'] = diversidad_genero.diversidad_genero(directivos, nombres_mujeres, nombres_hombres)

        # Llamamos a la función que calcula la propiedad del accionista principal
        row['PORCENTAJE_PROPIEDAD'] = porcentaje_propiedad.porcentaje_propiedad(datos[i]['NOMBRE_ACCIONISTAS'][firm],
                                                                                   datos[i]['ACCIONISTAS_PROPIEDAD'][firm])

        # Determinamos si la empresa pertenece a un grupo empresarial
        if datos[i]['EMPRESAS_GRUPO'][firm] > 0:
            row['GRUPO_EMPRESARIAL'] = 1
        else:
            row['GRUPO_EMPRESARIAL'] = 0

        # Guardamos la fila en el dataframe
        resultados[i] = resultados[i].append(row, ignore_index=True)

            
resultados[0].to_excel('datos_host/variables.xlsx', index=False)
resultados[1].to_excel('datos_infor/variables.xlsx', index=False)
