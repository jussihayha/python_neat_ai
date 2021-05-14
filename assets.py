import pygame

pygame.font.init()
WIN_HEIGHT = 512
WIN_WIDTH = 1200

DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("INTELLIGENT HERO AI JUMPING, OK")
# HERO images
RUN = [pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-1.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-2.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-3.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-4.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-5.png'), (128, 128)),
       pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-6.png'), (128, 128))]

JUMP = [pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-1.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-1.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-2.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-2.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-3.png'), (128, 128)),
        pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-3.png'), (128, 128))
        ]

# ENEMY PICTURES
ENEMY = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu1.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu2.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu3.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu4.png'), (96, 96)), True, False)]

# RANDOM VARIABLES
BG = pygame.transform.scale(pygame.image.load('./assets/tausta.png'), (1200, 512))
BULLET = pygame.transform.scale(pygame.image.load('./assets/ammus.png'), (30, 30))
FONT = pygame.font.Font('./assets/gothic_pixel.ttf', 40)
