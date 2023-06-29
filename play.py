
from stable_baselines3 import DQN, PPO
from gym_game_controller import MyGameEnv
import pygame
import time
import csv
snake_speed = 10
window_x = 1000
window_y = 1000

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

env = MyGameEnv(20, [], True)  # No need to wrap the environment
model = DQN.load("./dqn_mlp.zip")
# model = PPO.load('./ppo_mlp.zip')
obs = env.reset()
dones = False
information = []
while not dones:
# for i in range(25):
    pygame.event.get()
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    # print("Can move:" + str(info['can_move']) + " - reward: " + str(rewards) + " Antes: " + str(info["b"]) + " Depois: " + str(info["a"]))
    information.append(info)
    if dones:
        print(info['pontos'])
        print(info['done'])
        print(info['hx'])
        print(info['hy'])
        print(info['body'])
        break
    # env.render()
    draw_all(env)

with open("results.csv", "w", newline="") as fp:
    # Create a writer object
    writer = csv.DictWriter(fp, fieldnames=information[0].keys())

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in information:
        writer.writerow(row)
    print('Done writing dict to a csv file')
