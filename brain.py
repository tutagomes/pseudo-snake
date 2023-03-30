import numpy as np

xsize = 4
hsize = 6
wsize = 3

h = np.random.rand(xsize, hsize)
w = np.random.rand(hsize, wsize)

print(h)
print(w)

def move(x):
    x = np.matrix(x)

    hs = np.matmul(x, h)
    ys = np.matmul(hs, w)
    
    y = np.zeros(wsize)
    y[np.argmax(ys)] = 1

    return y

x = [1, 1, 1, 0.5]

print(move(x))