import random

from assets.assets import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIN_WIDTH + random.randint(0, 250)
        self.rect.y = random.randint(50, 287)
        self.step_index = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, speed):
        self.rect.x -= speed
        if self.step_index >= 36:
            self.step_index = 0

    def draw(self, DISPLAY):
        DISPLAY.blit(self.image, self.rect)


class LargeEnemy(Enemy):
    def __init__(self, image):
        super().__init__(image)


class SmallEnemy(Enemy):
    def __init__(self, image):
        super().__init__(image)

