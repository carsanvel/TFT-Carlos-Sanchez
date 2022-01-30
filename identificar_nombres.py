import pandas as pd

# Función de apoyo que identifica si se trata de una persona o una empresa a partir de una serie de palabras clave
def es_empresa(palabras):
    for palabra in palabras:
        if palabra in ['SOCIEDAD', 'SA', 'SA.', 'S.A', 'S.A.', 'SL', 'SL.', 'S.L', 'S.L.', 'SLU', 'SLU.', 'S.L.U.',
                       'SAU', 'S.À R.L.', 'S.A.U.', 'S.A.R.L', 'INC', 'FUNDACION', 'S', 'SAL', 'RRM', 'ASOC', '&',
                       'SLP', 'GRUPO', 'SELF', 'GROUP', 'LLC', 'OFICIAL']:
            return True
    return False

# Recibe uns String y si esta se trata de un nombre, ya sea compuesto o simple, devuelve la frecuencia de este en España
def frecuencia_nombre(nombre):
    frec = [0, 0]
    nombres = nombre.split(' ')
    listas = [nombres_hombres, nombres_mujeres]
    for i in range(len(listas)):
        frec_nombre = listas[i]['frec'][listas[i]['nombre'] == nombre].tolist()
        if len(frec_nombre) != 0:
            if len(nombres) > 1:
                frec[i] = frec_nombre[0] + listas[i]['frec'][listas[i]['nombre'] == nombres[0]].tolist()[0] + \
                          frecuencia_apellido(nombres[-1]) #Dar prioridad a nombre compuesto frente a primer nombre o coger como apellido la segunda parte
            else:
                frec[i] = frec_nombre[0]
        elif len(nombres) == 2:
            frec1 = listas[i]['frec'][listas[i]['nombre'] == nombres[0]].tolist()
            frec2 = listas[i]['frec'][listas[i]['nombre'] == nombres[1]].tolist()
            if len(frec1) != 0 and len(frec2) != 0:
                frec[i] = min(frec1[0], frec2[0])
    return max(frec)

# Recibe uns String y si esta se trata de un apellido, ya sea compuesto o simple, devuelve la frecuencia de este en España
def frecuencia_apellido(apellido):
    frec_apellido = apellidos['frec_pri'][apellidos['apellido'] == apellido].tolist()
    apellidos_separados = apellido.split(" ")
    frec = 0
    if len(frec_apellido) != 0:
        if(len(apellidos_separados) > 1):
            frec = frec_apellido[0] * 5
        else:
            frec = frec_apellido[0]
    elif len(apellidos_separados) == 2:
        frec1 = apellidos['frec_pri'][apellidos['apellido'] == apellidos_separados[0]].tolist()
        frec2 = apellidos['frec_pri'][apellidos['apellido'] == apellidos_separados[1]].tolist()
        if len(frec1) != 0 and len(frec2) != 0:
            frec = min(frec1[0], frec2[0])
    return frec

# Determina si una combinación es válida por ejemplo, una que no tenga nombre no es válida
def combinacion_valida(comb):
    checklist = [False, False, False]
    posiciones = [[], [], []]
    for i in range(len(comb)):
        if comb[i] == 0:
            checklist[0] = True
            posiciones[0].append(i)
        elif comb[i] == 1:
            checklist[1] = True
            posiciones[1].append(i)
        else:
            checklist[2] = True
            posiciones[2].append(i)
    if checklist[0] == False or checklist[1] == False:
        return False
    for i in range(len(posiciones)):
        for j in range(len(posiciones[i])-1):
            if posiciones[i][j+1] - posiciones[i][j] > 1:
                return False
    return True

# Recorre las diferentes combinaciones y determina aquella con mejor puntuación
def mejor_combinacion(palabras):
    mejor = [0] * len(palabras)
    comb = [0] * len(palabras)
    max = 0
    puntuando_max = 0
    for n in range(pow(3, len(palabras))):
        if combinacion_valida(comb):
            nombre = ''
            ap1 = ''
            ap2 = ''
            puntuando = 0
            for i in range(len(comb)):
                if comb[i] == 0:
                    nombre = nombre + palabras[i] + " "
                elif comb[i] == 1:
                    ap1 = ap1 + palabras[i] + " "
                else:
                    ap2 = ap2 + palabras[i] + " "
            nombre = nombre.strip()
            ap1 = ap1.strip()
            ap2 = ap2.strip()
            punt_nombre = frecuencia_nombre(nombre)
            if punt_nombre > 0:
                puntuando = puntuando + len(nombre.split(" "))
            punt_ap1 = frecuencia_apellido(ap1)
            if punt_ap1 > 0:
                puntuando = puntuando + len(ap1.split(" "))
            punt_ap2 =  frecuencia_apellido(ap2)
            if punt_ap2 > 0:
                puntuando = puntuando + len(ap2.split(" "))
            punt = punt_nombre + punt_ap1 + punt_ap2
            if len(palabras) > 2 and punt_nombre > 0 and punt_ap1 > 0 and punt_ap2 > 0:
                punt = punt + 1000
            if (punt > max and puntuando >= puntuando_max) or (puntuando > puntuando_max):
                max = punt
                puntuando_max = puntuando
                mejor = comb.copy()
        for i in range(len(comb)):
            if comb[i] < 2:
                comb[i] = comb[i] + 1
                break
            else:
                comb[i] = 0
    return mejor



empresas = firms = pd.read_excel(r'datos_host\datos_totales.xlsx')

# Cargamos los ficheros de nombres y apellidos en España
apellidos = pd.read_csv(r'spanish-names\apellidos.csv')
nombres_hombres = pd.read_csv(r'spanish-names\hombres.csv')
nombres_mujeres = pd.read_csv(r'spanish-names\mujeres.csv')

res = pd.DataFrame(columns=('NIF', 'EMPRESA', 'NOMBRE', 'APELLIDO_1', 'APELLIDO_2', 'TIPO'))

for empresa in range(len(empresas)):
    print(empresa)

    # Lidtados de accionistas y directivos
    accionistas = empresas['NOMBRE_ACCIONISTAS'][empresa]
    directivos = firms['NOMBRE_DIRECTORES'][empresa]

    lista_accionistas = accionistas.split("\n")
    lista_directivos = directivos.split("\n")

    # Tratamiento accionistas

    if lista_accionistas[0] != "There is no shareholders information for this company":
        for i in range(len(lista_accionistas)):
            palabras = lista_accionistas[i].replace("  ", " ").upper().split(" ")
            if not es_empresa(palabras):
                if palabras[0] == 'MR' or palabras[0] == 'MRS':
                    palabras.pop(0)
                    combinacion = mejor_combinacion(palabras)
                else:
                    combinacion = mejor_combinacion(palabras)
                nombre = ''
                ap1 = ''
                ap2 = ''
                for pos in range(len(combinacion)):
                    if combinacion[pos] == 0:
                        nombre = nombre + " " + palabras[pos]
                    elif combinacion[pos] == 1:
                        ap1 = ap1 + " " + palabras[pos]
                    else:
                        ap2 = ap2 + " " + palabras[pos]
                print(nombre, ap1, ap2)
                row = {'EMPRESA': empresas['NOMBRE'][empresa], 'NIF': empresas['NIF'][empresa], 'NOMBRE': nombre.strip(),
                       'APELLIDO_1': ap1.strip(), 'APELLIDO_2': ap2.strip(), 'TIPO': 'ACCIONISTA'}
                res = res.append(row, ignore_index = True)

    # Tratamiento directivos
    if lista_directivos[0] != 'Directors / managers / contacts are available, yet none related to the selected filter'\
                and lista_directivos[0] != 'There is no Directors / managers / contacts information for this company':
        for i in range(len(lista_directivos)):
            palabras = lista_directivos[i].replace("  ", " ").upper().split(" ")
            print(palabras)
            if palabras[-1] == 'DEL':
                print(palabras)
            if not es_empresa(palabras):
                if palabras[0] == 'DON' or palabras[0] == 'DOÑA':
                    palabras.pop(0)
                    combinacion = mejor_combinacion(palabras)
                else:
                    combinacion = mejor_combinacion(palabras)
                print(palabras)
                nombre = ''
                ap1 = ''
                ap2 = ''
                for pos in range(len(combinacion)):
                    if combinacion[pos] == 0:
                        nombre = nombre + " " + palabras[pos]
                    elif combinacion[pos] == 1:
                        ap1 = ap1 + " " + palabras[pos]
                    else:
                        ap2 = ap2 + " " + palabras[pos]
                print(nombre, ap1, ap2)
                row = {'EMPRESA': empresas['NOMBRE'][empresa], 'NIF': empresas['NIF'][empresa], 'NOMBRE': nombre.strip(),
                       'APELLIDO_1': ap1.strip(), 'APELLIDO_2': ap2.strip(), 'TIPO': 'DIRECTIVO'}
                res = res.append(row, ignore_index=True)

res.to_excel('.xlsx')