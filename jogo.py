
import random

class Cascavel:

    # Onde ppp é uma variável de controle (pixels por ponto) que determina uma melhor conversão entre o que é mostrado na tela e o que é o jogo real
    # Por exemplo, para calcular o x_max, tem-se a largura total da tela menos o ppp para impedir que a cobrinha já comece na beirada do tabuleiro

    def __init__(self, tabuleiro, obstaculos, aleatorio = False):
        self.aleatorio = aleatorio
        self.obstaculos = obstaculos
        self.posicoes_frutas = [(18, 2), (4, 10), (14, 4), (1, 3), (2, 19), (15, 14), (1, 6), (13, 4), (8, 18), (5, 18), (10, 7), (14, 9), (6, 11), (18, 1), (1, 13), (9, 4), (13, 18), (9, 6), (12, 8), (1, 1), (9, 10), (3, 11), (10, 6), (17, 1), (2, 12), (13, 2), (18, 2), (13, 14), (15, 9), (4, 10), (15, 15), (3, 11), (2, 14), (13, 10), (6, 11), (13, 1), (11, 6), (10, 15), (7, 16), (19, 18)]
        
        self.tabuleiro = tabuleiro
        
        # Configuração de cores de desenho
        self.cobra = None
        self.fruta = None
        self.reset()
    
    def reset(self):
        self.frutas = 0
        # defining snake default position
        x_max = self.tabuleiro[0]
        y_max = self.tabuleiro[1]
        # Se for aleatório, deve gerar uma posição da fruta e da cobra aleatoriamente no mapa
        if self.aleatorio:
            self.snake_position = [random.randint(1, x_max), random.randint(1, y_max)]
            self.snake_body = [[self.snake_position[0], self.snake_position[1]],
                [self.snake_position[0] + 1, self.snake_position[1]],
                [self.snake_position[0] + 2, self.snake_position[1]],
                [self.snake_position[0] + 3, self.snake_position[1]],
                [self.snake_position[0] + 4, self.snake_position[1]]
            ]
            self.fruit_position = [random.randrange(1, (self.tabuleiro[0])), random.randrange(1, (self.tabuleiro[1]))]
        else:
            # Caso contrario, fixar em 300 e 100
            self.snake_position = [5, 5]
            self.snake_body = [[self.snake_position[0], self.snake_position[1]],
                [self.snake_position[0] + 1, self.snake_position[1]],
                [self.snake_position[0] + 2, self.snake_position[1]],
                [self.snake_position[0] + 3, self.snake_position[1]],
                [self.snake_position[0] + 4, self.snake_position[1]]
            ]
                    # fruit position
            self.fruit_position = [3, 10]
        self.fruit_spawn = True
        self.gameOver = False
        # definições de pontuação
        self.score = 0
        
    def get_direction(self):
        if self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] < self.snake_body[1][1]: # Estou subindo
           return 'UP'
        elif self.snake_body[0][0] == self.snake_body[1][0] and self.snake_body[0][1] > self.snake_body[1][1]: # Estou descendo
            return 'DOWN'
        elif self.snake_body[0][0] > self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra direita
            return 'RIGHT'
        elif self.snake_body[0][0] < self.snake_body[1][0] and self.snake_body[0][1] == self.snake_body[1][1]: # Estou indo pra esquerda
            return 'LEFT'

    def is_valid_position(self, position, scale = 0):
        if (scale <= position[0] <= (self.tabuleiro[0])) and (scale <= position[1] <= (self.tabuleiro[1]) - scale ) and (position not in self.snake_body) and (position not in self.obstaculos):
            return True
        return False

    def get_score(self):
        return self.score
    
    def is_game_over(self):
        return self.gameOver

    def game_over(self):
        self.gameOver = True

    def draw(self, pygame, game_window):
        if self.cobra is None:
            self.cobra = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.fruta = self.cobra
        if self.gameOver:
            self.cobra = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.fruta = self.cobra

        window_width, window_height = game_window.get_size()
        ppp = min(window_width / self.tabuleiro[0], window_height / self.tabuleiro[1])

        for idx, pos in enumerate(self.snake_body):
            pygame.draw.rect(game_window, self.cobra,
                            pygame.Rect(pos[0] * ppp, pos[1] * ppp, ppp, ppp))
        pygame.draw.rect(game_window, self.fruta, pygame.Rect(
            self.fruit_position[0] * ppp, self.fruit_position[1] * ppp, ppp, ppp))

    def get_next_position(self, direction):
        position = [self.snake_position[0], self.snake_position[1]]
        direcao = self.get_direction()
        offset = 1
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
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 1
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
                self.fruit_position = [random.randrange(1, (self.tabuleiro[0])),
                            random.randrange(1, (self.tabuleiro[1]))]
           else:
                if len(self.posicoes_frutas) > self.frutas + 1:
                    self.fruit_position[0] = self.posicoes_frutas[self.frutas][0]
                    self.fruit_position[1] = self.posicoes_frutas[self.frutas][1]
                else:
                    self.fruit_position = [random.randrange(1, (self.tabuleiro[0])),
                            random.randrange(1, (self.tabuleiro[1]))]

        self.fruit_spawn = True    
        # Game Over conditions
        # Se bateu na borda do tabuleiro

        if self.is_valid_position(self.snake_position, 0):
            self.game_over()

        if self.snake_position[0] < 0 or self.snake_position[0] > self.tabuleiro[0]:
            self.game_over()
        if self.snake_position[1] < 0 or self.snake_position[1] > self.tabuleiro[1] :
            self.game_over()

        # Se bateu no proprio corpo
        if (self.snake_position in self.obstaculos) or (self.snake_position in self.snake_body[1:]):
            self.game_over()

        return [self.score, self.is_game_over()]
    