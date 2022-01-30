
import math

# Calcula el umbral de clasificación de un modelo que situa el punto óptimo enla curva ROC
def calcula_umbral_optimo(tpr, fpr, thresholds):
    mejor = 0.5
    mejor_dis = 10000000000
    i_buena = 0
    for i in range(len(thresholds)):
        dis = math.sqrt(math.pow((1 - tpr[i]), 2) + math.pow(fpr[i], 2))
        if dis < mejor_dis:
            mejor = thresholds[i]
            mejor_dis = dis
            i_buena = i
    print(mejor, tpr[i_buena], fpr[i_buena])