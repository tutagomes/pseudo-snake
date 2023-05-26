import numpy as np

class Controle:
    def __init__(self, cascavel, brain):
        self.cascavel = cascavel
        self.brain = brain
        self.directions = ['LEFT', 'UP', 'RIGHT']
        self.movimentos_feitos = 0
        self.mov_since_food = 0
        self.last_score = 0

    def move(self):
        # array de 3 posicoes indicando perigo em quais direcoes
        movimentos = self.cascavel.get_possible_moves()
        # array de 4 posicoes indicando qual a direcao atual da cobra
        direcao = self.cascavel.get_direction_on_array()

        # array de 4 posicoes considerando a posicao da fruta em relacao a cabeca
        food_position = self.cascavel.get_rel_food_position()
        # head_position = [self.cascavel.snake_position[0]/self.cascavel.tabuleiro[0], self.cascavel.snake_position[1]/self.cascavel.tabuleiro[1]]
        # tail_position = [(self.cascavel.snake_body[len(self.cascavel.snake_body) - 1][0])/self.cascavel.tabuleiro[0], (self.cascavel.snake_body[len(self.cascavel.snake_body) - 1][1])/self.cascavel.tabuleiro[1]]
        move =  self.brain.get_move(np.array(movimentos + direcao + food_position, dtype=np.float32))
        self.cascavel.move(self.directions[move])
        self.movimentos_feitos = self.movimentos_feitos + 1
        self.mov_since_food = self.mov_since_food + 1
        if self.last_score == self.cascavel.frutas and self.mov_since_food > 120:
            self.cascavel.game_over()
        elif self.last_score < self.cascavel.frutas:
            self.last_score = self.cascavel.frutas

    def draw(self, pygame, game_window):
        self.cascavel.draw(pygame, game_window)

    def is_dead(self):
        return self.cascavel.is_game_over()
    
    def get_crom(self):
        return [self.brain.h, self.brain.w]

    def set_crom(self, h, w):
        self.brain.h = h
        self.brain.w = w
    
    def get_score(self):
        return self.cascavel.get_score()

    def set_cascavel(self, cascavel):
        self.cascavel  = cascavel
