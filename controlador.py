class Controle:
    def __init__(self, cascavel, brain):
        self.cascavel = cascavel
        self.brain = brain
        self.directions = ['LEFT', 'UP', 'RIGHT']
        self.movimentos_feitos = 0
        self.mov_since_food = 0
        self.last_score = 0

    def move(self):
        movimentos = self.cascavel.get_possible_moves()
        food_position = self.cascavel.get_rel_food_position()        
        move = self.brain.get_move(movimentos + food_position)
        self.cascavel.move(self.directions[move])
        self.movimentos_feitos = self.movimentos_feitos + 1
        self.mov_since_food = self.mov_since_food + 1
        if self.last_score == self.cascavel.frutas and self.mov_since_food > 2000:
            self.cascavel.game_over()
        elif self.last_score < self.cascavel.frutas:
            self.mov_since_food = 0
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
