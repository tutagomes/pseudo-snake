import numpy as np

# [10 11 12]
# [00 01 02]

# up 0
# down 1
# right 2
# left 3

def get_surroundings(X, direction):
    vertical = 1 if direction == "DOWN" else -1
    lateral = 1 if direction == "RIGHT" else -1
    head = np.where(X == 2)
    i = head[0]
    j = head[1]
    xs = X.shape

    s = np.zeros((2, 3))

    B = np.ones((xs[0] + 2, xs[1] + 2))

    for i in range(xs[0]):
        for j in range(xs[1]):
            B[i + 1][j + 1] = X[i][j]

    s[0, 0] = X[i - lateral, j]
    s[0, 2] = X[i + lateral, j]
    s[1, 0] = X[i - lateral, j + vertical]
    s[1, 0] = X[i, j + vertical]
    s[1, 0] = X[i + lateral, j + vertical]

    return s

def is_dillema(s):
    if s[1, 1] and not s[0, 0] and not s[0, 2]:
        return True
    
    if s[1, 0] and not s[0, 0]:
        return True
    
    if s[1, 2] and not s[0, 2]:
        return True
    
    return False


        