# importing libraries
import time
from jogo import Cascavel
from controlador import Controle
from brain import Brain
from scipy.optimize import differential_evolution
import numpy as np

snake_speed = 1000

directions = ['RIGHT', 'UP', 'LEFT']    
# obstaculos = [[10, 10], [50, 50], [50, 60], [50, 70], [50, 80]]
obstaculos = []
# Window size
window_x = 600
window_y = 600
# window_x = 1000
# window_y = 1000
# pixels por ponto
# variável que auxilia no desenho das cobras, organização do tabuleiro, limites e obstaculos
ppp = 4
n_cobrinhas = 50

x_size = 9
h_size = 12

def fun(x, *data):
    window_x = data[0]
    window_y = data[1]
    x_size = data[2]
    h_size = data[3]
    h = x[:x_size*h_size].reshape((x_size, h_size))
    w = x[x_size*h_size:].reshape((h_size, 3))
    # pygame = data[2]
    # game_window = data[3]
    controlador = Controle(Cascavel([window_x, window_y], 4, []), Brain(h=h, w=w))
    while True:
        controlador.move()
        if controlador.is_dead():
            return -controlador.get_score()

def optimize():
    args = [window_x, window_y, x_size, h_size]
    result = differential_evolution(fun, [(-100, 100) for n in range(x_size*h_size+h_size*3)], args=args, maxiter=50, disp=True, polish=False, updating='deferred', workers=-1)
    print(result)
    print(result.x)
    with open(str(((-1)*result.fun)) +'.csv', 'w') as my_file:
        np.savetxt(my_file, result.x)
    time.sleep(2)
    quit()
    
if __name__ == '__main__':
    optimize()
