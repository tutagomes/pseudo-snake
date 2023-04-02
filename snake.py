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
    a = 80
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
        pygame.event.get()
        for cobra in cobrinhas:
            cobra.move()
            mortas += cobra.is_dead() if 1 else 0
        
        if mortas == len(cobrinhas):
            for cobra in cobrinhas:
                print(cobra.get_score())
            break

def fun(x, *data):
    h = x[:5*6].reshape((5, 6))
    w = x[5*6:].reshape((6, 3))
    window_x = data[0]
    window_y = data[1]
    controlador = Controle(Cascavel([window_x, window_y], 4, []), Brain(h=h, w=w))
    while True:
        pygame.event.get()
        drawAll(controlador)
        controlador.move()
        if controlador.is_dead():
            return -controlador.get_score()

# run()
# args = [window_x, window_y, pygame, game_window, obstaculos]
args = [window_x, window_y]
result = differential_evolution(fun, [(-100, 100) for n in range(5*6+6*3)], args=args, maxiter=300, disp=True, polish=False, updating='deferred')

print(result)
print(result.x)
time.sleep(2)
pygame.quit()
quit()
