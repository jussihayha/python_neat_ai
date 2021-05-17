import pygame

pygame.font.init()
WIN_HEIGHT = 512
WIN_WIDTH = 1200

DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("INTELLIGENT HERO AI JUMPING, OK")
# HERO images
RUN = [pygame.transform.scale(pygame.image.load('./assets/hero-run-1.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/hero-run-2.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/hero-run-3.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/hero-run-4.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/hero-run-5.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/hero-run-6.png'), (128, 128))]

JUMP = [pygame.transform.scale(pygame.image.load('./assets/hero-jump-1.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/hero-jump-1.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/hero-jump-2.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/hero-jump-2.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/hero-jump-3.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/hero-jump-3.png'), (128, 128))
        ]

# ENEMY PICTURES
SMALL_ENEMY = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy1.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy2.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy3.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy4.png'), (96, 96)), True, False)]

LARGE_ENEMY = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy1.png'), (240, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy2.png'), (240, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy3.png'), (240, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/enemy4.png'), (240, 96)), True, False)]

# RANDOM VARIABLES
BG = pygame.transform.scale(pygame.image.load('./assets/background.png'), (1200, 512))
BULLET = pygame.transform.scale(pygame.image.load('./assets/bullet.png'), (30, 30))
FONT = pygame.font.Font('./assets/gothic_pixel.ttf', 40)
