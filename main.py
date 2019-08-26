import pygame
import random

# "Constants":
windowWidth = 600
windowHeight = 600
tileSize = 20
mapWidth = 30
mapHeight = 30
startLength = 4

# Global variables:
done = False
dead = False
paused = True
lastTime = 0
currentTime = 0
deltaTime = 0
wallTiles = list()
foodTile = (0,0)

class Snake:
    def __init__(self, x, y):
        self.dir = 3   # Up, left, down, right.
        self.waitForMove = 100
        self.wait = self.waitForMove
        self.body = list([(x, y), (x-1, y), (x-2, y), (x-3, y)])
        # for i in range(startLength-1):
        #     self.body += (self.x - i - 1, self.y)

    def changeDir(self, dir):
        delta = abs(dir - self.dir)
        if delta != 2:
            self.dir = dir

    def update(self, deltaTime):
        global dead 
        self.wait -= deltaTime
        if self.wait <= 0:
            self.wait = self.waitForMove

            # Update head:
            x, y = self.body[0]
            if self.dir == 0:   # Up.
                y -= 1     
            if self.dir == 1:   # Left.
                x -= 1
            if self.dir == 2:   # Down.
                y += 1
            if self.dir == 3:   # Right.
                x += 1    
                    
            # Check if we hit food:
            if x == foodTile[0] and y == foodTile[1]:
                self.body = list([(x, y)]) + self.body[0 : len(self.body)]
                spawnFood(self)
            else:
                self.body = list([(x, y)]) + self.body[0 : len(self.body)-1]

            # check if we died:
            for wallX, wallY in wallTiles:
                if x == wallX and y == wallY:
                    print("We died from a wall!!")
                    dead = True
                    break
            for bodyX, bodyY in self.body[1 : len(self.body)]:
                if x == bodyX and y == bodyY:
                    print("We died from our own body!!")
                    dead = True
                    break
            


    def draw(self, screen):
        for x, y in self.body:
            color = (0, 128, 255)
            pygame.draw.rect(screen, color, pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize))


def spawnFood(snake):
    global foodTile
    foodX = 0
    foodY = 0
    collidedWithBody = False
    while True:
        foodX = random.randint(3, mapWidth-4)
        foodY = random.randint(3, mapHeight-4)
        for snakeX, snakeY in snake.body:
            if snakeX == foodX and snakeY == foodY:
                collidedWithBody = True
                print("Spawn food failed, inside body(%d, %d). Retrying..." % (foodX, foodY))
        if not collidedWithBody:
            break
    
    foodTile = (foodX, foodY)
    print("Spawned a food")

# init:
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
dead = False
# border:
for i in range(2, mapWidth -2):
    wallTiles.append((i, 1))
    wallTiles.append((i, mapHeight-2))

for i in range(2, mapHeight-2):
    wallTiles.append((2, i))
    wallTiles.append((mapWidth-3, i))


snake = Snake(10,10)
spawnFood(snake)

# Gameloop
while not done:
    for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        done = True
                    paused = True
                if event.key == pygame.K_w:
                    snake.changeDir(0)
                    paused = False
                if event.key == pygame.K_a:
                    snake.changeDir(1)
                    paused = False
                if event.key == pygame.K_s:
                    snake.changeDir(2)
                    paused = False
                if event.key == pygame.K_d:
                    snake.changeDir(3)
                    paused = False
    # Clear:
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, windowWidth, windowHeight))

    if dead == True:
        print("Respawn.")
        dead = False
        paused = True
        spawnFood(snake)
        snake = Snake(10, 10)
        # Do some AI shit here!

    # Time management:
    lastTime = currentTime
    currentTime = pygame.time.get_ticks()
    deltaTime = currentTime - lastTime

    if not paused:
        snake.update(deltaTime)
    if paused:
        pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(0, 0, windowWidth, windowHeight))

    # Draw walls:
    for x, y in wallTiles:
        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize))

    # Draw food:
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(foodTile[0] * tileSize, foodTile[1] * tileSize, tileSize, tileSize))

    snake.draw(screen)

    pygame.display.flip()