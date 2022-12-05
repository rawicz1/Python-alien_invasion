import pygame
from pygame.sprite import Sprite
from pygame.time import delay

timer = 0
amount_of_time = 20
class Alien(Sprite):
    """a class to represent a single alien in the class"""
    def __init__(self, alien_pos_x, alien_pos_y, screen_size_y, player_top_rect):
        super().__init__()
        self.player_top_rect = player_top_rect
        self.alien_pos_x = alien_pos_x
        self.alien_pos_y = alien_pos_y
        self.screen_size_y = screen_size_y
        self.image = pygame.image.load('./images/ship_transparent.png').convert_alpha()
        self.rect = self.image.get_rect(center=(alien_pos_x, alien_pos_y))
        self.alien_speedx = 4
        self.alien_speedy = 1
        self.alien_time = 50

    def level_up_speed(self):

        self.alien_speedx += 6
        self.alien_speedy += 5
    def movement(self):
        self.alien_time -=1
        if self.alien_time <=0:
            self.rect.x += self.alien_speedx
            self.rect.y += self.alien_speedy
            self.alien_time = 3

    def extra_speed(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y += self.alien_speedx

    def change_direction(self):

        if self.rect.right >= self.screen_size_y:
            self.alien_speedx *= -1
        elif self.rect.left <= 0:
            self.alien_speedx *= -1

    """def alien_bottom_game_over(self):

        if self.rect.bottom >= self.player_top_rect:
            print('Game over')"""

    def alien_collisions(self, sprite_group):

        if pygame.sprite.spritecollide(self, sprite_group, False):
            self.alien_speedx *= -1

    def update(self):
        self.movement()
        self.change_direction()
        #self.alien_bottom_game_over()
        self.extra_speed()



