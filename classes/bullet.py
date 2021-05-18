from assets.assets import *



class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, x_position, y_position, image=BULLET):
        super().__init__()
        self.image = image
        self.speed = speed + 2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x_position + 70
        self.rect.y = y_position + 60

    def update(self, hero):
        self.rect.x += self.speed


    def draw(self, DISPLAY):
        DISPLAY.blit(self.image, self.rect)