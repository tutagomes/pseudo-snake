
import random
import numpy as np

class Cascavel:

    # Onde ppp é uma variável de controle (pixels por ponto) que determina uma melhor conversão entre o que é mostrado na tela e o que é o jogo real
    # Por exemplo, para calcular o x_max, tem-se a largura total da tela menos o ppp para impedir que a cobrinha já comece na beirada do tabuleiro

    def __init__(self, tabuleiro, pygame, game_window, ppp, obstaculos):
        self.pygame = pygame
        self.game_window = game_window
        self.obstaculos = obstaculos
        self.ppp = ppp
        # defining snake default position
        x_max = tabuleiro[0] - ppp
        y_max = tabuleiro[1] - ppp
        self.snake_position = [random.randint(1, x_max/ppp)*ppp, random.randint(1, y_max/ppp)*ppp]
        self.snake_body = [[self.snake_position[0], self.snake_position[1]],
                [self.snake_position[0] + ppp, self.snake_position[1]],
                [self.snake_position[0] + 2*ppp, self.snake_position[1]],
                [self.snake_position[0] + 3*ppp, self.snake_position[1]],
                [self.snake_position[0] + 4*ppp, self.snake_position[1]]
            ]

        # fruit position
        self.fruit_position = [random.randrange(1, ((tabuleiro[0] - 2*ppp)//ppp)) * ppp,
                        random.randrange(1, ((tabuleiro[1] - 2*ppp)//ppp)) * ppp]
        self.tabuleiro = tabuleiro
        self.fruit_spawn = True
        self.gameOver = False
        # setting default snake direction towards
        # right
        self.direction = 'RIGHT'
        self.change_to = self.direction
    
        # initial score
        self.score = 0
        self.cobra = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        # self.fruta = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.fruta = self.cobra
        self.moves = 0
    # displaying Score function

    def get_direction(self):
        if self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] < self.snake_body[1][1]: # Estou subindo
           return 'UP'
        elif self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] > self.snake_body[1][1]: # Estou descendo
            return 'DOWN'
        elif self.snake_body[0][0] > self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra direita
            return 'RIGHT'
        elif self.snake_body[0][0] < self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra esquerda
            return 'LEFT'

    def get_possible_moves(self):
        possible_moves = []
        scale = 10
        def is_valid_position(position):
            if (scale < position[0] < (self.tabuleiro[0]) - scale) and (scale < position[1] < (self.tabuleiro[1]) - scale ) and (position not in self.snake_body) and (position not in self.obstaculos):
                return True
            return False

        new_position = self.get_next_position("LEFT")
        if is_valid_position(new_position):
            possible_moves.append(1)
        else:
            possible_moves.append(0)
        
        new_position = self.get_next_position("UP")
        if is_valid_position(new_position):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        new_position = self.get_next_position("RIGHT")
        if is_valid_position(new_position):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        if np.sum(possible_moves) == 0:
            self.game_over()

        return possible_moves

    def get_score(self):
        return self.score
    
    def is_game_over(self):
        return self.gameOver

    def game_over(self):
        self.gameOver = True
        self.cobra = self.pygame.Color(255, 0, 0)
        self.fruta = self.pygame.Color(255, 0, 0)

    def get_rel_food_position(self):
        onDown = 1 if (self.snake_position[1] - self.fruit_position[1]) < 0 else 0
        onRight = 1 if (self.snake_position[0] - self.fruit_position[0]) < 0 else 0
        return [(self.snake_position[0] - self.fruit_position[0]), (self.snake_position[1] - self.fruit_position[1])]

    def draw(self):
        for pos in self.snake_body:
            self.pygame.draw.rect(self.game_window, self.cobra,
                            self.pygame.Rect(pos[0], pos[1], self.ppp, self.ppp))
        self.pygame.draw.rect(self.game_window, self.fruta, self.pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], self.ppp, self.ppp))

    def get_next_position(self, direction):
        position = [self.snake_position[0], self.snake_position[1]]
        direcao = self.get_direction()
        # offset = 10
        offset = self.ppp
        if direcao == 'UP': # Estou subindo
            if direction == 'UP': # Ir pra frente
                position[1] -= offset
            elif direction == 'RIGHT':
                position[0] += offset
            elif direction == 'LEFT':
                position[0] -= offset
        elif direcao == 'DOWN': # Estou descendo
            if direction == 'UP': # Ir pra frente
                position[1] += offset
            elif direction == 'RIGHT':
                position[0] -= offset
            elif direction == 'LEFT':
                position[0] += offset
        elif direcao == 'RIGHT': # Estou indo pra direita
            if direction == 'UP': # Ir pra frente
                position[0] += offset
            elif direction == 'RIGHT':
                position[1] += offset
            elif direction == 'LEFT':
                position[1] -= offset
        elif direcao == 'LEFT': # Estou indo pra esquerda
            if direction == 'UP': # Ir pra frente
                position[0] -= offset
            elif direction == 'RIGHT':
                position[1] -= offset
            elif direction == 'LEFT':
                position[1] += offset
        return position

    def move(self, direction):
        if self.gameOver:
            return

        # Moving the snake
        position = self.get_next_position(direction)
        self.snake_position[0] = position[0]
        self.snake_position[1] = position[1]

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        if self.moves < 4:
            self.moves = self.moves + 1
        self.score += 0.5
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 1000/self.moves
            self.moves = 0
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawn:
           self.fruit_position = [random.randrange(1, ((self.tabuleiro[0] - 2*self.ppp)//self.ppp)) *self.ppp,
                        random.randrange(1, ((self.tabuleiro[1] - 2*self.ppp)//self.ppp)) * self.ppp]
            
        self.fruit_spawn = True
    
        # Game Over conditions
        if self.snake_position[0] < 0 or self.snake_position[0] > self.tabuleiro[0]-10:
            self.game_over()
        if self.snake_position[1] < 0 or self.snake_position[1] > self.tabuleiro[1]-10:
            self.game_over()
    
        # Touching the snake body
        # for block in self.snake_body[1:]:
        #     if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
        #         self.game_over()
        if (self.snake_position in self.obstaculos) or (self.snake_position in self.snake_body[1:]):
            self.game_over()

    def smart_move(self):
        move = self.brain.get_move(self)
        self.move(move)

    