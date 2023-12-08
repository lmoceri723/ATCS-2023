import pygame

class Board:
    def __init__(self, width, spot_size):
        self.width = width
        self.empty_color = (255, 255, 255)
        self.obstacle_color = (0, 0, 0)
        self.spot_size = spot_size
        
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.width)]
        # Read in the board from board.txt
        f = open("board.txt", "r")
        for i in range(self.width):
            line = f.readline()
            for j in range(self.width):
                if line[j] == "-":
                    self.fill_position(i, j, 2)

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.width):
                if self.grid[x][y] == 1:
                    #pygame.draw.rect(screen, (0, 0, 255), (x * self.spot_size, y * self.spot_size, self.spot_size, self.spot_size))
                    pass
                elif self.grid[x][y] == 2:
                    pygame.draw.rect(screen, self.obstacle_color, (x * self.spot_size, y * self.spot_size, self.spot_size, self.spot_size))
                elif self.grid[x][y] == 3:
                    # pygame.draw.rect(screen, (255, 0, 0), (x * self.spot_size, y * self.spot_size, self.spot_size, self.spot_size))
                    pass
                else:
                    pygame.draw.rect(screen, self.empty_color, (x * self.spot_size, y * self.spot_size, self.spot_size, self.spot_size))

    def fill_position(self, row, col, value):
        self.grid[row][col] = value
        
    def get_position(self, row, col):
        return self.grid[row][col]
