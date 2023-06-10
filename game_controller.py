from cycle_generator import create_path
from drawpath import draw_path
from jogo import Cascavel
import numpy as np
import logging
class Controller:

    def __init__(self, dimensao, obstaculos, aleatorio = False):
        self.dimensao = dimensao
        self.cascavel = Cascavel([dimensao, dimensao], obstaculos, aleatorio)
        logging.debug("Criando Path")
        caminho = create_path(dimensao, 0.001)
        self.path = np.zeros((dimensao, dimensao))
        self.directions = ['UP', 'DOWN', 'RIGHT', 'LEFT']
        for i, pos in enumerate(caminho):
            self.path[pos[0]][pos[1]] = i + 1
        logging.debug("Path Criado")
        self.frame_iteration = 0
        self.last_score = 0
        # draw_path(dimensao, caminho)
    # retorna o array da direcao em que a cobra esta indo
    
    def get_direction_on_array(self):
        direcao = self.cascavel.get_direction()
        if direcao == 'UP':
            return [1, 0, 0, 0]
        if direcao == 'DOWN':
            return [0, 1, 0, 0]
        if direcao == 'RIGHT':
            return [0, 0, 1, 0]
        if direcao == 'LEFT':
            return [0, 0, 0, 1]
    
    def reset(self):
        self.frame_iteration = 0
        self.last_score = 0
        self.cascavel.reset()
        
    # retorna um array de posicionamento da fruta em relacao ao corpo

    def get_rel_food_position(self):
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
    
    # retorna um array em relacao ao ciclo hamiltoniano utilizado

    def get_rel_cycle_position(self):
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

    # retorna um array de movimentacoes possiveis - left, up or right

    def get_possible_moves(self):
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
    
    def step(self, action):
        self.frame_iteration += 1
        ax, ay = self.cascavel.snake_position
        pontos, done = self.cascavel.move(self.directions[action], True)
        dx, dy = self.cascavel.snake_position
        reward = 0
        if done or self.frame_iteration > 100*len(self.cascavel.snake_body):
            self.cascavel.game_over()
            done = True
            reward = -10
            return [reward, done, pontos]
        if self.last_score is not pontos:
            self.frame_iteration = 0
            self.last_score = pontos
            reward = 10
            print("peguei")
        current_size = self.dimensao * self.dimensao
        if self.path[dx, dy] > self.path[ax, ay] and int(abs(current_size - self.path[dx][dy]) > len(self.cascavel.snake_body)):
            reward += 0.1
        else:
            reward -= 0.1
        return [reward, done, pontos]        
    
    def get_state_size(self):
        return 19
    
    def get_state(self):
        # tamanho 19
        moves = self.get_possible_moves()
        direction = self.get_direction_on_array()
        food = self.get_rel_food_position()
        cycle = self.get_rel_cycle_position()
        return np.concatenate([moves, direction, food, cycle])
    
    def draw(self, pygame, game_window, show_cycle = False):
        # self.font = pygame.font.Font(None, 10)
        # TEXT_COLOR = (255, 255, 255)
        # score_font = pygame.font.SysFont('times new roman', 10)
        
        # window_width, window_height = game_window.get_size()
        # ppp = min(window_width / self.dimensao, window_height / self.dimensao)
        # for i in range(self.dimensao):
        #     for j in range(self.dimensao):
        #         # Create a Surface with the text
        #         score_surface = score_font.render(str(int(self.path[i][j])), True, 'white')
        #         # text_surface = self.font.render(, True, TEXT_COLOR)
        #         # Draw the text on the screen at the given position
        #         score_rect = score_surface.get_rect()
        #         # game_window.blit(score_surface, score_rect)
        #         game_window.blit(score_surface, (i * ppp, j * ppp))
        #     # creating font object score_font
        # # create the display surface object
        # # score_surface
        # for y in range(self.dimensao):
        #     for x in range(self.dimensao):
        #         rect = pygame.Rect(x*(ppp + 1), y*(ppp + 1), ppp, ppp)
        #         pygame.draw.rect(game_window, 'white', rect)
        
        # create a rectangular object for the
        # text surface object
        

        # displaying text
        
        self.cascavel.draw(pygame, game_window)