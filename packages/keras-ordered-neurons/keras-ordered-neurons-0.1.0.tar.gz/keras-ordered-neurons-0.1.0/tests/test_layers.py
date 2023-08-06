import os
import tempfile
from unittest import TestCase
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Embedding, Bidirectional, Dense
from keras_ordered_neurons import ONLSTM


class TestONLSTM(TestCase):

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            model = Sequential()
            model.add(ONLSTM(units=13, chunk_size=5, input_shape=(None, 100)))

    def test_fit_classification(self):
        model = Sequential()
        model.add(Embedding(input_shape=(None,), input_dim=10, output_dim=100))
        model.add(Bidirectional(ONLSTM(units=50, chunk_size=5, dropout=0.1, use_bias=False, return_sequences=True)))
        model.add(Bidirectional(ONLSTM(units=50, chunk_size=5, recurrent_dropout=0.1, return_sequences=True)))
        model.add(Bidirectional(ONLSTM(units=50, chunk_size=5, unit_forget_bias=False)))
        model.add(Dense(units=2, activation='softmax'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

        model_path = os.path.join(tempfile.gettempdir(), 'test_on_lstm_%f.h5' % np.random.random())
        model.save(model_path)
        model = load_model(model_path, custom_objects={'ONLSTM': ONLSTM})

        data_size, seq_len = 10000, 17
        x = np.random.randint(0, 10, (data_size, seq_len))
        y = [0] * data_size
        for i in range(data_size):
            if 3 in x[i].tolist() and 7 in x[i].tolist():
                y[i] = 1
        y = np.array(y)
        model.summary()
        model.fit(x, y, epochs=10)

        model_path = os.path.join(tempfile.gettempdir(), 'test_on_lstm_%f.h5' % np.random.random())
        model.save(model_path)
        model = load_model(model_path, custom_objects={'ONLSTM': ONLSTM})

        predicted = model.predict(x).argmax(axis=-1)
        self.assertLess(np.sum(np.abs(y - predicted)), data_size // 100)
