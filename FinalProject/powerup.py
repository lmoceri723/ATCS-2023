"""
This module contains the PowerUp class which is responsible for creating and drawing power ups.

@author: Landon Moceri (with the help of GitHub Copilot)
"""
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
        # Get a random position on the board
        self.x = random.randint(0, self.board.width - 1)
        self.y = random.randint(0, self.board.width - 1)
        
        # Make sure the position is not an obstacle
        while self.board.get_position(self.x, self.y) != 0 or self.y <= 1:
            self.x = random.randint(0, self.board.width - 1)
            self.y = random.randint(0, self.board.width - 1)
        
    def collect(self):
        # Remove the power up from the board and freeze the AI
        self.board.fill_position(self.x, self.y, 0)
        self.ai.slow = True
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * self.board.spot_size, self.y * self.board.spot_size, self.board.spot_size, self.board.spot_size))
        
