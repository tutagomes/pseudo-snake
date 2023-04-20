# importing libraries
import pygame
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

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 100, 0)
 
# Initialising pygame
pygame.init()
 
# Initialise game window
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()

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
    fps.tick(snake_speed)
    pygame.display.update()

drawAll()

x_size = 9
h_size = 12

# Define the callback function
def print_iteration_time(xk, convergence):
    global start_time
    elapsed_time = time.time() - start_time
    print(f"Iteration time: {elapsed_time:.2f} seconds")
    start_time = time.time()  # Update the start_time for the next iteration
    
def fun(x, *data):
    window_x = data[0]
    window_y = data[1]
    x_size = data[2]
    h_size = data[3]
    h1 = x[:x_size*h_size].reshape((x_size, h_size))
    h2 = x[x_size*h_size:(x_size*h_size + h_size*h_size)].reshape((h_size, h_size))
    w = x[(x_size*h_size + h_size*h_size):].reshape((h_size, 3))
    controlador = Controle(Cascavel([window_x, window_y], 4, []), Brain(h1=h1, h2=h2, w=w))
    while True:
        controlador.move()
        pygame.event.get()
        drawAll(controlador.cascavel)
        if controlador.is_dead():
            return -controlador.get_score()

args = [window_x, window_y, x_size, h_size]
result = differential_evolution(fun, [(-100, 100) for n in range(x_size*h_size+h_size*h_size+h_size*3)], args=args, maxiter=400, disp=True, polish=False, workers=1, updating='immediate', callback=print_iteration_time)


print(result)
print(result.x)
time.sleep(2)
pygame.quit()
quit()
