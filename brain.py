import numpy as np

class Brain:
    def __init__(self, xsize = 5, hsize = 6, wsize = 3, h=None, w=None):
        self.xsize = xsize
        self.hsize = hsize
        self.wsize = wsize

        self.h = h
        self.w = w

        if h is None:
            self.h = np.random.uniform(-1, 1, size=(xsize, hsize))

        if w is None:
            self.w = np.random.uniform(-1, 1, size=(hsize, wsize))

    def get_move(self, input):
        x = np.matrix(input)

        hs = np.matmul(x, self.h)
        ys = np.matmul(hs, self.w)
        
        return np.argmax(ys)
