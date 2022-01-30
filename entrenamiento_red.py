
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator


def entrenar_red(model, epocas, sector):
    if sector == 'host':
        train_path = 'imagenes/host/train'
    else:
        train_path = 'imagenes/infor/train'

    train_datagen = ImageDataGenerator()
    batch_size = 64
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical')

    model.compile(loss='binary_crossentropy',
                  optimizer='Adadelta',
                  metrics=['accuracy', 'AUC'])

    model.fit(train_generator, epochs=epocas)


# Aquí escogemos cualquier modelo que queramos, las epocas que queramos especificamos el sector, y el origen de los datos de test
model = load_model('modelos/resnet_host.h5')
epocas = 20
sector = 'host'

entrenar_red(model, epocas, sector)

model.save("modelos/resnet_host.h5")

