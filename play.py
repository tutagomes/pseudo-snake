
from stable_baselines3 import DQN
from gym_game_controller import MyGameEnv
import pygame
import time

snake_speed = 20
window_x = 500
window_y = 500
dimensao = 20

# Initialising pygame
pygame.init()
 
# Initialise game window
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

def draw_all(cobra = None):
    game_window.fill(pygame.Color(0, 0, 0))

    if cobra:
       cobra.draw(pygame, game_window, True)
 
    fps.tick(snake_speed)
    pygame.display.update()

env = MyGameEnv(20)  # No need to wrap the environment
model = DQN.load("./gym/best_model.zip")
obs = env.reset()
for i in range(1000):
    pygame.event.get()
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print(info['pontos'])
    if dones:
        print(info['pontos'])
        break
    # env.render()
    draw_all(env)
