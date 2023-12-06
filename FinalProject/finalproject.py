import pygame
from board import Board
from player import Player

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Create a clock object
        self.clock = pygame.time.Clock()

        # Set the frames per second (FPS)
        self.FPS = 10

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
        
    def draw(self):
        # Update the screen
        self.screen.fill(self.screen_color)
        self.board.draw(self.screen)
        pygame.display.flip()

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
            
            self.draw()

        # Quit the game
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()