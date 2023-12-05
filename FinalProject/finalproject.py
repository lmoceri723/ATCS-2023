import time
import pygame

# Initialize Pygame
pygame.init()

# Create a clock object
clock = pygame.time.Clock()

# Set the frames per second (FPS)
FPS = 10

# Set up the screen
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cross Country Game")

# Set up the board
board_width = 32
board = [[0 for x in range(board_width)] for y in range(board_width)]

# Set up the character
character_width = screen_width / board_width
character_height = screen_height / board_width
character_speed = 1
character_x = board_width // 2
character_y = board_width // 2 - 3
board[character_x][character_y] = 1

def initialize_board():
    # Read in the board from board.txt
    f = open("FinalProject/board.txt", "r")
    for i in range(board_width):
        line = f.readline()
        for j in range(board_width):
            if line[j] == "-":
                board[i][j] = 2

def draw_board(screen, board):
    for x in range(board_width):
        for y in range(board_width):
            if board[x][y] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * character_width, y * character_height, character_width, character_height))
            elif board[x][y] == 2:
                pygame.draw.rect(screen, (255, 0, 0), (x * character_width, y * character_height, character_width, character_height))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * character_width, y * character_height, character_width, character_height))

initialize_board()
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Cap the frame rate and get the time passed since the last frame
    dt = clock.tick(FPS)
    
    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Move the character based on the key pressed
    if keys[pygame.K_w]:
        if (board[character_x][character_y - 1] == 2):
            continue
        board[character_x][character_y] = 0
        character_y -= character_speed
        character_y %= board_width
        board[character_x][character_y] = 1
    if keys[pygame.K_s]:
        if (board[character_x][character_y + 1] == 2):
            continue
        board[character_x][character_y] = 0
        character_y += character_speed
        character_y %= board_width
        board[character_x][character_y] = 1
    if keys[pygame.K_a]:
        if (board[character_x - 1][character_y] == 2):
            continue
        board[character_x][character_y] = 0
        character_x -= character_speed
        character_x %= board_width
        board[character_x][character_y] = 1
    if keys[pygame.K_d]:
        if (board[character_x + 1][character_y] == 2):
            continue
        board[character_x][character_y] = 0
        character_x += character_speed
        character_x %= board_width
        board[character_x][character_y] = 1

    # Update the screen
    screen.fill((0, 0, 0))
    draw_board(screen, board)
    pygame.display.flip()

# Quit the game
pygame.quit()
