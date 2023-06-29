import gym
from gym import spaces
from cycle_generator import create_path
from jogo import Cascavel
import numpy as np
import collections

class MyGameEnv(gym.Env):
    def __init__(self, dimensao, obstaculos = [], aleatorio = False):
        super(MyGameEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(3)  # Example for a binary action space: 0 and 1
        self.observation_space = spaces.MultiBinary(20,)
        self.dimensao = dimensao
        self.cascavel = Cascavel([dimensao, dimensao], obstaculos, aleatorio)
        self.caminho = create_path(dimensao, 1)
        self.path = np.zeros((dimensao, dimensao))
        self.directions = ['UP', 'RIGHT', 'LEFT', 'DOWN']
        for i, pos in enumerate(self.caminho):
            self.path[int(pos[0])][int(pos[1])] = i + 1
        self.frame_iteration = 0
        self.last_score = 0
        self.visited = collections.deque(maxlen=2*self.dimensao)
        self.__calculate_lower_points()
    
    def step(self, action):
        self.frame_iteration += 1
        ax, ay = self.cascavel.snake_position
        pontos, done = self.cascavel.move(self.directions[action])
        dx, dy = self.cascavel.snake_position
        reward = 0
        info = {
            "pontos": pontos,
            "hx": self.cascavel.snake_position[0],
            "hy": self.cascavel.snake_position[1],
            "axy": str(ax) + "-" + str(ay),
            "dxy": str(dx) + "-" + str(dy),
            "body": str(self.cascavel.snake_body),
            # "body_points": list(map(lambda x: self.path[x[0]][x[1]], self.cascavel.snake_body)),
            "done": done,
            # "greater": self.path[ax][ay] < self.path[dx][dy],
            # "can_move": self.__can_i_move_on_cycle([ax, ay], [dx, dy]),
            # "b": self.path[ax][ay],
            # "a": self.path[dx][dy],
            "lower": self.points_lower,
            "lowest": self.points_lowest,

        }
        if done:
            self.cascavel.game_over()
            obs = self.get_current_observation()
            reward = -100
            return obs, reward, done, info
        if self.frame_iteration > 1.5*self.dimensao*self.dimensao:
            self.cascavel.game_over()
            obs = self.get_current_observation()
            reward = -100
            return obs, reward, done, info
        
        self.__calculate_lower_points()
        info["lower"] = self.points_lower
        info["lowest"] = self.points_lowest

        fx, fy = self.cascavel.fruit_position
        if self.last_score is not pontos:
            self.frame_iteration = 0
            self.last_score = pontos
            reward = 100
        else:
            reward -= 1
        # elif self.path[ax][ay] < self.path[fx][fy] < self.path[dx][dy]:
        #     reward -= 50000
        if not self.__can_i_move_on_cycle([ax, ay], [dx, dy]):
            reward -= 1
        elif ([dx, dy] in list(self.visited)):
            reward -=10
        else:
            reward +=1
        obs = self.get_current_observation()
        self.visited.append([dx, dy])
        return obs, reward, done, info
    
    def reset(self):
        self.frame_iteration = 0
        self.last_score = 0
        self.cascavel.reset()
        obs = self.get_current_observation()
        self.__calculate_lower_points()
        return obs

    def __find_smallest_greater(self, array, target):
        closest_greater = np.max(array)
        for num in array:
            if target < num < closest_greater:
                closest_greater = num
        return closest_greater
    
    def __calculate_lower_points(self):
        x, y = self.cascavel.snake_position
        current_score = self.path[x][y]
        positions_scores = []
        for idx, pos in enumerate(self.cascavel.snake_body[:-1]):
            if pos[0] > self.dimensao or pos[1] > self.dimensao:
                continue
            positions_scores.append(self.path[pos[0]][pos[1]])
        self.points_lower = self.__find_smallest_greater(positions_scores, current_score)
        self.points_lowest = np.min(positions_scores)

    def __get_lower_points(self):
        return [self.points_lower, self.points_lowest]
    
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
        retorno = []
        # On Top or Bottom
        if (self.cascavel.snake_position[1] < self.cascavel.fruit_position[1]):
            retorno.append(0)
            retorno.append(1)
        elif (self.cascavel.snake_position[1] > self.cascavel.fruit_position[1]):
            retorno.append(1)
            retorno.append(0)
        else:
            retorno.append(0)
            retorno.append(0)
        
        # On Right or On Left
        if (self.cascavel.snake_position[0] < self.cascavel.fruit_position[0]):
            retorno.append(0)
            retorno.append(1)
        elif (self.cascavel.snake_position[0] > self.cascavel.fruit_position[0]):
            retorno.append(1)
            retorno.append(0)
        else:
            retorno.append(0)
            retorno.append(0)

        is_greater = [0, 0, 0, 0]

        x, y = self.cascavel.snake_position
        fx, fy = self.cascavel.fruit_position
        # se eu for pra cima, a fruta está na casa maior?
        if x - 1 >= 0 and y < self.dimensao and x < self.dimensao:
            is_greater[0] = int(self.path[fx][fy] > self.path[x - 1][y])
        if y - 1 >= 0 and y < self.dimensao and x < self.dimensao:
            # e pra esquerda?
            is_greater[1] = int(self.path[fx][fy] > self.path[x][y - 1])
        if y + 1 < self.dimensao and y < self.dimensao and x < self.dimensao:
            # e pra direita?
            is_greater[2] = int(self.path[fx][fy] > self.path[x][y + 1])
        if x + 1 < self.dimensao and y < self.dimensao and x < self.dimensao:
            # e para baixo?
            is_greater[3] = int(self.path[fx][fy] > self.path[x + 1][y])

        return np.concatenate([retorno, is_greater])
    
    def __can_i_move_on_cycle(self, actual, next):
        current_score = -float('inf')
        future = -float('inf')
        if actual[0] >= 0 and actual[1] >= 0 and actual[0] < self.dimensao and actual[1] < self.dimensao:
            current_score = self.path[actual[0]][actual[1]]
        if next[0] >= 0 and next[1] >= 0 and next[0] < self.dimensao and next[1] < self.dimensao:
            future = self.path[next[0]][next[1]]
        current_size = self.dimensao * self.dimensao
        lower, lowest = self.__get_lower_points()
        
        # Se eu for para essa casa
        # retorno = abs(future - lowest) > len(self.cascavel.snake_body) or True
        # retorno = (future < lower) and retorno
        retorno = (future > current_score)
        # eu não visitei essa casa recentemente?
        # retorno = retorno and (next not in list(self.visited))
        retorno = (current_score == current_size and future == 1) or retorno
        return retorno
        
    def __get_rel_cycle_position(self):
        x, y = self.cascavel.snake_position
        scores = [0, 0, 0, 0]
        scores2 = [0, 0, 0, 0]
        if x < self.dimensao - 1:
            scores[0] = int(self.__can_i_move_on_cycle([x, y], [x + 1, y]))
            scores2[0] = ([x + 1, y] not in list(self.visited))
        if x > 0:
            scores[1] = int(self.__can_i_move_on_cycle([x, y], [x - 1, y]))
            scores2[1] = ([x - 1, y] not in list(self.visited))
        if y > 0:
            scores[2] = int(self.__can_i_move_on_cycle([x, y], [x, y - 1]))
            scores2[2] = ([x, y - 1] not in list(self.visited))
        if y < self.dimensao - 1:
            scores[3] = int(self.__can_i_move_on_cycle([x, y], [x, y + 1]))
            scores2[3] = ([x, y + 1] not in list(self.visited))
        return np.concatenate([scores, scores2])

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
        # direction = self.__get_direction_on_array()
        moves = self.__get_possible_moves()
        food = self.__get_rel_food_position()
        cycle = self.__get_rel_cycle_position()
        return np.concatenate([moves, food, cycle])
    
    def draw(self, pygame, game_window, show_cycle = False):
        window_width, window_height = game_window.get_size()
        ppp = min(window_width / self.dimensao, window_height / self.dimensao)
        font = pygame.font.SysFont('arial', 12)
        self.cascavel.draw(pygame, game_window)
        x, y = self.cascavel.snake_position
        for i in range(len(self.path)):
            for j in range(len(self.path[i])):
                color = (255, 255, 255)
                if self.__can_i_move_on_cycle([x, y], [i, j]):
                    color = (0, 255, 0)
                text = font.render(str(int(self.path[i][j])), True, color)
                position = [i * ppp, j * ppp]
                game_window.blit(text, position)
