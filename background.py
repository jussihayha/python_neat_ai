from assets import *


class Background:
    X_position = 50
    Y_position = 250

    def __init__(self, image=BG):
        self.image = image
        self.width = self.image.get_width()
        self.rect = image.get_rect()

    def draw(self, DISPLAY, speed):
        DISPLAY.blit(self.image, (self.rect.x, self.rect.y))
        DISPLAY.blit(self.image, (self.width + self.rect.x, self.rect.y))

        if self.rect.x <= -self.width:
            self.rect.x = 0
        self.rect.x -= speed
