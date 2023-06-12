import gym
from gym import spaces
from cycle_generator import create_path
from jogo import Cascavel
import numpy as np

class MyGameEnv(gym.Env):
    def __init__(self, dimensao, obstaculos = [], aleatorio = False):
        super(MyGameEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(4)  # Example for a binary action space: 0 and 1
        self.observation_space = spaces.MultiBinary(20,)
        self.dimensao = dimensao
        self.cascavel = Cascavel([dimensao, dimensao], obstaculos, aleatorio)
        caminho = create_path(dimensao, 0.001)
        self.path = np.zeros((dimensao, dimensao))
        self.directions = ['UP', 'DOWN', 'RIGHT', 'LEFT']
        for i, pos in enumerate(caminho):
            self.path[pos[0]][pos[1]] = i + 1
        self.frame_iteration = 0
        self.last_score = 0
    
    def step(self, action):
        self.frame_iteration += 1
        ax, ay = self.cascavel.snake_position
        pontos, done = self.cascavel.move(self.directions[action], True)
        dx, dy = self.cascavel.snake_position
        reward = 0
        info = {
            "pontos": pontos
        }
        if done or self.frame_iteration > 400*len(self.cascavel.snake_body):
            self.cascavel.game_over()
            obs = self.get_current_observation()
            done = True
            reward = -10
            return obs, reward, done, info
        if self.last_score is not pontos:
            self.frame_iteration = 0
            self.last_score = pontos
            reward = 10
        # current_size = self.dimensao * self.dimensao
        # if self.path[dx, dy] > self.path[ax, ay] and int(abs(current_size - self.path[dx][dy]) > len(self.cascavel.snake_body)):
        #     reward += 0.005
        # else:
        #     reward -= 0.005
        obs = self.get_current_observation()
        return obs, reward, done, info
    
    def reset(self):
        self.frame_iteration = 0
        self.last_score = 0
        self.cascavel.reset()
        obs = self.get_current_observation()
        return obs

    def __get_direction_on_array(self):
        direcao = self.cascavel.get_direction()
        if direcao == 'UP':
            return [1, 0, 0, 0]
        if direcao == 'DOWN':
            return [0, 1, 0, 0]
        if direcao == 'RIGHT':
            return [0, 0, 1, 0]
        if direcao == 'LEFT':
            return [0, 0, 0, 1]
        
    def __get_rel_food_position(self):
        on_down = (self.cascavel.snake_position[1] < self.cascavel.fruit_position[1])
        on_right = (self.cascavel.snake_position[0] < self.cascavel.fruit_position[0])
        retorno = []
        if on_down:
            retorno.append(0)
            retorno.append(1)
        else:
            retorno.append(1)
            retorno.append(0)
        
        if on_right:
            retorno.append(0)
            retorno.append(1)
        else:
            retorno.append(1)
            retorno.append(0)
        return retorno
    
    def __get_rel_cycle_position(self):
        x, y = self.cascavel.snake_position
        scores = [0, 0, 0, 0]
        snake_rel_size = [0, 0, 0, 0]
        
        if (x >= self.dimensao) or y >= self.dimensao:
            return np.concatenate([scores, snake_rel_size]) 
        
        current_size = self.dimensao * self.dimensao
        current_score = self.path[x][y]
        if x < self.dimensao - 1:
            scores[0] = int(self.path[x + 1][y] > current_score)
            snake_rel_size[0] = int(abs(current_size - self.path[x + 1][y]) > len(self.cascavel.snake_body))
        if x > 0:
            scores[1] = int(self.path[x - 1][y] > current_score)
            snake_rel_size[1] = int(abs(current_size - self.path[x - 1][y]) > len(self.cascavel.snake_body))
        if y > 0:
            scores[2] = int(self.path[x][y - 1] > current_score)
            snake_rel_size[2] = int(abs(current_size - self.path[x][y - 1]) > len(self.cascavel.snake_body))
        if y < self.dimensao - 1:
            scores[3] = int(self.path[x][y + 1] > current_score)
            snake_rel_size[3] = int(abs(current_size - self.path[x][y + 1]) > len(self.cascavel.snake_body))
    
        return np.concatenate([scores, snake_rel_size])
    
    def __get_possible_moves(self):
        possible_moves = []
        scale = 0

        new_position = self.cascavel.get_next_position_full_direction("UP")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)
        
        new_position = self.cascavel.get_next_position_full_direction("DOWN")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        new_position = self.cascavel.get_next_position_full_direction("RIGHT")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        new_position = self.cascavel.get_next_position_full_direction("LEFT")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        return possible_moves
    
    def render(self, mode='human', extra_param=None):
        # Render the environment to the screen
        # This can be as simple or complex as you want,
        # depending on how you want to visualize your environment.

        # Here, you'll need to implement the rendering logic of your game.
        self.cascavel.draw(extra_param[0], extra_param[1])

    def get_current_observation(self):
        # This method should return the current observation/state of your game.
        # This is just a placeholder and should be replaced with your game's logic.
        moves = self.__get_possible_moves()
        direction = self.__get_direction_on_array()
        food = self.__get_rel_food_position()
        cycle = self.__get_rel_cycle_position()
        return np.concatenate([moves, direction, food, cycle])
    
    def draw(self, pygame, game_window, show_cycle = False):
        self.cascavel.draw(pygame, game_window)