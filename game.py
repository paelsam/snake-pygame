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
        self.is_alive = True
        self.crunch_sound = pygame.mixer.Sound('sounds/sound_crunch.wav')

    def draw_snake(self):
        for block in self.body:
            # create a rect
            block_rect = pygame.Rect((block.x * CELL_SIZE), (block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            # draw a rect
            pygame.draw.rect(screen, self.color, block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        global MS_UPDATE
        # Si mueres vuelves otra vez
        MS_UPDATE = 160
        self.score = 0
        self.is_alive = True
        self.body =  [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


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
        self.game_active = True

    def update(self):
        self.win_condition()
        for snake in self.snakes:
            snake.move_snake()  
        self.check_collision()
        self.lose_condition()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        for snake in self.snakes:
            snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        for snake in self.snakes:
            if self.fruit.pos == snake.body[0]:
                snake.score += 1
                self.increase_speed()
                # reposition the fruit
                self.fruit.randomize()
                # play cruch sound
                snake.play_crunch_sound()
                # add another block to the snake
                snake.add_block()
        
                for block in snake.body[1:]:
                    if block == self.fruit.pos:
                        self.fruit.randomize()

    def inputs(self):
        # Events and conditiosn for avoid that the snake move to reverse
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
        
        # snake2
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
                snake.is_alive = False
                self.game_over()
            # Check if snake is touching itself
            for block in snake.body[1:]:
                if block == snake.body[0]:
                    snake.is_alive = False
                    self.game_over()
                
    def game_over(self):
        for snake in self.snakes:
            if snake.is_alive == False:
                snake.reset() 
            
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for i in range(CELL_NUMBER):
            for j in range(CELL_NUMBER):
                if (i+j)%2 == 0:
                    grass_rect = pygame.Rect(i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE)
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

    def increase_speed(self):
        global MS_UPDATE
        for snake in self.snakes:
            if MS_UPDATE <= 100: MS_UPDATE = 100
            if snake.score > 0 and snake.score % 2 == 0:
                MS_UPDATE -= 10
    
    def win_condition(self):
        snake_1 = self.snakes[0]
        snake_2 = self.snakes[1]
        if snake_1.score == 5:
            self.game_active = False
            self.show_winner("You win Green Snake", 'green')
        if snake_2.score == 5:
            self.game_active = False
            self.show_winner("You win Red Snake", 'red')
    
    def show_winner(self, text, color):
        if self.game_active == False:
            for snake in self.snakes:
                snake.reset()
            screen.fill((175, 215, 70))
            text_winner = game_font.render(text, True, color)
            text_winner_rec = text_winner.get_rect(center = (CELL_SIZE * CELL_NUMBER / 2, CELL_SIZE * CELL_NUMBER / 2))
            text_option = game_font.render("Press any button to continue", True, 'red')
            text_option_rec = text_option.get_rect(center = (CELL_SIZE * CELL_NUMBER / 2, CELL_SIZE * CELL_NUMBER / 2 + 20))
            screen.blit(text_winner, text_winner_rec)
            screen.blit(text_option, text_option_rec)

        

        
                

pygame.init()
pygame.display.set_caption("Snake: Battle Royale")
# pygame.display.set_icon() # Set icon

FRAMERATE = 120
# Tamaño de los cuadrados
CELL_SIZE = 30
# Número de cuadrados del grid
CELL_NUMBER = 20
screen = pygame.display.set_mode(
    (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/Little turtle.ttf', 25)

main = Main()
fruit = main.fruit
if len(main.snakes) == 2:
    main.snakes[1].color = (200, 50, 25)
    main.snakes[1].body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]


# Timers
SCREEN_UPDATE = pygame.USEREVENT
# Este evento se actualizará cada 150ms
MS_UPDATE = 180
pygame.time.set_timer(SCREEN_UPDATE, MS_UPDATE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            pygame.time.set_timer(SCREEN_UPDATE, MS_UPDATE)
            main.update()
        if event.type == pygame.KEYDOWN:
            main.game_active = True
            main.inputs()

    if main.game_active == True:
        screen.fill((175, 215, 70))
        main.draw_elements()
        clock.tick(FRAMERATE)
    else:
        main.win_condition()
    
    pygame.display.update()
        
