from keras.layers import Dropout, Dense
from keras.models import Model
from keras.utils import plot_model
from dataset import *
import numpy as np

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    policy = tf.keras.mixed_precision.experimental.Policy('mixed_float16')
    tf.keras.mixed_precision.experimental.set_policy(policy)
    train_ds, val_ds = datadata()  # create datasets

    # Layering
    # Keras Functional API
    # Documentation on Inception V4 https://arxiv.org/pdf/1602.07261.pdf
    net, input_for_model = stem()  # copy Keras Input object, net to be passed along

    net = inception_block_a(net)  # Inception V4: inception a
    net = reduction_block_a(net)  # Inception V4: reduction a
    net = inception_block_b(net)  # Inception V4: inception b
    net = reduction_block_b(net)  # Inception V4: inception b

    net = inception_block_c(net)  # Inception V4: inception_c
    net = AveragePooling2D()(net)
    net = Dropout(dropout_keep_prob)(net)  # Inception V4: dropout 0.2

    # Softmax function is used for the output layer only (at least in most cases) to ensure that the sum of the
    # components of output vector is equal to 1 (for clarity see the formula of softmax cost function).
    # def softmax():
    #     z = np.exp(x - np.max(x))
    #     return z / z.sum()
    net = Dense(2, activation='softmax', name='dense_output')(net)

    model = Model(inputs=input_for_model, outputs=net, name="SD2_D02")
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
    history = model.fit(np.array(train_ds), validation_data=np.array(val_ds), epochs=epochs)
