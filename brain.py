import numpy as np

from numba import jit

@jit(nopython=True)
def rapido(x, h1, w):

    hs = x@h1
    ys = hs@w
        
    return np.argmax(ys)

class Brain:
    def __init__(self, xsize = 5, hsize = 6, wsize = 3, h1=None, h2=None, w=None):
        self.xsize = xsize
        self.hsize = hsize
        self.wsize = wsize

        self.h1 = h1.astype(np.float32)
        self.w = w.astype(np.float32)

        if h1 is None:
            self.h1 = np.random.uniform(-1, 1, size=(xsize, hsize))


        if w is None:
            self.w = np.random.uniform(-1, 1, size=(hsize, wsize))

    def get_move(self, input):
        return rapido(input.reshape((1, 11)), self.h1, self.w)

