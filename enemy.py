import pygame
import random
from assets import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image=ENEMY[0]):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIN_WIDTH
        self.rect.y = 300
        self.step_index = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, speed, image=ENEMY[0]):
        self.image = ENEMY[self.step_index // 9]
        self.step_index += 1

        self.rect.x -= speed
        if self.step_index >= 36:
            self.step_index = 0


    def draw(self, DISPLAY):
        DISPLAY.blit(self.image, self.rect)