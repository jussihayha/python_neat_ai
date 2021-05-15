import pygame

pygame.font.init()
IKKUNA_KORKEUS = 512
IKKUNA_LEVEYS = 1200

NAYTTO = pygame.display.set_mode((IKKUNA_LEVEYS, IKKUNA_KORKEUS))

# Sankarin kuvat
JUOKSU = [pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-1.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-2.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-3.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-4.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-5.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-6.png'), (128, 128))]

HYPPY = [pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-1.png'), (128, 128)),
         pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-1.png'), (128, 128)),
         pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-2.png'), (128, 128)),
         pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-2.png'), (128, 128)),
         pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-3.png'), (128, 128)),
         pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy-3.png'), (128, 128))
         ]

# Vihollisen kuvat
VIHOLLINEN = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu1.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu2.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu3.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu4.png'), (96, 96)), True, False)]

# Loput kuvat
TAUSTA = pygame.transform.scale(pygame.image.load('assets/background.png'), (1200, 512))
LUOTI = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (30, 30))
FONTTI = pygame.font.Font('./assets/gothic_pixel.ttf', 40)