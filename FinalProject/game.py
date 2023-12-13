import pygame
from board import Board
from player import Player
from ai import EnemyAI
from powerup import PowerUp

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Create a clock object
        self.clock = pygame.time.Clock()

        # Set the frames per second (FPS)
        self.FPS = 10
        
        # Set up the timer
        self.timer = 30

        # Set up the screen
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Cross Country Game")
        self.screen_color = (255, 255, 255)
        
        # Set up the board
        self.board_size = 32
        self.board = Board(self.board_size, 800 // self.board_size)
        
        # Set up the player
        self.player = Player(self.board, 800 // self.board_size, 800 // self.board_size)
        self.ai = EnemyAI(self.player)
        
        self.power_ups = []
        for _ in range(4):
            self.power_ups.append(PowerUp(self.ai))
            
        self.scene = "title"
        
    def draw(self):
        # Update the screen
        if self.scene == "game":
            self.screen.fill(self.screen_color)
            self.board.draw(self.screen)
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            self.player.draw(self.screen)
            self.ai.draw(self.screen)
            self.ai.draw_state(self.screen)
            self.draw_timer()
            pygame.display.flip()
        elif self.scene == "title":
            self.screen.fill(self.screen_color)
            self.draw_title()
            pygame.display.flip()
            
    def draw_title(self):
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        # Create a text surface object
        text = font.render('Cross Country: The Game', True, (0, 0, 0), (255, 255, 255))
        instructions = [
            font.render("Instructions:", True, (0, 0, 0)),
            font.render("You are the blue character.", True, (0, 0, 0)),
            font.render("Use the arrow keys to move.", True, (0, 0, 0)),
            font.render("Avoid the red AI.", True, (0, 0, 0)),
            font.render("Collect the light blue power ups to freeze the AI.", True, (0, 0, 0)),
            font.render("You have 30 seconds to survive.", True, (0, 0, 0)),
            font.render("Press space to play.", True, (0, 0, 0)),
]
        # Draw the text object on the screen followed by the instructions
        # Make the title at the top
        # Make the instructions below the title with a gap inbetween the title and instructions
        # Make the instructions fit on the screen
        
        self.screen.blit(text, (self.screen_width // 2 - 200, self.screen_height // 2 - 200))
        for i in range(len(instructions)):
            self.screen.blit(instructions[i], (20, self.screen_height // 2 - 100 + i * 50))
        
        
        pygame.display.flip()
    
    def draw_timer(self):
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 32)

        # Create a text surface object
        text = font.render('Time left: ' + str(int(self.timer)), True, (0, 0, 0), (255, 255, 255))

        # Draw the text object on the screen
        self.screen.blit(text, (10, 10))  # Adjust the position as needed
        
        
    def game_over(self, message):
        # Draw the board
        self.draw()
        
        # Create a font object
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        # Create a text surface object
        text = font.render(message, True, (0, 0, 0), (255, 255, 255))
        
        # Create a rectangular object for the text surface object
        textRect = text.get_rect()
        
        # Set the center of the rectangular object
        textRect.center = (self.screen_width // 2, self.screen_height // 2)
        
        # Blit the text onto the screen
        self.screen.blit(text, textRect)
        
        # Update the screen
        pygame.display.flip()
        
        # Wait for 3 seconds
        pygame.time.wait(3000)
        
    def player_caught(self):
        # See if the player is within 1 square of the ai
        x_difference = abs(self.player.x - self.ai.x)
        y_difference = abs(self.player.y - self.ai.y)
        
        if x_difference <= 1 and y_difference <= 1:
            return True
        
    def player_on_power_up(self):
        for power_up in self.power_ups:
            if self.player.x == power_up.x and self.player.y == power_up.y:
                return power_up
        return False
    
    def reset(self):
        self.board.reset()
        self.player.reset()
        self.ai.reset()
        for power_up in self.power_ups:
            power_up.reset()
        self.timer = 30
        self.scene = "title"

    def play(self):
        # Game loop
        pygame.display.flip()
            
        running = True
        while running:
            if self.scene == "title":
                # Move to the game scene after the player clicks space
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.scene = "game"
                            self.draw()
                            pygame.time.wait(250)
                    elif event.type == pygame.QUIT:
                        running = False
                
            elif self.scene == "game":
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                # Cap the frame rate and get the time passed since the last frame
                dt = self.clock.tick(self.FPS)
                self.timer -= dt / 1000
                
                # Get the state of the keyboard
                keys = pygame.key.get_pressed()

                # Move the character based on the key pressed
                if keys[pygame.K_w]:
                    self.player.move("up")
                    
                if keys[pygame.K_s]:
                    self.player.move("down")
                    
                if keys[pygame.K_a]:
                    self.player.move("left")
                    
                if keys[pygame.K_d]:
                    self.player.move("right")
                    
                if self.player_on_power_up():
                    power_up = self.player_on_power_up()
                    power_up.collect()
                    self.power_ups.remove(power_up)
                
                if self.player_caught():
                    self.game_over("AI caught you!")
                    running = False
                    self.reset()
                    # wait for 3 seconds
                    self.play()
                    
                if self.timer <= 0:
                    self.game_over("You win!")
                    running = False
                    self.reset()
                    # wait for 3 seconds
                    self.play()
                    
                self.ai.move()
            self.draw()

        # Quit the game
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()