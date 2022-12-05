import random
from settings import Settings
import pygame
from laser import Laser
from background import BackgroundStar

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()

        self.image = pygame.image.load('./images/ship_Vini1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.laser_cooldown = 500
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True # create to shoot lasers
        self.laser_time = 0 # reset after shooting
        self.lasers = pygame.sprite.Group()

        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)


    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):

        sounds = ['./sounds/pio_ship.wav', './sounds/pio1.wav', './sounds/pio2.wav', './sounds/pio3.wav', './sounds/pio4.wav', './sounds/pio5.wav']
        shoot = pygame.mixer.Sound(random.choice(sounds))
        shoot.set_volume(0.3)

        x = 10
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_w]:
            x = 5
        self.lasers.add(Laser(self.rect.center, x, 'red'))
        pygame.mixer.Sound.play(shoot)

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def laser_cooldown(self):

        self.laser_cooldown -= 30


    def update(self):

        self.constraint()
        self.get_input()
        self.recharge()
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)


