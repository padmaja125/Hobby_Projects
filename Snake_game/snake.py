# Libraries required for Snake game

import sys
import pygame
import random
import time

# Screen size for the game
Window_Height = 480
Window_Width = 640

# Color range for using inside game
Black_color = (0, 0, 0)
White_color = (255, 255, 255)
Red_color = (255, 0, 0)
Green_color = (0, 255, 0)
Blue_color = (0, 0, 255)


# Creating the Class for Window
class Window:
    # setting the constru with parameter
    def __init__(self, window):
        self.window = window

    def draw_stages(self):
        self.window.fill(Black_color)

    def draw_snake(self, game, snake_body):
        for pixel in snake_body:
            game.draw.rect(self.window, Green_color, game.Rect(pixel[0], pixel[1], 10, 10))

    def draw_food(self, game, food):
        game.draw.rect(self.window, Blue_color, game.Rect(food[0], food[1], 10, 10))

    def draw_score(self, game, score):
        Score_font = game.font.SysFont('Italic', 40)
        score_surface = Score_font.render(f'Score: ${score}', True, White_color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (Window_Width // 2, 15)
        self.window.blit(score_surface, score_rect)

    def draw_game_over(self, game, exit_game):
        Final_font = game.font.SysFont('Times New Roman', 30)
        final_surface = Final_font.render('Game Over', True, Red_color)
        final_rect = final_surface.get_rect()
        final_rect.midtop = (Window_Width // 2, Window_Height // 2)
        self.window.fill(Black_color)
        self.window.bill(final_surface, final_rect)
        game.display.update()
        time.sleep(10)
        exit_game()


class Snake:
    def __init__(self):
        self.snake_head = [100, 50]
        self.snake_direction = 'RIGHT'
        self.snake_body = [
            self.snake_head,
            [self.snake_head[0] - 10, self.snake_head[1]],
            [self.snake_head[0] - 20, self.snake_head[1]]
        ]

    def snake_change_direction(self, new_direction):
        if new_direction == self.snake_direction:
            return
        if self.snake_direction == 'DOWN' and new_direction == 'UP':
            return
        if self.snake_direction == 'UP' and new_direction == 'DOWN':
            return
        if self.snake_direction == 'RIGHT' and new_direction == 'LEFT':
            return
        if self.snake_direction == 'LEFT' and new_direction == 'RIGHT':
            return
        self.snake_direction = new_direction

    def snake_move(self):
        if self.snake_direction == 'UP':
            self.snake_head = [self.snake_head[0], self.snake_head[1] - 10]
        if self.snake_direction == 'DOWN':
            self.snake_head = [self.snake_head[0], self.snake_head[1] + 10]
        if self.snake_direction == 'RIGHT':
            self.snake_head = [self.snake_head[0] + 10, self.snake_head[1]]
        if self.snake_direction == 'LEFT':
            self.snake_head = [self.snake_head[0] - 10, self.snake_head[1]]
        self.snake_body.insert(0, self.snake_head)
        self.snake_body.pop()

    def snake_grow(self):
        self.snake_body.insert(0, self.snake_head)
        self.snake_move()


class Food:
    def __init__(self):
        self.position = [100, 100]

    def food_respawn(self):
        self.position = [random.randrange(1, Window_Width // 10) * 10,
                         random.randrange(1, Window_Height // 10) * 10]


class Score:
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 10


class Game:
    def __init__(self):
        # initializing game vars
        self.game = pygame
        self.game.init()
        self.game.display.set_caption('Snake')
        # initializing all the Game objects
        self.fps = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        # making the game window appeared on the screen
        self.window = Window(self.game.display.set_mode(size=(Window_Width, Window_Height)))

    def game_over(self):
        # snake head running into the borders of the window
        if self.snake.snake_head[0] < 0 or self.snake.snake_head[0] > Window_Width - 10:
            self.window.draw_game_over(self.game, self.exit_game)
        if self.snake.snake_head[1] < 0 or self.snake.snake_head[1] > Window_Height - 10:
            self.window.draw_game_over(self.game, self.exit_game)

        # snake is running into itself
        for block in self.snake.snake_body[1:]:
            if block[0] == self.snake.snake_head[0] and block[1] == self.snake.snake_head[1]:
                self.window.draw_game_over(self.game, self.exit_game)

    def exit_game(self):
        self.game.quit()
        sys.exit()

    # checking if snake ate and if so, the food will reappear and score will be increased!
    def food_control(self):
        self.snake.snake_move()
        if self.snake.snake_head[0] == self.food.position[0] and self.snake.snake_head[1] == self.food.position[1]:
            self.snake.snake_grow()
            self.food.food_respawn()
            self.score.increase()

    def run(self):
        while True:
            for event in self.game.event.get():
                if event.type == self.game.QUIT:
                    self.exit_game()
                elif event.type == self.game.KEYDOWN:
                    if event.key == self.game.K_ESCAPE:
                        self.exit_game()
                    else:
                        if event.key == self.game.K_DOWN or event.key == self.game.K_s:
                            self.snake.snake_change_direction('DOWN')
                        if event.key == self.game.K_UP or event.key == self.game.K_w:
                            self.snake.snake_change_direction('UP')
                        if event.key == self.game.K_LEFT or event.key == self.game.K_a:
                            self.snake.snake_change_direction('LEFT')
                        if event.key == self.game.K_RIGHT or event.key == self.game.K_d:
                            self.snake.snake_change_direction('RIGHT')

            self.food_control()
            self.game_over()
            self.window.draw_stages()
            self.window.draw_snake(self.game, self.snake.snake_body)
            self.window.draw_food(self.game, self.food.position)
            self.window.draw_score(self.game, self.score.score)
            self.game.display.update()
            self.fps.tick(20)
