import random
import pygame

class EnemyAI:
    def __init__(self, player):
        self.player = player
        self.board = player.board
        
        self.x = 0
        self.y = 0
        self.board.fill_position(self.x, self.y, 3)
        
        self.speed = 1  # Set the enemy's speed
        self.clock = 0  # Set the enemy's clock
        self.slow = False  # Set the enemy's slow status
        self.phase = False  # Set the enemy's phase status
        
        self.old_position_value = None  # Set the enemy's old position value

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x * self.board.spot_size, self.y * self.board.spot_size, self.board.spot_size, self.board.spot_size))
    
    def draw_state(self, screen):
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 16)

        # If the enemy is slow, draw the slow status
        if self.slow:
            # Create a text surface object
            text = font.render('Enemy is slow', True, (0, 0, 0), (255, 255, 255))

            # Draw the text object on the screen
            screen.blit(text, (675, 10))
            
        # If the enemy is in phase, draw the phase status
        if self.phase:
            # Create a text surface object
            text = font.render('Enemy is phasing', True, (0, 0, 0), (255, 255, 255))

            # Draw the text object on the screen
            screen.blit(text, (650, 30))
    
    def process_freeze(self):
        if self.slow:
            if random.randint(1, 20) == 1:
                self.slow = False
                self.clock = 0
            elif self.clock % 2 == 0:
                self.clock += 1
                return "freeze"
            else:
                self.clock += 1
            
    def process_random_phase(self):
        if not self.phase:
            # Generate a random number between 1 and 5, if it is 5 then make the enemy phase
            if random.randint(1, 20) == 1:
                self.phase = True
        else:
            if random.randint(1, 5) == 1:
                self.phase = False
                self.old_position_value = None
    
    def move(self):

        self.process_random_phase()
            
        if self.process_freeze() == "freeze":
            return
        
        x_difference = abs(self.player.x - self.x)
        y_difference = abs(self.player.y - self.y)

        new_x = self.x
        new_y = self.y

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

        if self.phase == False and self.board.get_position(new_x, new_y) != 2:  # Check if the new position is not an obstacle
            self.board.fill_position(self.x, self.y, 0)
            self.board.fill_position(new_x, new_y, 3)
            self.x, self.y = new_x, new_y
        elif self.phase == True:  # If the enemy is phasing, try moving in the new direction
            self.board.fill_position(self.x, self.y, self.old_position_value)
            self.old_position_value = self.board.get_position(new_x, new_y)
            self.board.fill_position(new_x, new_y, 3)
            self.x, self.y = new_x, new_y
        else:  # If the new position is an obstacle, try moving in the other direction
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