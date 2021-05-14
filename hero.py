import pygame
import random
from assets import *


class Hero(pygame.sprite.Sprite):
    X_position = 50
    Y_position = 250

    VELOCITY = 14

    def __init__(self, image=RUN[0]):

        self.image = image
        self.hero_running = True
        self.hero_jumping = False
        self.velocity = self.VELOCITY
        self.step_index = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        if self.hero_running:
            self.run()
        if self.hero_jumping:
            self.jump()

        if self.step_index >= 36:
            self.step_index = 0

    def run(self):
        self.image = RUN[self.step_index // 6]
        self.rect.x = self.X_position
        self.rect.y = self.Y_position
        self.step_index += 1

    def jump(self):
        self.hero_jumping = True
        self.image = JUMP[0]
        self.hero_running = False

        if self.hero_jumping:
            self.rect.y -= self.velocity * 2
            self.velocity -= 0.8
        if self.velocity <= -self.VELOCITY:
            self.hero_jumping = False
            self.hero_running = True
            self.velocity = self.VELOCITY



    def draw(self, DISPLAY):
        DISPLAY.blit(self.image, (self.rect.x, self.rect.y))
