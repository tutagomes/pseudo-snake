import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import torch
from numba import jit

@jit(nopython=True)
def rapido(x, h1, h2, w):

    hs = x@h1
    hs2 = hs@h2
    ys = hs2@w
        
    return np.argmax(ys)

class Brain:
    def __init__(self, xsize = 5, hsize = 6, wsize = 3, h1=None, h2=None, w=None):
        self.xsize = xsize
        self.hsize = hsize
        self.wsize = wsize

        self.h1 = h1.astype(np.float32)
        self.h2 = h2.astype(np.float32)
        self.w = w.astype(np.float32)

        if h1 is None:
            self.h1 = np.random.uniform(-1, 1, size=(xsize, hsize))

        if h2 is None:
            self.h2 = np.random.uniform(-1, 1, size=(hsize, hsize))

        if w is None:
            self.w = np.random.uniform(-1, 1, size=(hsize, wsize))



    def get_move(self, input):
        return rapido(input.reshape((1, 9)), self.h1, self.h2, self.w)


class Brain2(Brain):
    def __init__(self, xsize=9, hsize=12, wsize=3, h1=None, h2 = None, w=None):
        super().__init__(xsize, hsize, wsize, h1, h2, w)
        self.model = keras.Sequential([
            layers.Dense(hsize, activation="relu", input_shape=(xsize,), use_bias=False),
            layers.Dense(hsize, activation="relu", use_bias=False),
            layers.Dense(wsize, activation="relu", use_bias=False)
        ])
        self.model.set_weights([h1, h2, w])
    @tf.function(input_signature=[tf.TensorSpec(shape=[9], dtype=tf.float32)])
    def get_move(self, input):
        input = tf.expand_dims(input, axis=0)
        prediction = self.model(input, training=False)
        return tf.argmax(prediction, axis=1)[0]
        # retorno = self.model.predict([input])
        # return np.argmax(retorno)

class Brain3(Brain):

    def __init__(self, xsize=9, hsize=12, wsize=3, h1=None, h2 = None, w=None):
        super().__init__(xsize, hsize, wsize, h1, h2, w)
        self.h1 = torch.from_numpy(h1.astype(np.float32))
        self.h2 = torch.from_numpy(h2.astype(np.float32))
        self.w = torch.from_numpy(w.astype(np.float32))

    def matrix_multiplication(A, B):
        C_tensor = torch.matmul(A, B)
        return C_tensor.numpy()

    def get_move(self, input):
        x = np.matrix(input).astype(np.float32)
        x = torch.from_numpy(x)
        hs = torch.matmul(x, self.h1)
        hs2 = torch.matmul(hs, self.h2)
        ys = torch.matmul(hs2, self.w).numpy()
        
        return np.argmax(ys)