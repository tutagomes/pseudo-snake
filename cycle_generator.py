import random
import math
import random
import os
import numpy as np

def backbite(n, path):
    itemp = math.floor(random.random() * 2)
    nsq = n * n
    if itemp == 0:
        x, y = path[0]
        xedge = (x == 0) or (x == n - 1)
        yedge = (y == 0) or (y == n - 1)
        if xedge and yedge:
            add_edge = math.floor(random.random() * 3) - 2
        elif xedge or yedge:
            add_edge = math.floor(random.random() * 3) - 1
        else:
            add_edge = math.floor(random.random() * 3)
        success = (add_edge >= 0)
        iedge = 0
        i = 3
        while iedge <= add_edge:
            dx = abs(x - path[i][0])
            dy = abs(y - path[i][1])
            if dx + dy == 1:
                if iedge == add_edge:
                    jlim = (i - 1) // 2
                    for j in range(jlim):
                        path[j], path[i - 1 - j] = path[i - 1 - j], path[j]
                iedge += 1
            i += max(2, dx + dy - 1)
    else:
        x, y = path[nsq - 1]
        xedge = (x == 0) or (x == n - 1)
        yedge = (y == 0) or (y == n - 1)
        if xedge and yedge:
            add_edge = math.floor(random.random() * 3) - 2
        elif xedge or yedge:
            add_edge = math.floor(random.random() * 3) - 1
        else:
            add_edge = math.floor(random.random() * 3)
        success = (add_edge >= 0)
        iedge = 0
        i = nsq - 4
        while iedge <= add_edge:
            dx = abs(x - path[i][0])
            dy = abs(y - path[i][1])
            if dx + dy == 1:
                if iedge == add_edge:
                    jlim = (nsq - 1 - i - 1) // 2
                    for j in range(jlim):
                        path[nsq - 1 - j], path[i + 1 + j] = path[i + 1 + j], path[nsq - 1 - j]
                iedge += 1
            i -= max(2, dx + dy - 1)
    return success


def generate_hamiltonian_path(n, q):
    path = [[0, 0] for _ in range(n * n)]
    for i in range(n):
        if i % 2 == 0:
            for j in range(n):
                path[i * n + j] = [i, j]
        else:
            for j in range(n):
                path[i * n + j] = [i, n - j - 1]
    nsuccess = 0
    nattempts = 0
    nmoves = q * 10.0 * n * n * math.pow(math.log(2.0 + n), 2)
    while nsuccess < nmoves:
        success = backbite(n, path)
        if success:
            nsuccess += 1
        nattempts += 1
    for _ in range(nattempts):
        success = backbite(n, path)
    return path

def generate_hamiltonian_circuit(n, q):
    path = generate_hamiltonian_path(n, q)
    nsq = n * n
    min_dist = 1 + (n % 2)
    while abs(path[nsq - 1][0] - path[0][0]) + abs(path[nsq - 1][1] - path[0][1]) != min_dist:
        success = backbite(n, path)
    return path

def create_path(n = 10, q = 1.0, dir = './cycles'):
    os.makedirs(dir, exist_ok=True)
    file_path = dir + '/' + str(n) + '_' + str(q)
    if os.path.exists(file_path):
        path = np.loadtxt(file_path)
        return path
    path = generate_hamiltonian_circuit(n, q)
    np.savetxt(file_path, path)
    return path

if __name__ == '__main__':
    print(create_path(40))