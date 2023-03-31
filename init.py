# importing libraries
import pygame
import time
import random
from jogo import Cascavel

import random as rd
import numpy as np
import matplotlib.pyplot as plt

snake_speed = 120 

directions = ['RIGHT', 'UP', 'LEFT']
obstaculos = [[10, 10], [50, 50], [50, 60], [50, 70], [50, 80]]

# Window size
window_x = 720
window_y = 480
# window_x = 1000
# window_y = 1000
# pixels por ponto
# variável que auxilia no desenho das cobras, organização do tabuleiro, limites e obstaculos
ppp = 10
n_cobrinhas = 40

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
for i in range(0, n_cobrinhas):
    cobrinhas.append(Cascavel([window_x, window_y], pygame, game_window, ppp, obstaculos))

pygame.display.update()

def drawAll():
    game_window.fill(black)
    # Desenhando as margens do mapa
    pygame.draw.rect(game_window, green, pygame.Rect(0, 0, window_x, ppp))
    pygame.draw.rect(game_window, green, pygame.Rect(0, window_y - ppp, window_x, ppp))
    pygame.draw.rect(game_window, green, pygame.Rect(0, 0, ppp, window_y))
    pygame.draw.rect(game_window, green, pygame.Rect(window_x - ppp, 0, ppp, window_y))

    for obs in obstaculos:
        pygame.draw.rect(game_window, white, pygame.Rect(obs[0], obs[1], ppp, ppp))

    for cobra in cobrinhas:
        cobra.draw()
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
            moves = cobra.possible_moves()
            # print(moves)
            if len(moves) != 0:
                dir = moves[random.randint(0, len(moves) - 1)]
                cobra.move(dir)
            mortas += cobra.isGameOver() if 1 else 0
        drawAll()
        if mortas == len(cobrinhas):
            for cobra in cobrinhas:
                print(cobra.getScore())



time.sleep(2)
pygame.quit()
quit()
