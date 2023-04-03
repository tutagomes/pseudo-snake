# importing libraries
import pygame
import time
import random
from jogo import Cascavel
from controlador import Controle
from brain import Brain


import random as rd
import numpy as np
import matplotlib.pyplot as plt

snake_speed = 120
# Com 126000 pontos
# pesos = [ -9.02596297 , -3.910032  ,  79.63849792 ,-38.50798272 ,  7.15406837, 64.91693806,  -3.32713247,  54.66298791, -64.48630107,  23.57019835, 89.77569489, -62.28798434,  11.52000912, -75.23377896,  -5.3398137, -23.9569645  , 78.88517599, -20.7227467 ,  46.62432024,  35.86544946, -5.96356857, -39.02085701 , 51.55302299,  28.87657014,  75.81762479, -41.88824131, -18.37081914,  -5.06155555, -55.35572236 , 12.06815799, -7.39673757, -44.92409332, -98.34428864 , 34.41792751 , 77.24112405, -7.3575189 ,  23.96999571, -13.97686508 , -1.14516561 , 26.30196756, -0.37518103  ,81.31812607 ,-96.7055934 , -46.69607122, -63.07767752,  71.23451461 , 19.01288745, -27.77662086]
# com 72000 pontos
pesos = [-94.13771095,39.34485121,-47.69777225,-44.09732132,9.06046366,-7.49371472,-43.7482685,87.27102411,47.80991292,-28.84095565,-82.28623149,-21.98201387,53.9726049,-81.40207767,-84.65540858,-42.60255322,88.10286247,-81.0309745,-8.69813449,14.8995569,54.17048622,-51.98544048,-42.83357319,-72.44417211,46.02416725,35.92350108,-41.15791124,66.23940183,86.31857642,-56.77229075,5.2640029,48.15299837,79.53482375,-61.6522168,74.09006052,-72.35777415,28.46527127,28.12963019,-67.16051334,20.08608107,1.26279175,-38.07865053,22.48804006,79.1282633,93.85033063,31.76362957,-27.25964994,7.92855839]

import random as rd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution

snake_speed = 100

directions = ['RIGHT', 'UP', 'LEFT']    
# obstaculos = [[10, 10], [50, 50], [50, 60], [50, 70], [50, 80]]
obstaculos = []
# Window size
window_x = 500
window_y = 500
# window_x = 1000
# window_y = 1000
# pixels por ponto
# variável que auxilia no desenho das cobras, organização do tabuleiro, limites e obstaculos
ppp = 10
n_cobrinhas = 50

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 100, 0)
blue = pygame.Color(0, 0, 255)
 
# Initialising pygame
pygame.init()
 
# Initialise game window
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
 
# Main Function
cobrinhas = []
# for i in range(0, n_cobrinhas):
#     controlador = Controle(Cascavel([window_x, window_y], pygame, game_window, ppp, obstaculos), Brain())
#     cobrinhas.append(controlador)

pygame.display.update()

def drawAll(cobra = None):
    game_window.fill(black)
    # Desenhando as margens do mapa
    pygame.draw.rect(game_window, green, pygame.Rect(0, 0, window_x, ppp))
    pygame.draw.rect(game_window, green, pygame.Rect(0, window_y - ppp, window_x, ppp))
    pygame.draw.rect(game_window, green, pygame.Rect(0, 0, ppp, window_y))
    pygame.draw.rect(game_window, green, pygame.Rect(window_x - ppp, 0, ppp, window_y))

    for obs in obstaculos:
        pygame.draw.rect(game_window, white, pygame.Rect(obs[0], obs[1], ppp, ppp))

    if cobra:
       cobra.draw(pygame, game_window)

    for cobra in cobrinhas:
        cobra.draw(pygame, game_window)
 
    fps.tick(snake_speed)
    pygame.display.update()

drawAll()
def run():
    while True:
        mortas = 0
        for event in pygame.event.get():
            a = 37
            # print(event)
        for cobra in cobrinhas:
            cobra.move()
            mortas += cobra.is_dead() if 1 else 0
        
        if mortas == len(cobrinhas):
            for cobra in cobrinhas:
                print(cobra.get_score())
            break

h = np.array(pesos[:5*6]).reshape((5, 6))
w = np.array(pesos[5*6:]).reshape((6, 3))
controlador = Controle(Cascavel([window_x, window_y], ppp, []), Brain(h=h, w=w))
while True:
    pygame.event.get()
    drawAll(controlador)
    controlador.move()
    if controlador.is_dead():
        print(controlador.get_score())
        break
# print(result)
# print(result.x)
time.sleep(2)
pygame.quit()
quit()
