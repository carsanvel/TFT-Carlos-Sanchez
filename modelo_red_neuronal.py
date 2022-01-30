from keras.layers import Input, Lambda, Dense, Flatten, GlobalAveragePooling2D
from keras.models import Model
from keras.applications.resnet import ResNet50, ResNet101, ResNet152
from keras.applications.inception_v3 import InceptionV3
from keras.applications.vgg19 import VGG19

# Cargamos los modelos ya entrenados
resnet_host = ResNet50(weights='imagenet', input_shape=(224,224,3), include_top=False)
resnet_infor = ResNet50(weights='imagenet', input_shape=(224,224,3), include_top=False)
vgg_host = VGG19(weights='imagenet', input_shape=(224,224,3), include_top=False)
vgg_infor = VGG19(weights='imagenet', input_shape=(224,224,3), include_top=False)
inception_host = InceptionV3(weights='imagenet', input_shape=(224,224,3), include_top=False)
inception_infor = InceptionV3(weights='imagenet', input_shape=(224,224,3), include_top=False)

# Lista con todos los modelos que recorrer
modelos = [resnet_host, resnet_infor, vgg_host, vgg_infor, inception_host, inception_infor]
nombres = ['resnet_host', 'resnet_infor', 'vgg_host', 'vgg_infor', 'inception_host', 'inception_infor']

for i in range(len(modelos)):
  # Volvemos las capas no entrenables
  for layer in modelos[i].layers:
    layer.trainable = False

  # Añadimos las capas finales que llevan a cabo la clasificación
  inputs = Input(shape=(224,224,3))
  x = modelos[i](inputs, training=False)
  x = GlobalAveragePooling2D()(x)
  x = Dense(256, activation='relu')(x)
  outputs = Dense(2, activation='softmax')(x)
  model = Model(inputs, outputs)

  # Guardamos el modelo
  model.save('modelos/' + nombres[i] + '.h5')