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
        self.directions = ['LEFT', 'UP', 'RIGHT']
        for i, pos in enumerate(caminho):
            self.path[pos[0]][pos[1]] = i + 1
        logging.debug("Path Criado")
        draw_path(dimensao, caminho)
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
        scores = [-1, -1, -1, -1]
        snake_rel_size = [0, 0, 0, 0]
        
        if (x >= self.dimensao) or y >= self.dimensao:
            return np.concatenate([scores, snake_rel_size]) 
        
        current_size = self.dimensao * self.dimensao
        current_score = self.path[x][y]
        if x < self.dimensao - 1:
            scores[0] = self.path[x + 1][y]/current_score
            snake_rel_size[0] = int((current_size - self.path[x + 1][y]) > len(self.cascavel.snake_body))
        if x > 0:
            scores[1] = self.path[x - 1][y]/current_score
            snake_rel_size[1] = int((current_size - self.path[x - 1][y]) > len(self.cascavel.snake_body))
        if y > 0:
            scores[2] = self.path[x][y - 1]/current_score
            snake_rel_size[2] = int((current_size - self.path[x][y - 1]) > len(self.cascavel.snake_body))
        if y < self.dimensao - 1:
            scores[3] = self.path[x][y + 1]/current_score
            snake_rel_size[3] = int((current_size - self.path[x][y + 1]) > len(self.cascavel.snake_body))
        return np.concatenate([scores, snake_rel_size])

    # retorna um array de movimentacoes possiveis - left, up or right

    def get_possible_moves(self):
        possible_moves = []
        scale = 0

        new_position = self.cascavel.get_next_position("LEFT")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)
        
        new_position = self.cascavel.get_next_position("UP")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        new_position = self.cascavel.get_next_position("RIGHT")
        if self.cascavel.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        return possible_moves
    
    def step(self, action):
        return self.cascavel.move(self.directions[action])
    
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
        # window_width, window_height = game_window.get_size()
        # ppp = min(window_width / self.dimensao, window_height / self.dimensao)
        # for i in range(self.dimensao):
        #     for j in range(self.dimensao):
        #         # Create a Surface with the text
        #         text_surface = self.font.render(str(self.path[i][j]), True, TEXT_COLOR)
        #         # Draw the text on the screen at the given position
        #         game_window.blit(text_surface, (i * ppp, j * ppp))
        self.cascavel.draw(pygame, game_window)