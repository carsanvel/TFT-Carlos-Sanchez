
import sklearn
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, RocCurveDisplay
from matplotlib import pyplot as plt
from keras.models import load_model
import calculo_umbral

# Elegimos el modelo a evaluar
model = load_model('modelos/resnet_host.h5')

test_path = 'imagenes/host/test'
test_datagen = ImageDataGenerator()
test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=(224, 224),
        class_mode='categorical',
        shuffle=False)

Y_true = test_generator.classes
Y_pred = model.predict_generator(test_generator)
y_pred = Y_pred[:, 1]


fpr, tpr, thresholds = roc_curve(Y_true, y_pred, pos_label=1)
valor_auc = sklearn.metrics.auc(fpr, tpr)

# Calculamos el umbral opttimo
umbral, valor_tpr, valor_fpr = calculo_umbral.calcula_umbral_optimo(tpr, fpr, thresholds)

# Resultados de las predicciones con el umbral optimo
res = []
for i in range(len(y_pred)):
  if y_pred[i] < umbral:
    res.append(0)
  else:
    res.append(1)

# Si queremos representar la curva ROC
display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=valor_auc,estimator_name='ResNet50')
display.plot()
plt.show()

# Mostrar matriz de confusion
print('Confusion Matrix')
print(confusion_matrix(test_generator.classes, res))

# Mostrar otros resultados como precision y recall
print('Classification Report')
target_names = ['no_gacela', 'gacela']
print(classification_report(test_generator.classes, res, target_names=target_names))