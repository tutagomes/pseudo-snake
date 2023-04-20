
import random
import numpy as np

class Cascavel:

    # Onde ppp é uma variável de controle (pixels por ponto) que determina uma melhor conversão entre o que é mostrado na tela e o que é o jogo real
    # Por exemplo, para calcular o x_max, tem-se a largura total da tela menos o ppp para impedir que a cobrinha já comece na beirada do tabuleiro

    def __init__(self, tabuleiro, ppp, obstaculos, aleatorio = False):
        self.aleatorio = aleatorio
        self.posicoes_frutas = [[100, 100], [300, 300], [300, 100], [100, 400], [400, 500], [100, 100], [300, 300], [100, 100]]
        self.obstaculos = obstaculos
        self.ppp = ppp
        # defining snake default position
        x_max = tabuleiro[0] - ppp
        y_max = tabuleiro[1] - ppp
        # Se for aleatório, deve gerar uma posição da fruta e da cobra aleatoriamente no mapa
        if aleatorio:
            self.snake_position = [random.randint(1, x_max/ppp)*ppp, random.randint(1, y_max/ppp)*ppp]
            self.snake_body = [[self.snake_position[0], self.snake_position[1]],
                [self.snake_position[0] + ppp, self.snake_position[1]],
                [self.snake_position[0] + 2*ppp, self.snake_position[1]],
                [self.snake_position[0] + 3*ppp, self.snake_position[1]],
                [self.snake_position[0] + 4*ppp, self.snake_position[1]]
            ]
            self.fruit_position = [random.randrange(1, ((tabuleiro[0] - 2*ppp)//ppp)) * ppp, random.randrange(1, ((tabuleiro[1] - 2*ppp)//ppp)) * ppp]
        else:
            # Caso contrario, fixar em 300 e 100
            self.snake_position = [300, 300]
            self.snake_body = [[self.snake_position[0], self.snake_position[1]],
                [self.snake_position[0] + ppp, self.snake_position[1]],
                [self.snake_position[0] + 2*ppp, self.snake_position[1]],
                [self.snake_position[0] + 3*ppp, self.snake_position[1]],
                [self.snake_position[0] + 4*ppp, self.snake_position[1]]
            ]
                    # fruit position
            self.fruit_position = [100, 100]
        self.tabuleiro = tabuleiro
        self.fruit_spawn = True
        self.gameOver = False

        # definições de pontuação
        self.score = 0
        self.moves = 0
        self.frutas = 0

        # Configuração de cores de desenho
        self.cobra = None
        self.fruta = None

    def get_direction(self):
        if self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] < self.snake_body[1][1]: # Estou subindo
           return 'UP'
        elif self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] > self.snake_body[1][1]: # Estou descendo
            return 'DOWN'
        elif self.snake_body[0][0] > self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra direita
            return 'RIGHT'
        elif self.snake_body[0][0] < self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra esquerda
            return 'LEFT'

    def is_valid_position(self, position, scale):
        if (scale <= position[0] < (self.tabuleiro[0]) - scale) and (scale <= position[1] < (self.tabuleiro[1]) - scale ) and (position not in self.snake_body) and (position not in self.obstaculos):
            return True
        return False

    def get_possible_moves(self):
        possible_moves = []
        scale = self.ppp

        new_position = self.get_next_position("LEFT")
        if self.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)
        
        new_position = self.get_next_position("UP")
        if self.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        new_position = self.get_next_position("RIGHT")
        if self.is_valid_position(new_position, scale):
            possible_moves.append(1)
        else:
            possible_moves.append(0)

        if np.sum(possible_moves) == 0:
            self.game_over()

        return possible_moves

    def get_score(self):
        return self.score
    
    def get_fruits(self):
        return self.frutas
    
    def is_game_over(self):
        return self.gameOver

    def game_over(self):
        self.gameOver = True

    def get_rel_food_position(self):
        onDown = (self.snake_position[1] - self.fruit_position[1]) / self.tabuleiro[1]
        onRight = (self.snake_position[0] - self.fruit_position[0]) / self.tabuleiro[0]
        # return [1 if (self.snake_position[0] - self.fruit_position[0]) > 0 else 0, 1 if (self.snake_position[1] - self.fruit_position[1]) > 0 else 0]
        return [onDown, onRight]
    
    def draw(self, pygame, game_window):
        if self.cobra is None:
            self.cobra = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            # self.fruta = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.fruta = self.cobra
        if self.gameOver:
            self.cobra = pygame.Color(255, 0, 0)
            self.fruta = self.cobra
        for pos in self.snake_body:
            pygame.draw.rect(game_window, self.cobra,
                            pygame.Rect(pos[0], pos[1], self.ppp, self.ppp))
        pygame.draw.rect(game_window, self.fruta, pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], self.ppp, self.ppp))

    def get_next_position(self, direction):
        position = [self.snake_position[0], self.snake_position[1]]
        direcao = self.get_direction()
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

    def __have_scored(self):
        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        self.score -= 0.5
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 10000
            self.moves = 0
            self.fruit_spawn = False
            self.frutas += 1
        else:
            self.snake_body.pop()

    def move(self, direction):
        if self.gameOver:
            return

        # Moving the snake
        position = self.get_next_position(direction)
        self.snake_position[0] = position[0]
        self.snake_position[1] = position[1]

        # vamos calcular o quanto a cobra ganhou
        self.__have_scored()

        if not self.fruit_spawn:
           if self.aleatorio:
                self.fruit_position = [random.randrange(1, ((self.tabuleiro[0] - 2*self.ppp)//self.ppp)) *self.ppp,
                            random.randrange(1, ((self.tabuleiro[1] - 2*self.ppp)//self.ppp)) * self.ppp]
           else:
                if len(self.posicoes_frutas) > self.frutas + 1:
                    self.fruit_position[0] = self.posicoes_frutas[self.frutas][0]
                    self.fruit_position[1] = self.posicoes_frutas[self.frutas][1]
                else:
                    self.game_over()

            
        self.fruit_spawn = True
    
        # Game Over conditions
        # Se bateu na borda do tabuleiro
        if self.snake_position[0] < 0 or self.snake_position[0] > self.tabuleiro[0] - self.ppp:
            # self.score -= 1000
            self.game_over()
        if self.snake_position[1] < 0 or self.snake_position[1] > self.tabuleiro[1] - self.ppp:
            # self.score -= 1000
            self.game_over()

        # Se bateu no proprio corpo
        if (self.snake_position in self.obstaculos) or (self.snake_position in self.snake_body[1:]):
            self.score -= 1000
            self.game_over()

    