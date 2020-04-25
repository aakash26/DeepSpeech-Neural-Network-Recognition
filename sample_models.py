from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input, 
    TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU, LSTM)

def simple_rnn_model(input_dim, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(output_dim, return_sequences=True, 
                 implementation=2, name='rnn')(input_data)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(simp_rnn)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model

def rnn_model(input_dim, units, activation, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(units, activation=activation,
        return_sequences=True, implementation=2,dropout_W=0.2, dropout_U=0.1, name='rnn')(input_data)
    # TODO: Add batch normalization 
    bn_rnn = BatchNormalization(name='bn_rnn_1d')(simp_rnn)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_rnn_model(input_dim, filters, kernel_size, conv_stride,
    conv_border_mode, units, output_dim=29):
    """ Build a recurrent + convolutional network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size, 
                     strides=conv_stride, 
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # Add a recurrent layer
    simp_rnn = SimpleRNN(units, activation='relu',
        return_sequences=True, implementation=2, name='rnn')(bn_cnn)
    # TODO: Add batch normalization
    bn_rnn = BatchNormalization(name='bn_rnn_1d')(simp_rnn)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim), name="time_dense")(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model

def cnn_output_length(input_length, filter_size, border_mode, stride,
                       dilation=1):
    """ Compute the length of the output sequence after 1D convolution along
        time. Note that this function is in line with the function used in
        Convolution1D class from Keras.
    Params:
        input_length (int): Length of the input sequence.
        filter_size (int): Width of the convolution kernel.
        border_mode (str): Only support `same` or `valid`.
        stride (int): Stride size used in 1D convolution.
        dilation (int)
    """
    if input_length is None:
        return None
    assert border_mode in {'same', 'valid'}
    dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'valid':
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // stride

def deep_rnn_model(input_dim, units, recur_layers, output_dim=29):
    """ Build a deep recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # TODO: Add recurrent layers, each with batch normalization
    simp_rnn_1 = GRU(units, activation='relu',return_sequences=True, implementation=2,dropout_W=0.02, dropout_U=0.1, name='rnn1')(input_data)
    # TODO: Add batch normalization 
    bn_rnn_1 = BatchNormalization(name='bn_rnn_1d')(simp_rnn_1)
    simp_rnn_2 = GRU(units, activation='relu',return_sequences=True, implementation=2,dropout_W=0.02, dropout_U=0.1, name='rnn2')(bn_rnn_1)
    # TODO: Add batch normalization 
    bn_rnn_2 = BatchNormalization(name='bn_rnn_2d')(simp_rnn_2)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn_2)    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model

def bidirectional_rnn_model(input_dim, units, output_dim=29):
    """ Build a bidirectional recurrent network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # TODO: Add bidirectional recurrent layer
    bidir_rnn = Bidirectional(GRU(units, return_sequences=True, activation='relu', name='bdrnn'), merge_mode='concat')(input_data)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bidir_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model
    

def final_model(input_dim, filters, kernel_size, conv_stride,

conv_border_mode, units, output_dim=29):

    # Main acoustic input

    input_data = Input(name='the_input', shape=(None, input_dim))

    # Add convolutional layer

    conv_1d = Conv1D(filters, kernel_size,

    strides=conv_stride,

    padding=conv_border_mode,

    activation='relu',

    name='conv1d')(input_data)

    # Add batch normalization

    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)

    # add initial rnn layr

    bd_rnn_0 = Bidirectional(GRU(units, activation='relu',

    return_sequences=True, implementation=2,

    dropout_W=0.02, dropout_U=0.1,

    name='rnn_layer1'), merge_mode='concat')(bn_cnn)

    bn_rnn_0 = BatchNormalization(name='bn_rnn_layer1')(bd_rnn_0)

    # add second layer

    bd_rnn_1 = Bidirectional(GRU(units, activation='relu',

    return_sequences=True, implementation=2,

    dropout_W=0.02, dropout_U=0.1,

    name='rnn_layer2'), merge_mode='concat')(bn_rnn_0)

    bn_rnn_1 = BatchNormalization(name='bn_rnn_layer2')(bd_rnn_1)

 

    # Add a TimeDistributed(Dense(output_dim)) layer

    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn_1)

    # Add softmax activation layer

    y_pred = Activation('softmax', name='softmax')(time_dense)

    # Specify the model

    model = Model(inputs=input_data, outputs=y_pred)

    # Specify model.output_length

    model = Model(inputs=input_data, outputs=y_pred)

    model.output_length = lambda x: cnn_output_length(

    x, kernel_size, conv_border_mode, conv_stride)

    print(model.summary())

    return model