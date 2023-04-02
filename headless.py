# importing libraries
import time
from jogo import Cascavel
from controlador import Controle
from brain import Brain
from scipy.optimize import differential_evolution

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

def fun(x, *data):
    h = x[:5*6].reshape((5, 6))
    w = x[5*6:].reshape((6, 3))
    window_x = data[0]
    window_y = data[1]
    # pygame = data[2]
    # game_window = data[3]
    controlador = Controle(Cascavel([window_x, window_y], 4, []), Brain(h=h, w=w))
    while True:
        controlador.move()
        if controlador.is_dead():
            return -controlador.get_score()

def optimize():
    args = [window_x, window_y]
    result = differential_evolution(fun, [(-100, 100) for n in range(5*6+6*3)], args=args, maxiter=300, disp=True, polish=False, updating='deferred', workers=-1)
    print(result)
    print(result.x)
    time.sleep(2)
    quit()
    
if __name__ == '__main__':
    optimize()
