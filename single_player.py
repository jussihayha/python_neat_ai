import random
import sys

from assets_singleplayer import *

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

    def __init__(self, kuva=JUOKSU[0]):

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
        self.kuva = JUOKSU[self.askel_indeksi // 6]
        self.rect.x = self.X_positio
        self.rect.y = self.Y_positio
        self.askel_indeksi += 1

    def hyppaa(self):
        self.sankari_hyppaa = True
        self.kuva = HYPPY[0]
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

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, (self.rect.x, self.rect.y))
        for vihollinen in self.viholliset:
            pygame.draw.line(NAYTTO, self.vari, (self.rect.x + 74, self.rect.y + 35), vihollinen.rect.center, 5)

        for luoti in self.luodit:
            luoti.piirra(NAYTTO)
            luoti.paivita(self)


class Vihollinen():
    def __init__(self, kuva=VIHOLLINEN[0]):
        self.kuva = kuva
        self.rect = self.kuva.get_rect()
        self.rect.x = IKKUNA_LEVEYS + random.randint(0, 250)
        self.rect.y = random.randint(50, 287)
        self.askel_indeksi = 0
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def paivita(self, sankari, kuva=VIHOLLINEN[0]):
        self.kuva = VIHOLLINEN[self.askel_indeksi // 9]
        self.askel_indeksi += 1

        self.rect.x -= nopeus
        if self.askel_indeksi >= 36:
            self.askel_indeksi = 0
        if self.rect.x < 0:
            sankari.viholliset.pop()

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)


class Luoti():
    def __init__(self, nopeus, x_positio, y_positio, kuva=LUOTI):
        self.kuva = kuva
        self.nopeus = nopeus + 2
        self.rect = self.kuva.get_rect()
        self.rect.x = x_positio + 70
        self.rect.y = y_positio + 60
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def paivita(self, sankari):
        self.rect.x += self.nopeus
        if self.rect.x > IKKUNA_LEVEYS:
            sankari.luodit.pop(0)

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)


def main():
    global nopeus, highscore, tausta_x, tausta_y, aika, gameover
    gameover = False
    kello = pygame.time.Clock()
    sankari = Sankari()

    def tausta():
        global tausta_x, tausta_y
        kuva_leveys = TAUSTA.get_width()
        NAYTTO.blit(TAUSTA, (tausta_x, tausta_y))
        NAYTTO.blit(TAUSTA, (kuva_leveys + tausta_x, tausta_y))

        if tausta_x <= -kuva_leveys:
            tausta_x = 0
        tausta_x -= nopeus

    def pistelasku():
        enkkateksti = FONTTI.render(f'ENNATYS   {str(highscore)}', True, (0, 0, 0))
        nopeusteksti = FONTTI.render(f'NOPEUS {str(nopeus)}', True, (0, 0, 0))
        NAYTTO.blit(enkkateksti, (900, 480))
        NAYTTO.blit(nopeusteksti, (900, 440))

    def pelilooppi(sankari):
        global highscore
        tarkista_osumat(sankari)
        sankari.paivita()
        sankari.piirra(NAYTTO)

        if len(sankari.viholliset) < 1:
            sankari.viholliset.append(Vihollinen())

        if sankari.pisteet > highscore:
            highscore = sankari.pisteet

    def tarkista_osumat(sankari):
        for vihollinen in sankari.viholliset:
            vihollinen.piirra(NAYTTO)
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

                if event.key == pygame.K_z and sankari.rect.x != 300:
                    sankari.laskeudu()

                if event.key == pygame.K_c:
                    sankari.luodit.append(Luoti(nopeus, sankari.rect.x, sankari.rect.y))

        NAYTTO.fill((255, 255, 255))
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
