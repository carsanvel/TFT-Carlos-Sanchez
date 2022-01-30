

def diversidad_genero(directivos, nombres_mujer, nombres_hombre):
    total = 0
    mujeres = 0

    # Recorremos la lista de directivos
    for i in range(len(directivos)):
        nombre = directivos[i][0]

        # Si el nombre está vacío por cualquier cosa seguimos
        if len(nombre) == 0:
            continue

        frec_hombre = 0
        frec_mujer = 0

        #### Buscamos frecuencia de hombre
        es_hombre = nombres_hombre['frec'][nombres_hombre['nombre'] == nombre].tolist()
        if len(es_hombre) > 0:
            frec_hombre = es_hombre[0]
        es_hombre = nombres_hombre['frec'][nombres_hombre['nombre'] == nombre[0]].tolist()
        if len(es_hombre) > 0:
            if es_hombre[0] > frec_hombre:
                frec_hombre = es_hombre[0]

        #### Buscamos frecuencia de mujer
        es_mujer = nombres_mujer['frec'][nombres_mujer['nombre'] == nombre].tolist()
        if len(es_mujer) > 0:
            frec_mujer = es_mujer[0]
        es_mujer = nombres_mujer['frec'][nombres_mujer['nombre'] == nombre[0]].tolist()
        if len(es_mujer) > 0:
            if es_mujer[0] > frec_mujer:
                frec_mujer = es_mujer[0]

        # Si la puntuación o frecuencia del nombre en la lista de mujeres es mayor, sumamos una mujer
        if frec_hombre > 0 or frec_mujer > 0:
            total = total + 1
            if frec_hombre < frec_mujer:
                mujeres = mujeres + 1

    # En caso de que no se hayan detectado nombres devolvemos 0.5
    if total == 0:
        return 0.5

    # Devolvemos la tasa de mujeres en la directiva
    return mujeres / total