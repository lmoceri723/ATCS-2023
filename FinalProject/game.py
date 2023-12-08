import pygame
from board import Board
from player import Player
from ai import EnemyAI

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
        
    def draw(self):
        # Update the screen
        self.screen.fill(self.screen_color)
        self.board.draw(self.screen)
        self.player.draw(self.screen)
        self.ai.draw(self.screen)
        self.ai.draw_state(self.screen)
        self.draw_timer()
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

    def play(self):
        # Game loop
        running = True
        while running:
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
            
            if self.player_caught():
                self.game_over("AI caught you!")
                running = False
                
            if self.timer <= 0:
                self.game_over("You win!")
                running = False
                
            self.ai.move()
            self.draw()

        # Quit the game
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()