from dqn import DQN
from game_controller import Controller
import numpy as np
import pygame

from helper import plot

snake_speed = 100
window_x = 1000
window_y = 1000
dimensao = 20

# Initialising pygame
# pygame.init()
 
# Initialise game window
# game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
# fps = pygame.time.Clock()

# def draw_all(cobra = None):
#     game_window.fill(pygame.Color(0, 0, 0))

#     if cobra:
#        cobra.draw(pygame, game_window, True)
 
#     fps.tick(snake_speed)
#     pygame.display.update()

controller = Controller(dimensao, [])

dqn = DQN(controller.get_state_size(), 3)  # Assuming 3 possible actions: up, left, right
batch_size = 1000
scores = []
mean_scores = []

for episode in range(10000):  # Play 10000 games
    controller.reset()
    state = controller.get_state()
    done = False
    score = 0
    while not done:
        # pygame.event.get()
        action = dqn.act(state)
        reward, done = controller.step(action)
        score = reward
        next_state = controller.get_state()
        dqn.remember(state, action, reward, next_state, done)
        state = next_state
        # draw_all(controller)
    if len(dqn.memory) > batch_size:
        dqn.replay(batch_size)
    if len(scores) and score > np.max(scores):
        # termos um recorde!
        dqn.save_model(file_path='./models/model' + str(score) + '.torch')
    scores.append(score)
    mean_scores.append(np.mean(scores))
    plot(scores, mean_scores)
    print('Jogo', episode, 'Score', score, 'Record:', np.max(scores))

# pygame.quit()
quit()