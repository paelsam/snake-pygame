import pygame
from pygame.math import Vector2
from sys import exit
from random import randint


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.color = (120, 150, 25)
        self.score = len(self.body) - 3
        self.crunch_sound = pygame.mixer.Sound('sounds/sound_crunch.wav')

    def draw_snake(self):
        for block in self.body:
            # create a rect
            block_rect = pygame.Rect(
                block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # draw a rect
            pygame.draw.rect(screen, self.color, block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def play_crunch_sound(self):
        self.crunch_sound.play()
        

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        # create a rectangle
        fruit_rect = pygame.Rect(
            self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # draw the rectangle
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    # Create aletories positions for the fruit
    def randomize(self):
        # create x and y psition
        self.y = randint(0, CELL_NUMBER - 1)
        self.x = randint(0, CELL_NUMBER - 1)
        # draw a square vector
        self.pos = [self.x, self.y]


class Main:
    def __init__(self):
        self.snakes = [Snake(), Snake()]
        self.fruit = Fruit()

    def update(self):
        for snake in self.snakes:
                snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        for snake in self.snakes:
            snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        global MS_UPDATE
        for snake in self.snakes:
            if self.fruit.pos == snake.body[0]:
                snake.score += 1
                if snake.score % 5 == 0:
                    if MS_UPDATE <= 80 : MS_UPDATE = 80
                    else:                                        
                        MS_UPDATE -= 10
                    print(MS_UPDATE)
                # reposition the fruit
                self.fruit.randomize()
                # play cruch sound
                snake.play_crunch_sound()
                # add another block to the snake
                snake.new_block = True
        
                for block in snake.body[1:]:
                    if self.fruit.pos == block:
                        self.fruit.randomize()

    def inputs(self):
        # snake1
        if event.key == pygame.K_UP:
            if self.snakes[0].direction.y != 1:
                self.snakes[0].direction = Vector2(0, -1)
        if event.key == pygame.K_DOWN:
            if self.snakes[0].direction.y != -1:
                self.snakes[0].direction = Vector2(0, 1)
        if event.key == pygame.K_LEFT:
            if self.snakes[0].direction.x != 1:
                self.snakes[0].direction = Vector2(-1, 0)
        if event.key == pygame.K_RIGHT:
            if self.snakes[0].direction.x != -1:
                self.snakes[0].direction = Vector2(1, 0)
        if len(self.snakes) == 2:
            # Snake 2 input
            if event.key == pygame.K_w:
                if self.snakes[1].direction.y != 1:
                    self.snakes[1].direction = Vector2(0, -1)
            if event.key == pygame.K_s:
                if self.snakes[1].direction.y != -1:
                    self.snakes[1].direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                if self.snakes[1].direction.x != 1:
                    self.snakes[1].direction = Vector2(-1, 0)
            if event.key == pygame.K_d:
                if self.snakes[1].direction.x != -1:
                    self.snakes[1].direction = Vector2(1, 0)

    def lose_condition(self):
        for snake in self.snakes:
            # Check if snake is outside the screen
            if not 0 <= snake.body[0].x < CELL_NUMBER or not 0 <= snake.body[0].y < CELL_NUMBER:
                self.game_over()
            # Check if snake is touching itself
            for block in snake.body[1:]:
                if block == snake.body[0]:
                    self.game_over()
                

    def game_over(self):
            self.snakes[0].body =  [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
            self.snakes[0].direction = Vector2(0, 0)
            if len(self.snakes) == 2:
                self.snakes[1].body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
                self.snakes[1].direction = Vector2(0, 0)


    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2: 
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE , row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else: 
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE , row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
            score_surface = game_font.render(f"Snake Green: {str(self.snakes[0].score)}", True, (56,74,12))
            score_x = int(CELL_SIZE * CELL_NUMBER - 100)
            score_y = int(CELL_SIZE * CELL_NUMBER - 40)
            score_rect = score_surface.get_rect(center = (score_x, score_y))
            screen.blit(score_surface, score_rect)
            if len(self.snakes) == 2:
                score_surface = game_font.render(f"Snake Red: {str(self.snakes[1].score)}", True, (130,74,12))
                score_x_2 = 100
                score_rect = score_surface.get_rect(center = (score_x_2, score_y))
                screen.blit(score_surface, score_rect)

                

pygame.init()
pygame.display.set_caption("Snake: Battle Royale")
# pygame.display.set_icon() # Set icon

FRAMERATE = 60
# Tamaño de los cuadrados
CELL_SIZE = 30
# Número de cuadrados del grid
CELL_NUMBER = 20
screen = pygame.display.set_mode(
    (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/Little turtle.ttf', 25)

main = Main()
if len(main.snakes) == 2:
    main.snakes[1].color = (200, 50, 25)
    main.snakes[1].body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
fruit = main.fruit


# Timers
SCREEN_UPDATE = pygame.USEREVENT
# Este evento se actualizará cada 150ms
MS_UPDATE = 160
pygame.time.set_timer(SCREEN_UPDATE, MS_UPDATE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main.update()
            pygame.time.set_timer(SCREEN_UPDATE, MS_UPDATE)
        if event.type == pygame.KEYDOWN:
            # Events and conditiosn for avoid that the snake move to reverse
            main.inputs()



    screen.fill((175, 215, 70))
    main.draw_elements()
    main.lose_condition()
    pygame.display.update()
    clock.tick(FRAMERATE)
