import random
import sys

from assets.assets import *

pygame.init()
aika = 0
highscore = 0
nopeus = 10
tausta_x = 0
tausta_y = 0


class Sankari:
    X_positio = 300
    Y_positio = 250

    PONNISTUSVOIMA = 14

    def __init__(self, kuva=RUN[0]):

        self.kuva = kuva
        self.sankari_juoksee = True
        self.sankari_hyppaa = False
        self.ponnistusvoima = self.PONNISTUSVOIMA
        self.askel_indeksi = 0
        self.rect = pygame.Rect(self.X_positio, self.Y_positio, kuva.get_width(), kuva.get_height())
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pisteet = 0
        self.viholliset = []
        self.luodit = []

    def paivita(self):
        if self.sankari_juoksee:
            self.juokse()
        if self.sankari_hyppaa:
            self.hyppaa()

        if self.askel_indeksi >= 36:
            self.askel_indeksi = 0

    def juokse(self):
        self.kuva = RUN[self.askel_indeksi // 6]
        self.rect.x = self.X_positio
        self.rect.y = self.Y_positio
        self.askel_indeksi += 1

    def hyppaa(self):
        self.sankari_hyppaa = True
        self.kuva = JUMP[0]
        self.sankari_juoksee = False

        if self.sankari_hyppaa:
            self.rect.y -= self.ponnistusvoima * 2
            self.ponnistusvoima -= 0.8
        if self.ponnistusvoima <= -self.PONNISTUSVOIMA:
            self.sankari_hyppaa = False
            self.sankari_juoksee = True
            self.ponnistusvoima = self.PONNISTUSVOIMA

    def laskeudu(self):
        self.ponnistusvoima -= self.PONNISTUSVOIMA * 0.9

    def piirra(self, DISPLAY):
        DISPLAY.blit(self.kuva, (self.rect.x, self.rect.y))
        # Demoa varten
        #pygame.draw.rect(DISPLAY, self.vari, self.rect)
        for vihollinen in self.viholliset:
            pygame.draw.line(DISPLAY, self.vari, (self.rect.x + 74, self.rect.y + 35), vihollinen.rect.center, 5)

        for luoti in self.luodit:
            luoti.piirra(DISPLAY)
            luoti.paivita(self)


class Vihollinen():
    def __init__(self, kuva=SMALL_ENEMY[0]):
        self.kuva = kuva
        self.rect = self.kuva.get_rect()
        self.rect.x = WIN_WIDTH + random.randint(0, 250)
        self.rect.y = random.randint(50, 287)
        self.askel_indeksi = 0
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def paivita(self, sankari):
        self.kuva = SMALL_ENEMY[self.askel_indeksi // 9]
        self.askel_indeksi += 1

        self.rect.x -= nopeus
        if self.askel_indeksi >= 36:
            self.askel_indeksi = 0
        if self.rect.x < 0:
            sankari.viholliset.pop()

    def piirra(self, DISPLAY):
        DISPLAY.blit(self.kuva, self.rect)
        # Demoa varten
        #pygame.draw.rect(DISPLAY, self.vari, self.rect)

class Luoti():
    def __init__(self, nopeus, x_positio, y_positio, kuva=BULLET):
        self.kuva = kuva
        self.nopeus = nopeus + 2
        self.rect = self.kuva.get_rect()
        self.rect.x = x_positio + 70
        self.rect.y = y_positio + 60
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def paivita(self, sankari):
        self.rect.x += self.nopeus
        if self.rect.x > WIN_WIDTH:
            sankari.luodit.pop(0)

    def piirra(self, DISPLAY):
        DISPLAY.blit(self.kuva, self.rect)


def main():
    global nopeus, highscore, tausta_x, tausta_y, aika, gameover
    gameover = False
    kello = pygame.time.Clock()
    sankari = Sankari()

    def tausta():
        global tausta_x, tausta_y
        kuva_leveys = BG.get_width()
        DISPLAY.blit(BG, (tausta_x, tausta_y))
        DISPLAY.blit(BG, (kuva_leveys + tausta_x, tausta_y))

        if tausta_x <= -kuva_leveys:
            tausta_x = 0
        tausta_x -= nopeus

    def pistelasku():
        luoteja_jaljella = '@' * (5 - len(sankari.luodit))
        enkkateksti = FONT.render(f'ENNATYS   {str(highscore)}', True, (0, 0, 0))
        nopeusteksti = FONT.render(f'NOPEUS {str(nopeus)}', True, (0, 0, 0))
        luodit = FONT.render(f'LUODIT {str(luoteja_jaljella)}', True, (0, 0, 0))
        DISPLAY.blit(enkkateksti, (900, 480))
        DISPLAY.blit(nopeusteksti, (900, 440))
        DISPLAY.blit(luodit, (200, 480))

    def pelilooppi(sankari):
        global highscore
        tarkista_osumat(sankari)
        sankari.paivita()
        sankari.piirra(DISPLAY)

        if len(sankari.viholliset) < 1:
            sankari.viholliset.append(Vihollinen())

        if sankari.pisteet > highscore:
            highscore = sankari.pisteet

    def tarkista_osumat(sankari):
        for vihollinen in sankari.viholliset:
            vihollinen.piirra(DISPLAY)
            vihollinen.paivita(sankari)

            if sankari.rect.colliderect(vihollinen.rect):
                pygame.quit()
                sys.exit()

        for j, luoti in enumerate(sankari.luodit):
            if luoti.rect.colliderect(vihollinen.rect):
                sankari.luodit.pop(j)
                sankari.viholliset.pop(0)
                sankari.pisteet += 1

    while not gameover:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sankari.sankari_hyppaa = True

                if event.key == pygame.K_z and sankari.rect.x is not 300:
                    sankari.laskeudu()

                if event.key == pygame.K_c:
                    if len(sankari.luodit) < 5:
                        sankari.luodit.append(Luoti(nopeus, sankari.rect.x, sankari.rect.y))

        DISPLAY.fill((255, 255, 255))
        tausta()
        pelilooppi(sankari)
        pistelasku()
        aika += 1

        if aika % 200 == 0:
            nopeus += 1
        kello.tick(30)
        pygame.display.update()


if __name__ == '__main__':
    main()
