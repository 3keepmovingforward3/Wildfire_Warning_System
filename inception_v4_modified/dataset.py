from model import *
import tensorflow as tf
import os
from keras.preprocessing.image import ImageDataGenerator
import numpy as np


tf.get_logger().setLevel('INFO')  # quiet tf logger

sub_class = os.listdir('C:\\Users\\3Keep\\Pictures\\LeptonCaptures\\data\\')
data_directory = 'C:\\Users\\3Keep\\Pictures\\LeptonCaptures\\data\\'


def datadata():
    # Generator
    # define data augmentation configuration
    train_generator = ImageDataGenerator(
        rescale=1 / 255.0,
        samplewise_std_normalization=True,
        samplewise_center=True,
        rotation_range=20,
        zoom_range=0.05,
        width_shift_range=0.05,
        height_shift_range=0.05,
        shear_range=0.05,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.20)

    valid_generator = ImageDataGenerator(
        rescale=1 / 255.0,
        samplewise_std_normalization=True,
        samplewise_center=True,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.20)

    # Training Dataset
    # Flows in sets of batch_size
    train_ds = train_generator.flow_from_directory(
        directory=data_directory,
        target_size=IMG_SIZE,
        color_mode="grayscale",
        batch_size=batch_size,
        subset='training',
        shuffle=True,
        seed=np.random.randint(seed_size),
        classes=class_names,
        class_mode='binary'
    )

    # Validation Dataset
    # Flows in sets of batch_size
    validation_generator = valid_generator.flow_from_directory(
        directory=data_directory,
        target_size=IMG_SIZE,
        color_mode="grayscale",
        batch_size=batch_size,
        subset='validation',
        shuffle=True,
        seed=np.random.randint(seed_size),
        classes=class_names,
        class_mode='binary'
    )

    return train_generator, validation_generator

    # model = keras.Model(inputs=inputs, outputs=outputs, name="new_model")
    # model.summary()


    # history = model.fit(
    #   train_generator,
    #  epochs=epochs,
    # validation_data=validation_generator)
