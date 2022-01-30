

def porcentaje_propiedad(accionistas, propiedades):

    # Si no hay información de los accionistas, supondremos que es o.5
    if accionistas.strip() == "There is no shareholders information for this company":
        return 0.5
    lista_propiedades = propiedades.replace('  ', ' ').replace('>', '').replace('<', '').split('\n')
    lista_accionistas = accionistas.replace('  ', ' ').split('\n')

    # Si el listado de propiedades es 0, se dividirá entre el numero de accionistas la propiedad
    if len(lista_propiedades) == 0:
        if len(lista_accionistas > 0):
            return 100 / len(lista_accionistas)
        else:
            return 0.5

    max = 0
    # Se busca el porcentaje de porpiedad del accionista mayoritario
    for i in range(len(lista_propiedades)):
        if lista_propiedades[i] != '-' and lista_propiedades[i] != 'NG' and lista_propiedades[i] != 'ADV' and lista_propiedades[i] != 'MO':
            num = float(lista_propiedades[i].replace(',', '.'))
            if num > max:
                max = num

    if max > 0:
        return max
    elif len(lista_accionistas) > 0:
        return 100 / len(lista_accionistas)
    else:
        return 0.5