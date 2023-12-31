"""
This file contains the Player class, which represents the player in the game.
The Player class is responsible for moving the player and drawing the player.

@author: Landon Moceri (with the help of GitHub Copilot)
"""
import pygame
from board import Board

class Player:
    def __init__(self, board, width, height):
        self.marker = 1
        self.board = board
        self.x = self.board.width // 2
        self.y = self.board.width // 2 - 3
        
        self.board.fill_position(self.x, self.y, self.marker)
        
        self.width = width
        self.height = height
        self.speed = 1
        self.color = (0, 0, 255)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * self.width, self.y * self.height, self.width, self.height))
                    
    def move(self, direction):
        # Move the player in the given direction
        new_x = self.x
        new_y = self.y
        
        # Check if the new position is on the board
        if direction == "up":
            new_y = self.y - self.speed
            if new_y < 0:
                return 
        elif direction == "down":
            new_y = self.y + self.speed
            if new_y >= self.board.width:
                return 
        elif direction == "left":
            new_x = self.x - self.speed
            if new_x < 0:
                return 
        elif direction == "right":
            new_x = self.x + self.speed
            if new_x >= self.board.width:
                return
        
        # Check if the new position is an obstacle
        if self.board.get_position(new_x, new_y) == 2:
            return
        
        # Move the player
        self.board.fill_position(self.x, self.y, 0)
        self.board.fill_position(new_x, new_y, 1)
        
        self.x, self.y = new_x, new_y
        
    def reset(self):
        self.x = self.board.width // 2
        self.y = self.board.width // 2 - 3
        
        self.board.fill_position(self.x, self.y, self.marker)