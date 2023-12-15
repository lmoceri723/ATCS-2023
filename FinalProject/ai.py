"""
This file contains the EnemyAI class, which is used to control the enemy's movement and handle the enemy's state.

@author: Landon Moceri (with the help of GitHub Copilot)
"""
import random
import pygame
from fsm import FSM

class EnemyAI:
    def __init__(self, player):
        self.player = player
        self.board = player.board
        self.fsm = FSM("idle")
        self.initialize_fsm()
        
        self.x = 0
        self.y = 0
        self.board.fill_position(self.x, self.y, 3)
        
        self.speed = 1  # Set the enemy's speed
        self.clock = 0  # Set the enemy's clock
        
    def initialize_fsm(self):
        # Add transitions to the FSM
        self.fsm.add_transition("GAME_START", "idle", None, "move")
        
        self.fsm.add_transition("PHASE_LOST", "phase", None, "move")
        self.fsm.add_transition("PHASE_LOST", "slow_phase", None, "slow")
        
        self.fsm.add_transition("PHASE_COLLECTED", "move", None, "phase")
        self.fsm.add_transition("PHASE_COLLECTED", "slow", None, "slow_phase")
        
        self.fsm.add_transition("POWERUP_LOST", "slow", None, "move")
        self.fsm.add_transition("POWERUP_LOST", "slow_phase", None, "phase")
        
        self.fsm.add_transition("POWERUP_COLLECTED", "move", None, "slow")
        self.fsm.add_transition("POWERUP_COLLECTED", "slow", None, "slow")
        self.fsm.add_transition("POWERUP_COLLECTED", "phase", None, "slow_phase")
        
        self.fsm.add_transition("GAME_OVER", "move", None, "idle")
        self.fsm.add_transition("GAME_OVER", "slow", None, "idle")
        self.fsm.add_transition("GAME_OVER", "phase", None, "idle")
        self.fsm.add_transition("GAME_OVER", "slow_phase", None, "idle")
        

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x * self.board.spot_size, self.y * self.board.spot_size, self.board.spot_size, self.board.spot_size))
    
    def draw_state(self, screen):
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 16)

        # If the enemy is slow, draw the slow status
        if self.is_slow():
            # Create a text surface object
            text = font.render('Enemy is slow', True, (0, 0, 0), (255, 255, 255))

            # Draw the text object on the screen
            screen.blit(text, (675, 10))
            
        # If the enemy is in phase, draw the phase status
        if self.is_phase():
            # Create a text surface object
            text = font.render('Enemy is phasing', True, (0, 0, 0), (255, 255, 255))

            # Draw the text object on the screen
            screen.blit(text, (650, 30))
    
    def process_freeze(self):
        # If the enemy is frozen, check if it is time to unfreeze
        if self.is_slow():
            if random.randint(1, 20) == 1:
                # Process the power up lost state change
                self.fsm.process("POWERUP_LOST")
                self.clock = 0
            elif self.clock % 2 == 0:
                self.clock += 1
                return "freeze"
            else:
                self.clock += 1
            
    def process_random_phase(self):
        # Process the random phase status
        if self.is_phase():
            # Generate a random number between 1 and 5, if it is 1 then make the enemy unphase
            if random.randint(1, 5) == 1:
                # Process the phase lost state change
                self.fsm.process("PHASE_LOST")
        else:
            # Generate a random number between 1 and 20, if it is 1 then make the enemy phase
            if random.randint(1, 20) == 1:
                # Process the phase collected state change
                self.fsm.process("PHASE_COLLECTED")
                
    def is_slow(self):
        # Check if the enemy is slow
        return self.fsm.current_state == "slow" or self.fsm.current_state == "slow_phase"
    
    def is_phase(self):
        # Check if the enemy is in phase
        return self.fsm.current_state == "phase" or self.fsm.current_state == "slow_phase"
    
    def move(self):
        # Process the random phase and freeze status
        self.process_random_phase()
            
        if self.process_freeze() == "freeze":
            return
        
        # Calculate the difference between the enemy and the player's x and y coordinates
        x_difference = abs(self.player.x - self.x)
        y_difference = abs(self.player.y - self.y)

        new_x = self.x
        new_y = self.y

        # Try moving in the direction of the player
        if x_difference > y_difference:
            if self.player.x > self.x:
                new_x += self.speed
            else:
                new_x -= self.speed
        else:
            if self.player.y > self.y:
                new_y += self.speed
            else:
                new_y -= self.speed

        # Check if the new position is not an obstacle or if the enemy is in phase
        if self.board.get_position(new_x, new_y) != 2 or self.is_phase():  # Check if the new position is not an obstacle
            self.board.fill_position(self.x, self.y, 0)
            self.board.fill_position(new_x, new_y, 3)
            self.x, self.y = new_x, new_y
        else:  # If the new position is an obstacle and the enemy is not in phase, try moving in the other direction
            if x_difference > y_difference:
                new_x = self.x  # Reset x
                if self.player.y > self.y:
                    new_y += self.speed
                else:
                    new_y -= self.speed
            else:
                new_y = self.y  # Reset y
                if self.player.x > self.x:
                    new_x += self.speed
                else:
                    new_x -= self.speed

            if self.board.get_position(new_x, new_y) != 2:  # Check if the new position is not an obstacle
                self.board.fill_position(self.x, self.y, 0)
                self.board.fill_position(new_x, new_y, 3)
                self.x, self.y = new_x, new_y
                
        self.board.load_board()
                
    def reset(self):
        self.x = 0
        self.y = 0
        self.board.fill_position(self.x, self.y, 3)
        
        self.clock = 0