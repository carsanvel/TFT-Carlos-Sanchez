from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import sys
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import KFold

# Se cargan datos de entrenamiento y test
datos_train = pd.read_excel('datos_host/train_host.xlsx')
datos_test = pd.read_excel('datos_host/test_host.xlsx')

# Los de entrenamiento se separan en gacelas y no gacelas
gacelas_train = datos_train[datos_train['GACELA'] == 1]
no_gacelas_train = datos_train[datos_train['GACELA'] == 0]


kf = KFold(n_splits=round(len(no_gacelas_train)/len(gacelas_train)), shuffle=True)

# Se se paran variables explicativas y la explicada
y_train_gacelas = gacelas_train.iloc[:, 1].to_numpy()
x_train_gacelas = gacelas_train.iloc[:, 2:43].to_numpy()
y_train_no_gacelas = no_gacelas_train.iloc[:, 1].to_numpy()
x_train_no_gacelas = no_gacelas_train.iloc[:, 2:43].to_numpy()

x_test = datos_test.iloc[:, 2:43].to_numpy()
y_test = datos_test.iloc[:, 1].to_numpy()

# Se genera el modelo de regresión logística
model = LogisticRegression(warm_start=True, max_iter=100000)
for i in range(100):
    # Se llevan a cabo las divisiones en folds
    kf = KFold(n_splits=round(len(no_gacelas_train) / len(gacelas_train)), shuffle=True, random_state=i)
    # Se entrena en todos los folds
    for fold in kf.split(x_train_no_gacelas):
        x_fold = x_train_no_gacelas[fold[1]]
        y_fold = y_train_no_gacelas[fold[1]]

        x_train = np.concatenate((x_fold, x_train_gacelas))
        y_train = np.concatenate((y_fold, y_train_gacelas))

        model.fit(x_train, y_train)

np.set_printoptions(threshold=sys.maxsize)
y_pred = model.predict(x_test)

fpr, tpr, thres = roc_curve(y_test, y_pred, pos_label=1)
print(auc(fpr, tpr))
print(fpr, tpr)

