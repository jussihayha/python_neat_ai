import math
import os
import random
import sys
import pickle
import neat

from assets import *

pygame.init()

highscore = 0


class Sankari:
    X_positio = 300
    Y_positio = 250

    PONNISTUSVOIMA = 14

    def __init__(self, kuva=JUOKSU[0]):
        self.viholliset = []
        self.luodit = []
        self.kuva = kuva
        self.sankari_juoksee = True
        self.sankari_hyppaa = False
        self.ponnistusvoima = self.PONNISTUSVOIMA
        self.askel_indeksi = 0
        self.rect = pygame.Rect(self.X_positio, self.Y_positio, kuva.get_width(), kuva.get_height())
        self.vari = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pisteet = pisteet

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
        NAYTTO.blit(self.kuva, (self.rect.x, self.rect.y))
        for vihollinen in self.viholliset:
            pygame.draw.line(NAYTTO, self.vari, (self.rect.x + 74, self.rect.y + 35), vihollinen.rect.center, 5)


class Vihollinen():
    def __init__(self, kuva=VIHOLLINEN[0]):
        self.kuva = kuva
        self.rect = self.kuva.get_rect()
        self.rect.x = IKKUNA_LEVEYS + random.randint(0, 100)
        self.rect.y = random.randint(0, 512)
        self.askel_indeksi = 0

    def paivita(self, sankari, kuva=VIHOLLINEN[0], ):
        self.kuva = VIHOLLINEN[self.askel_indeksi // 9]
        self.askel_indeksi += 1

        self.rect.x -= nopeus
        if self.askel_indeksi >= 36:
            self.askel_indeksi = 0
        if self.rect.x < -self.rect.width:
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

    def paivita(self, sankari):
        self.rect.x += self.nopeus
        if self.rect.x > IKKUNA_LEVEYS:
            sankari.luodit.pop(0)

    def piirra(self, NAYTTO):
        NAYTTO.blit(self.kuva, self.rect)


def paivita_luodit(sankari):
    for luoti in sankari.luodit:
        luoti.piirra(NAYTTO)
        luoti.paivita(sankari)


def tarkista_osumat(sankari):
    for vihollinen in sankari.viholliset:
        vihollinen.piirra(NAYTTO)
        vihollinen.paivita(sankari)
        for i, sankari in enumerate(sankarit):
            for j, luoti in enumerate(sankari.luodit):
                if luoti.rect.colliderect(vihollinen.rect) and len(sankari.viholliset) > 0:
                    ge[i].fitness += 1
                    sankari.luodit.pop(0)
                    sankari.viholliset.pop(0)
                    sankari.pisteet += 1

            if sankari.rect.colliderect(vihollinen.rect):
                ge[i].fitness -= 10
                sankari.alive = False
                sankarit.pop(i)
                ge.pop(i)
                nets.pop(i)



def hae_komennot(sankari, i):
    def etaisyys(sankari):

        if len(sankari.viholliset) == 0:
            pass
        else:
            return math.sqrt((sankari.rect.x - sankari.viholliset[0].rect.x) ** 2 + (
                        sankari.rect.y - sankari.viholliset[0].rect.y) ** 2)

    for i, sankari in enumerate(sankarit):

        distance_between_enemy = (
            sankari.rect.y, etaisyys(sankari))


        if distance_between_enemy[1] == None:
            pass
        else:

            output = nets[i].activate((distance_between_enemy))

            if output[0] > 0.5 and len(sankari.luodit) < 1:
                sankari.luodit.append(Luoti(nopeus, sankari.rect.x, sankari.rect.y))
            if output[1] > 0.5 and sankari.rect.x == sankari.X_positio:
                sankari.sankari_hyppaa = True


def eval_genomes(genomes, config):
    global nopeus, pisteet, tausta_x, tausta_y, sankarit, ge, nets, highscore, luodit
    kello = pygame.time.Clock()
    pisteet = 0
    tausta_x = 0
    tausta_y = 0
    nopeus = 20
    ge = []
    nets = []

    sankarit = []

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

        enkkateksti = FONTTI.render(f'ENNATYS   {str(highscore)}', True, (0, 0, 0))
        NAYTTO.blit(enkkateksti, (900, 480))

    def tilastot():
        global sankarit, nopeus, ge
        text_1 = FONTTI.render(f'ELOSSA  {str(len(sankarit))}', True, (0, 0, 0))
        text_2 = FONTTI.render(f'SUKUPOLVI  {pop.generation + 1}', True, (0, 0, 0))

        NAYTTO.blit(text_1, (50, 450))
        NAYTTO.blit(text_2, (50, 480))

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sankarit[0].sankari_hyppaa = True

                if event.key == pygame.K_z and sankarit[0].rect.x != 300:
                    sankarit[0].laskeudu()

                if event.key == pygame.K_c:
                    sankarit[0].luodit.append(Luoti(nopeus, sankarit[0].rect.x, sankarit[0].rect.y))

        NAYTTO.fill((255, 255, 255))
        tausta()

        for i, sankari in enumerate(sankarit):
            sankari.paivita()
            sankari.piirra(NAYTTO)

            if len(sankari.viholliset) < 1:
                sankari.viholliset.append(Vihollinen())
            paivita_luodit(sankari)
            tarkista_osumat(sankari)
            hae_komennot(sankari, i)

            if sankari.pisteet > highscore:
                highscore = sankari.pisteet

        if len(sankarit) == 0:
            break

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
    winner = pop.run(eval_genomes, 1000)
    pickle.dump(winner, open('winner.pkl', 'wb'))

def replay_genome(config_path, genome_path="winner.pkl"):
    global pop
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    eval_genomes(genomes, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    if len(sys.argv) < 2:
        print("normal run")
        run(config_path)
    else:
        print("Doing replay")
        replay_genome(config_path)
