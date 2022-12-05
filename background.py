
import pygame
import random
from random import randint

col = random.randint(0, 255)
star_colour = (col, col, col)
star_x = randint(0, 800)
star_list = []
class BackgroundStar:

    def __init__(self, screen, y = randint(0, 800)):

        self.screen = screen
        self.y = y
        col = random.randint(0, 255)
        star_colour = (col, col, col)
        self.y_move = 1
        self.speed = 8


    def draw_circle(self):
        #self.screen.fill('black')
        #star = pygame.draw.circle(self.screen, star_colour, (star_x, self.y), 50)
        for ctr in range(25):  # 25 circles
            x = randint(50, 450)
            #y = randint(50, 450)

            # I would like to draw about 50 dots of this type.
            dot = pygame.draw.circle(self.screen, star_colour, (x, self.y), 15)
            #pygame.screen.update()  # update screen
            star_list.append(dot)
        #self.screen.fill('black')



    def move_itself(self):
        if self.y >= 800:
            self.y = -100
        self.y += self.y_move

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y += self.speed

    def update(self):

        self.move_itself()
        self.move()
        self.draw_circle()
