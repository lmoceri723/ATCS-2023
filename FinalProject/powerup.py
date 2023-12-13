# Create a power up class that activates the AI's freeze when collected by the player and deletes itself from the board.
# The power up should be a light blue square that is randomly placed on the board.
import random
import pygame

class PowerUp:
    def __init__(self, ai):
        self.ai = ai  
        self.board = ai.board
        
        self.get_clear_position()
            
        self.board.fill_position(self.x, self.y, 4)

        self.color = (0, 255, 255)
        
    def get_clear_position(self):
        self.x = random.randint(0, self.board.width - 1)
        self.y = random.randint(0, self.board.width - 1)
        
        while self.board.get_position(self.x, self.y) != " " or self.y <= 1:
            self.x = random.randint(0, self.board.width - 1)
            self.y = random.randint(0, self.board.width - 1)
        
    def collect(self):
        self.board.fill_position(self.x, self.y, 0)
        self.ai.slow = True
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * self.board.spot_size, self.y * self.board.spot_size, self.board.spot_size, self.board.spot_size))
        
    def reset(self):
        self.get_clear_position()
        self.board.fill_position(self.x, self.y, 4)
