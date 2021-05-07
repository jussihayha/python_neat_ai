import math
import os
import random
import sys

import neat
import pygame

pygame.init()
highscore = 0
IKKUNA_KORKEUS = 512
IKKUNA_LEVEYS = 1200

NAYTTO = pygame.display.set_mode((IKKUNA_LEVEYS, IKKUNA_KORKEUS))

JUOKSU = [pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-1.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-2.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-3.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-4.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-5.png'), (128, 128)),
          pygame.transform.scale(pygame.image.load('./assets/sankari-juoksu-6.png'), (128, 128))]

HYPPY = pygame.transform.scale(pygame.image.load('./assets/sankari-hyppy.png'), (96, 96))

PIENI_PUSKA = pygame.transform.scale2x(pygame.image.load('./assets/puska-pieni.png'))
ISO_PUSKA = pygame.transform.scale(pygame.image.load('./assets/puska-suuri.png'), (128, 128))
VIHOLLINEN = [
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu1.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu2.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu3.png'), (96, 96)), True, False),
    pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/vihu4.png'), (96, 96)), True, False)]
TAUSTA = pygame.transform.scale(pygame.image.load('./assets/tausta.png'), (1200, 512))
LUOTI = pygame.transform.scale(pygame.image.load('./assets/ammus.png'), (30, 30))
FONTTI = pygame.font.Font('./assets/gothic_pixel.ttf', 40)


class Sankari:
    X_positio = 300
    Y_positio = 250

    PONNISTUSVOIMA = 12

    def __init__(self, kuva=JUOKSU[0]):
        self.kuva = kuva
        self.sankari_juoksee = True
        self.sankari_hyppaa = False
        self.ponnistusvoima = self.PONNISTUSVOIMA
        self.askel_indeksi = 0
        self.rect = pygame.Rect(self.X_positio, self.Y_positio, kuva.get_width(), kuva.get_height())
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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
        self.sankari_juoksee = False
        self.kuva = HYPPY

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
        pygame.draw.rect(NAYTTO, self.vari, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 5)
        for este in esteet:
            pygame.draw.line(NAYTTO, self.vari, (self.rect.x + 74, self.rect.y + 35), este.rect.topleft, 5)

    def ammu(self, nopeus):
        ammus = Luoti(nopeus, self.X_positio, self.Y_positio)


class Este():
    def __init__(self, kuva, maara):
        self.kuva = kuva
        self.maara = maara
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rect = self.kuva.get_rect()
        self.rect.x = IKKUNA_LEVEYS

    def paivita(self):
        global ge
        self.rect.x -= nopeus
        if self.rect.x < -self.rect.width:
            esteet.pop()

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)
        for este in esteet:
            pygame.draw.rect(NAYTTO, self.vari, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 5)


class PieniPuska(Este):
    def __init__(self, kuva, maara):
        super().__init__(kuva, maara)
        self.rect.y = 320


class IsoPuska(Este):
    def __init__(self, kuva, maara):
        super().__init__(kuva, maara)
        self.rect.y = 250


class Vihollinen():
    def __init__(self, kuva=VIHOLLINEN[0]):
        self.kuva = kuva
        self.rect = self.kuva.get_rect()
        self.rect.x = IKKUNA_LEVEYS + random.randint(0, 100)
        self.rect.y = random.randint(0, 350)
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.askel_indeksi = 0

    def paivita(self, kuva=VIHOLLINEN[0]):
        self.kuva = VIHOLLINEN[self.askel_indeksi // 9]
        self.askel_indeksi += 1

        self.rect.x -= nopeus
        if self.askel_indeksi >= 36:
            self.askel_indeksi = 0
        if self.rect.x < -self.rect.width:
            viholliset.pop()

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)
        RANDOM_VARI = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for vihollinen in viholliset:
            pygame.draw.rect(NAYTTO, self.vari, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 5)


class Luoti():
    def __init__(self, nopeus, x_positio, y_positio, kuva=LUOTI):
        self.kuva = kuva
        self.nopeus = nopeus + 2
        self.rect = self.kuva.get_rect()
        self.rect.x = x_positio + 70
        self.rect.y = y_positio + 60

        print("Testi")

    def paivita(self):
        self.rect.x += self.nopeus
        if self.rect.x > IKKUNA_LEVEYS:
            luodit.pop()

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)


def etaisyys(sankari, este):
    return math.sqrt((sankari[0] - este[0]) ** 2 + (sankari[1] - este[1]) ** 2)


def eval_genomes(genomes, config):
    global nopeus, pisteet, tausta_x, tausta_y, sankarit, ge, nets, esteet, viholliset, highscore, luodit
    kello = pygame.time.Clock()
    pisteet = 0
    tausta_x = 0
    tausta_y = 0
    nopeus = 10
    ge = []
    nets = []
    esteet = []
    viholliset = []
    sankarit = []
    luodit = []

    for genome_id, genome in genomes:
        sankarit.append(Sankari())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def tausta():
        global tausta_x, tausta_y
        kuva_leveys = TAUSTA.get_width()
        NAYTTO.blit(TAUSTA, (tausta_x, tausta_y))
        NAYTTO.blit(TAUSTA, (kuva_leveys + tausta_x, tausta_y))

        if tausta_x <= -kuva_leveys:
            tausta_x = 0
        tausta_x -= nopeus

    def pistelasku():
        global pisteet, nopeus, highscore
        pisteet += 1
        if pisteet % 100 == 0 and nopeus < 30:
            nopeus += 1
        elif pisteet % 100 == 0 and nopeus >= 30:
            nopeus += 2
        pisteteksti = FONTTI.render(f'PISTEET   {str(pisteet)}', True, (0, 0, 0))
        nopeusteksti = FONTTI.render(f'NOPEUS   {str(nopeus)}', True, (0, 0, 0))
        enkkateksti = FONTTI.render(f'ENNATYS   {str(highscore)}', True, (0, 0, 0))
        NAYTTO.blit(pisteteksti, (900, 400))
        NAYTTO.blit(nopeusteksti, (900, 440))
        NAYTTO.blit(enkkateksti, (900, 480))

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sankarit[0].sankari_hyppaa = True

                if event.key == pygame.K_z:
                    sankarit[0].laskeudu()

                if event.key == pygame.K_c:
                    luodit.append(Luoti(nopeus, sankarit[0].rect.x, sankarit[0].rect.y))

        NAYTTO.fill((255, 255, 255))
        tausta()

        for sankari in sankarit:
            sankari.paivita()
            sankari.piirra(NAYTTO)

        if len(sankarit) == 0:
            break

        if len(esteet) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                esteet.append(PieniPuska(PIENI_PUSKA, 2))
            elif rand_int == 1:
                esteet.append(IsoPuska(ISO_PUSKA, 20))

        if len(viholliset) == 0:
            viholliset.append(Vihollinen())

        for este in esteet:
            este.piirra(NAYTTO)
            este.paivita()
            for i, sankari in enumerate(sankarit):
                if sankari.rect.colliderect(este.rect):
                    ge[i].fitness -= 1
                    sankarit.pop(i)
                    ge.pop(i)
                    nets.pop(i)
                else:
                    ge[i].fitness += 1

        for vihollinen in viholliset:
            vihollinen.piirra(NAYTTO)
            vihollinen.paivita()
            for i, sankari in enumerate(sankarit):
                for j, luoti in enumerate(luodit):
                    if luoti.rect.colliderect(vihollinen.rect):
                        print("testi, osui")
                        ge[i].fitness += 1
                        luodit.pop(j)
                        viholliset.pop(0)

                if sankari.rect.colliderect(vihollinen.rect):
                    ge[i].fitness -= 1
                    sankarit.pop(i)
                    ge.pop(i)
                    nets.pop(i)
                else:
                    ge[i].fitness += 1

        def tilastot():
            global sankarit, nopeus, ge
            text_1 = FONTTI.render(f'ELOSSA  {str(len(sankarit))}', True, (0, 0, 0))
            text_2 = FONTTI.render(f'SUKUPOLVI  {pop.generation + 1}', True, (0, 0, 0))

            NAYTTO.blit(text_1, (50, 450))
            NAYTTO.blit(text_2, (50, 480))

        for i, sankari in enumerate(sankarit):
            distance_between_enemy = (
                sankari.rect.y, etaisyys((sankari.rect.x, sankari.rect.y), vihollinen.rect))
            output = nets[i].activate((distance_between_enemy))

            if output[0] > 0.5 and sankari.rect.x == sankari.X_positio:


        if pisteet > highscore:
            highscore = pisteet

        for luoti in luodit:
            luoti.piirra(NAYTTO)
            luoti.paivita()
        pistelasku()
        tilastot()
        kello.tick(30)
        pygame.display.update()


def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    statistiikka = neat.StatisticsReporter()
    pop.add_reporter(statistiikka)
    pop.run(eval_genomes, 100)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
