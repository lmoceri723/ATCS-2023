class EnemyAI:
    def __init__(self, player):
        self.player = player
        self.board = player.board
        
        self.x = 0
        self.y = 0
        
        self.speed = 1  # Set the enemy's speed

    def move(self):
        # Calculate the difference from the player to the enemy and take its absolute value
        x_difference = abs(self.player_x - self.x)
        y_difference = abs(self.player_y - self.y)

        # If the enemy is closer to the player on the x axis, move towards the player on the x axis
        if x_difference > y_difference:
            if self.player_x > self.x:
                self.x += self.speed
            else:
                self.x -= self.speed
        # If the enemy is closer to the player on the y axis, move towards the player on the y axis
        else:
            if self.player_y > self.y:
                self.y += self.speed
            else:
                self.y -= self.speed

