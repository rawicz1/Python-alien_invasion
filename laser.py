import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed = - 8, colour = 'orange'):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    

    def update(self):

        self.rect.y -= self.speed


