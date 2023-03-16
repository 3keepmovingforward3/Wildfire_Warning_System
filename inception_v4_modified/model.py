import keras

from configuration import *
from keras.layers import Input, Concatenate
from keras.layers.convolutional import MaxPooling2D, Convolution2D, AveragePooling2D
from keras.layers.normalization import BatchNormalization


# InceptionV4 :
# definition of stem block
def stem():
    network = Input(shape=shape)
    # stem inception v4
    conv1_3_3 = Convolution2D(32, 3, strides=2, activation='relu', name='conv1_3_3_S2', padding='valid')(network)
    conv2_3_3 = Convolution2D(32, 3, activation='relu', name='conv2_3_3', padding='valid')(conv1_3_3)
    # kernel=1x1 gives correct shape from inception journal paper, but is supposed to be 3x3
    conv3_3_3 = Convolution2D(64, 3, activation='relu', name='conv3_3_3')(conv2_3_3)
    b_conv_1_pool = MaxPooling2D(pool_size=3, strides=2, padding='valid', name='b_conv_1_pool')(conv3_3_3)
    b_conv_1_pool = BatchNormalization()(b_conv_1_pool)
    b_conv_1_conv = Convolution2D(96, 3, strides=2, padding='valid', activation='relu', name='b_conv_1_conv')(conv3_3_3)

    b_conv_1 = Concatenate(axis=3)([b_conv_1_conv, b_conv_1_pool])

    # left after filt-concat
    b_conv4_1_1 = Convolution2D(64, 1, activation='relu', name='conv4_3_3', padding='valid')(b_conv_1)
    b_conv4_3_3 = Convolution2D(96, 3, activation='relu', name='b_conv4_3_3')(b_conv4_1_1)

    # Note 7_1 and 1_7 kernel sizes are changed from study
    b_conv4_1_1_reduce = Convolution2D(64, 1, activation='relu', name='b_conv4_1_1_reduce')(b_conv_1)
    b_conv4_7_1 = Convolution2D(64, [7, 1], activation='relu', name='b_conv4_7_1')(b_conv4_1_1_reduce)
    b_conv4_1_7 = Convolution2D(64, [1, 7], activation='relu', name='b_conv4_1_7')(b_conv4_7_1)
    b_conv4_3_3_v = Convolution2D(96, 3, padding='valid', name='b_conv4_3_3_v')(b_conv4_1_7)
    b_conv4_3_3_v = keras.layers.ZeroPadding2D(padding=3)(b_conv4_3_3_v)
    b_conv_4 = Concatenate(axis=3)([b_conv4_3_3, b_conv4_3_3_v])

    b_conv5_3_3 = Convolution2D(192, 3, padding='valid', activation='relu', name='b_conv5_3_3', strides=2)(b_conv_4)
    b_pool5_3_3 = MaxPooling2D(pool_size=(3, 3), padding='valid', strides=2, name='b_pool5_3_3')(b_conv_4)
    b_pool5_3_3 = BatchNormalization()(b_pool5_3_3)

    b_conv5 = Concatenate(axis=3)([b_conv5_3_3, b_pool5_3_3])
    return b_conv5, network


# definition of inception_block_a
def inception_block_a(input_a):
    inception_a_pool = AveragePooling2D(pool_size=3, name='inception_a_pool', strides=1)(input_a)
    inception_a_pool_1_1 = Convolution2D(96, 1, activation='relu', name='inception_a_pool_1_1')(inception_a_pool)

    inception_a_conv1_1_1 = Convolution2D(96, 3, activation='relu', name='inception_a_conv1_1_1')(input_a)

    inception_a_conv1_3_3_reduce = Convolution2D(64, 3, activation='relu', name='inception_a_conv1_3_3_reduce')(input_a)
    inception_a_conv1_3_3 = Convolution2D(96, 1, activation='relu', name='inception_a_conv1_3_3')(
        inception_a_conv1_3_3_reduce)

    inception_a_conv2_3_3_reduce = Convolution2D(64, 3, activation='relu', name='inception_a_conv2_3_3_reduce')(input_a)
    inception_a_conv2_3_3_sym_1 = Convolution2D(96, 1, activation='relu', name='inception_a_conv2_3_3_sym_1')(
        inception_a_conv2_3_3_reduce)
    inception_a_conv2_3_3 = Convolution2D(96, 1, activation='relu', name='inception_a_conv2_3_3')(
        inception_a_conv2_3_3_sym_1)

    inception_a = Concatenate(axis=3)(
        [inception_a_pool_1_1, inception_a_conv2_3_3, inception_a_conv1_3_3, inception_a_conv1_1_1])
    return inception_a


# definition of inception_block_b
def inception_block_b(input_b):
    inception_b_pool = AveragePooling2D(pool_size=1, name='inception_b_pool')(input_b)
    inception_b_pool_1_1_sym_1 = Convolution2D(128, 1, activation='relu', name='inception_b_pool_1_1_sym_1')(
        inception_b_pool)

    inception_b_conv1_1_1 = Convolution2D(384, 1, activation='relu', name='inception_b_1_1')(input_b)

    inception_b_conv2_1_1_sym_1 = Convolution2D(192, 1, activation='relu', name='inception_b_conv2_1_1_sym_1')(input_b)
    inception_b_conv2_1_7 = Convolution2D(224, 1, activation='relu', name='inception_b_conv2_1_7')(
        inception_b_conv2_1_1_sym_1)
    inception_b_conv2_1_7_2 = Convolution2D(256, 1, activation='relu', name='inception_b_conv2_7_1_2')(
        inception_b_conv2_1_7)

    inception_b_conv3_1_1 = Convolution2D(192, 1, activation='relu', name='inception_b_conv3_1_1')(input_b)
    inception_b_conv3_1_7 = Convolution2D(192, 1, activation='relu', name='inception_b_conv3_1_7')(
        inception_b_conv3_1_1)
    inception_b_conv3_7_1 = Convolution2D(224, 1, activation='relu', name='inception_b_conv3_7_1')(
        inception_b_conv3_1_7)
    inception_b_conv3_1_7_2 = Convolution2D(224, 1, activation='relu', name='inception_b_conv3_1_7_2')(
        inception_b_conv3_7_1)
    inception_b_conv3_7_1_2 = Convolution2D(256, 1, activation='relu', name='inception_b_conv3_7_1_2')(
        inception_b_conv3_1_7_2)

    inception_b = Concatenate(axis=3)(
        [inception_b_pool_1_1_sym_1, inception_b_conv1_1_1, inception_b_conv2_1_7_2, inception_b_conv3_7_1_2])

    return inception_b


# definition of inception_block_c
def inception_block_c(input_c):
    inception_c_pool = AveragePooling2D(pool_size=1, name='inception_c_pool')(input_c)
    inception_c_pool_1_1 = Convolution2D(256, 1, activation='relu', name='inception_b_pool_1_1_1')(inception_c_pool)

    inception_c_1_1 = Convolution2D(256, 1, activation='relu', name='inception_c_1_1')(input_c)

    inception_c_3_3_reduce = Convolution2D(384, 1, activation='relu', name='inception_c_3_3_reduce')(input_c)
    inception_c_1_3_asym_1 = Convolution2D(256, [1, 3], activation='relu', name='inception_c_1_3_asym_1')(
        inception_c_3_3_reduce)
    inception_c_1_3_asym_1 = keras.layers.ZeroPadding2D(padding=(0, 1))(inception_c_1_3_asym_1)
    inception_c_3_1_asym_2 = Convolution2D(256, [3, 1], activation='relu', name='inception_c_3_1_asym_2')(
        inception_c_3_3_reduce)
    inception_c_3_1_asym_2 = keras.layers.ZeroPadding2D(padding=(1, 0))(inception_c_3_1_asym_2)
    inception_c_res = Concatenate(axis=3)([inception_c_1_3_asym_1, inception_c_3_1_asym_2])

    inception_c_5_5_reduce = Convolution2D(384, 1, activation='relu', name='inception_c_5_5_reduce')(input_c)
    inception_c_5_5_asym_1 = Convolution2D(448, [1, 3], name='inception_c_5_5_asym_1')(inception_c_5_5_reduce)
    inception_c_5_5_asym_2 = Convolution2D(512, [3, 1], activation='relu', name='inception_c_5_5_asym_2')(
        inception_c_5_5_asym_1)
    inception_c_5_5_asym_3 = Convolution2D(256, [1, 3], activation='relu', name='inception_c_5_5_asym_3')(
        inception_c_5_5_asym_2)
    inception_c_5_5_asym_3 = keras.layers.ZeroPadding2D(padding=(0, 1))(inception_c_5_5_asym_3)
    inception_c_5_5_asym_4 = Convolution2D(256, [3, 1], activation='relu', name='inception_c_5_5_asym_4')(
        inception_c_5_5_asym_2)
    inception_c_5_5_asym_4 = keras.layers.ZeroPadding2D(padding=(1, 0))(inception_c_5_5_asym_4)

    inception_c_5_5 = Concatenate(axis=3)([inception_c_5_5_asym_4, inception_c_5_5_asym_3])
    inception_c_5_5 = keras.layers.ZeroPadding2D(padding=1)(inception_c_5_5)
    inception_c = Concatenate(axis=3)([inception_c_pool_1_1, inception_c_1_1, inception_c_res, inception_c_5_5])
    return inception_c


def reduction_block_a(reduction_input_a):
    reduction_a_conv1_1_1 = Convolution2D(384,
                                          9,
                                          strides=2,
                                          padding='valid',
                                          activation='relu',
                                          name='reduction_a_conv1_1_1')(reduction_input_a)

    reduction_a_conv2_1_1 = Convolution2D(192,
                                          7,
                                          activation='relu',
                                          name='reduction_a_conv2_1_1')(reduction_input_a)
    reduction_a_conv2_3_3 = Convolution2D(224,
                                          3,
                                          activation='relu',
                                          name='reduction_a_conv2_3_3')(reduction_a_conv2_1_1)
    reduction_a_conv2_3_3_s2 = Convolution2D(256,
                                             1,
                                             strides=2,
                                             padding='valid',
                                             activation='relu',
                                             name='reduction_a_conv2_3_3_s2')(reduction_a_conv2_3_3)

    reduction_a_pool = MaxPooling2D(strides=2,
                                    padding='valid',
                                    pool_size=9,
                                    name='reduction_a_pool')(reduction_input_a)
    # merge reduction_a

    reduction_a = Concatenate(axis=3)([reduction_a_conv1_1_1,
                                       reduction_a_conv2_3_3_s2,
                                       reduction_a_pool])
    return reduction_a


def reduction_block_b(reduction_input_b):
    reduction_b_1_1 = Convolution2D(192, 1, activation='relu',
                                    name='reduction_b_1_1')(reduction_input_b)
    reduction_b_1_3 = Convolution2D(192, 3, strides=2, padding='valid',
                                    name='reduction_b_1_3')(reduction_b_1_1)

    reduction_b_3_3_reduce = Convolution2D(256, 1, activation='relu',
                                           name='reduction_b_3_3_reduce')(reduction_input_b)
    reduction_b_3_3_asym_1 = Convolution2D(256, [1, 3], activation='relu',
                                           name='reduction_b_3_3_asym_1')(reduction_b_3_3_reduce)
    reduction_b_3_3_asym_2 = Convolution2D(320, [3, 1], activation='relu',
                                           name='reduction_b_3_3_asym_2')(reduction_b_3_3_asym_1)
    reduction_b_3_3 = Convolution2D(320, 2, strides=2, activation='relu', padding='valid',
                                    name='reduction_b_3_3')(reduction_b_3_3_asym_2)

    reduction_b_pool = MaxPooling2D(pool_size=3, strides=2, padding='valid')(reduction_input_b)

    # merge the reduction_b

    reduction_b_output = Concatenate(axis=3)([reduction_b_1_3, reduction_b_3_3, reduction_b_pool])

    return reduction_b_output
