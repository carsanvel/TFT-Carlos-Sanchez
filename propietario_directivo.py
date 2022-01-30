
import pandas as pd

# Si el accionistra mayoritario es directivo devuelve 1
def propietario_es_directivo(son_directivos, propiedades):
    if pd.isna(propiedades) or pd.isna(son_directivos):
        return 0
    lista_propiedades = propiedades.replace('  ', ' ').replace('>', '').replace('<', '').split('\n')
    lista_son_dir = son_directivos.replace('  ', ' ').split('\n')
    for i in range(len(lista_propiedades)):
        if lista_propiedades[i] != '-' and lista_propiedades[i] != 'NG' and lista_propiedades[i] != 'ADV' and lista_propiedades[i] != 'MO':
            if float(lista_propiedades[i].replace(',', '.')) >= 50 and lista_son_dir[i] == 'Current manager':
                return 1
    return 0