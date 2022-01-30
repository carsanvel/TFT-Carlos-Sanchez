
# Determina si el nombre que se le pasa ha sido ya analizado, teniendo en cuenta que por defecto de SABI
# los apellidos pueden estar en otro orden, o puede estar solo el primer nombre de uno compuesto
def persona_no_analizada(persona, personas):
    for i in range(len(personas)):

        # Comprobamos que los apellidos coincidad, aunque en distinto orden
        if (persona[1] == personas[i][1] and persona[2] == personas[i][2]) or (persona[1] == personas[i][2] and persona[2] == personas[i][1]):

            # Separamos los nombres por espacios por si son compuestos
            nombre1 = persona[0].split(' ')
            nombre2 = personas[i][0].split(' ')

            # Si ninguno de los dos nombres son compuestos, basta con comprobar que sean el mismo
            if len(nombre1) == len(nombre2):
                if persona[0] == personas[i][0]:
                    return False
                elif len(nombre1) == 2:
                    if (nombre1[0] == nombre2[0] and nombre1[1] == nombre2[1]) or (nombre1[1] == nombre2[0] and nombre1[0] == nombre2[1]):
                        return False

            # En caso contrario, comprobamos que uno sea el primero de
            elif len(nombre1) > len(nombre2):
                if nombre2[0] in nombre1:
                    return False
            else:
                if nombre1[0] in nombre2:
                    return False
    return True




# Devuelve verdadero si se consideran pareja las personas recibidad como parametro
def son_pareja(nombres_hombres, nombres_mujeres, personas):
    sexos = ['', '']
    nombres = [personas[0][0], personas[1][0]]
    frec_hombre = 0
    frec_mujer = 0

    # Detectamos el sexo de cada persona
    for i in range(2):
        # Primeramente vemos si el nombre es compuesto, porque en ese caso quizás puede que el nombre compuesto
        # no esté en la lista y haga falta comprobar el primer nombre
        nombre_dividido = nombres[i].split(' ')
        nombres_comprobar = [nombres[i]]
        if len(nombre_dividido) > 1:
            # Si el nombre es compuesto, pues añadimos la posibilidad de que haya que comprobar el primer nombre
            nombres_comprobar.append(nombre_dividido[0])

        # Comprobamos las dos posibilidades
        for j in range(len(nombres_comprobar)):
            es_hombre = nombres_hombres['frec'][nombres_hombres['nombre'] == nombres[i]].tolist()
            es_mujer = nombres_mujeres['frec'][nombres_mujeres['nombre'] == nombres[i]].tolist()

            # Comprobamos si el nombre está en la lista de mujeres o de hombres
            if len(es_hombre) > 0:
                frec_hombre = es_hombre[0]
            if len(es_mujer) > 0:
                frec_mujer = es_mujer[0]

            # Escogemos el sexo para el que el nombre tenga mayor frecuencia
            if frec_hombre > 0 and frec_hombre > frec_mujer:
                sexos[i] = 'hombre'
                break
            elif frec_mujer > 0 and frec_mujer > frec_hombre:
                sexos[i] = 'mujer'
                break

    # Si son sexos distintos devolvemos verdadero
    if (sexos[0] == 'hombre' and sexos[1] == 'mujer') or (sexos[1] == 'hombre' and sexos[0] == 'mujer'):
        return True
    return False


# Devuelve verdadero si se determina a la empresa como familiar
def es_empresa_familiar(accionistas, directivos, tipo_matriz, nombres_hombre, nombres_mujer):

    # Si la matriz es una empresa no es familiar
    if tipo_matriz == 'Empresa' or tipo_matriz == 'Empresa financiera':
        return 0

    # Definimos las variables para el conteo de apellidos y apariciones de cada uno
    total_apellidos = 0
    personas_analizadas = []
    apariciones_apellidos = {}
    listas = [accionistas, directivos]

    # Comprobar coincidencias de apellidos
    for i in range(len(listas)):
        for j in range(len(listas[i])):
            if persona_no_analizada(listas[i][j], personas_analizadas):
                personas_analizadas.append(listas[i][j])
                apellido_1 = listas[i][j][1]
                apellido_2 = listas[i][j][2]
                if apellido_1 != '':
                    total_apellidos = total_apellidos + 1
                    apariciones_apellidos[apellido_1] = apariciones_apellidos.get(apellido_1, 0) + 1
                if apellido_2 != '':
                    total_apellidos = total_apellidos + 1
                    apariciones_apellidos[apellido_2] = apariciones_apellidos.get(apellido_2, 0) + 1

    # Si no hemos detectado apellidos (por ejemplo, accionistas y directivos son empresas) no es familiar
    if total_apellidos == 0:
        return 0

    # Contamos el total de coincidencias de apellidos
    suma = 0
    for value in apariciones_apellidos.values():
        if value > 1:
            suma = suma + value

    # Si las coincidencias de apellidos superan un determinado umbral se considera empresa familiar
    if suma / total_apellidos > 0.4:
        return 1

    # Si se trata de una pareja, se considera empresa familiar
    if len(personas_analizadas) == 2:
        if son_pareja(nombres_hombre, nombres_mujer, personas_analizadas):
            return 1

    # En caso contrario se considera no familiar
    return 0