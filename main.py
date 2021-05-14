import os
import pickle
import random
import sys

import neat
import pygame.sprite

from assets import *

pygame.init()


class Hero(pygame.sprite.Sprite):
    X_position = 300
    Y_position = 250

    VELOCITY = 14

    def __init__(self, image=RUN[0]):

        self.image = image
        self.hero_running = True
        self.hero_jumping = False
        self.velocity = self.VELOCITY
        self.step_index = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


    def update(self):
        if self.hero_running:
            self.run()
        if self.hero_jumping:
            self.jump()

        if self.step_index >= 36:
            self.step_index = 0

    def run(self):
        self.image = RUN[self.step_index // 6]
        self.rect.x = self.X_position
        self.rect.y = self.Y_position
        self.step_index += 1

    def jump(self):
        self.hero_jumping = True
        self.image = JUMP[0]
        self.hero_running = False

        if self.hero_jumping:
            self.rect.y -= self.velocity * 2
            self.velocity -= 0.8
        if self.velocity <= -self.VELOCITY:
            self.hero_jumping = False
            self.hero_running = True
            self.velocity = self.VELOCITY

    def stomp(self):
        self.velocity -= self.VELOCITY * 0.9

    def draw(self, DISPLAY):
        DISPLAY.blit(self.image, (self.rect.x, self.rect.y))



class Enemy(pygame.sprite.Sprite):
    def __init__(self, amount=1, image=ENEMY[0]):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = WIN_WIDTH
        self.rect.y = 300
        self.step_index = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.amount = amount

    def update(self, image=ENEMY[0]):
        self.image = ENEMY[self.step_index // 9]
        self.step_index += 1

        self.rect.x -= speed
        if self.step_index >= 36:
            self.step_index = 0
        if self.rect.x < 0:
            enemies.pop()

    def draw(self, DISPLAY):
        for i in range(self.amount):
            DISPLAY.blit(self.image, self.rect )


def eval_genomes(genomes, config):
    global speed, points, bg_x, bg_y, heroes, enemies, ge, nets, highscore
    clock = pygame.time.Clock()
    points = 0
    bg_x = 0
    bg_y = 0
    speed = 15
    ge = []
    nets = []
    heroes = []
    enemies = []
    highscore = 0
    for genome_id, genome in genomes:
        heroes.append(Hero())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def background():
        DISPLAY.blit(BG, (0, 0))

    def point_function():
        current_points = FONT.render(f'POINTS {str(points)}', True, (0, 0, 0))
        highscore_points = FONT.render(f'HIGHSCORE {str(highscore)}', True, (0, 0, 0))
        DISPLAY.blit(current_points, (900, 450))
        DISPLAY.blit(highscore_points, (900, 480))

    def statistics():
        global enemies, speed, ge
        text_1 = FONT.render(f'ALIVE  {str(len(heroes))}', True, (0, 0, 0))
        text_2 = FONT.render(f'GENERATION  {pop.generation + 1}', True, (0, 0, 0))

        DISPLAY.blit(text_1, (50, 450))
        DISPLAY.blit(text_2, (50, 480))

    def check_collision(hero, enemy):

        if pygame.sprite.spritecollide(hero, enemy, False, pygame.sprite.collide_mask):
            heroes.pop(0)



    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255, 255, 255))
        background()

        if len(enemies) == 0:
            amount = random.randint(0, 2)

            if amount == 1:
                enemies.append(pygame.sprite.Group(Enemy(1)))
            elif amount == 2:
                enemies.append(pygame.sprite.Group(Enemy(2)))
            else:
                enemies.append(pygame.sprite.Group(Enemy(3)))

        for enemy in enemies:
            enemy.draw(DISPLAY)
            enemy.update()

        for i, hero in enumerate(heroes):
            hero.update()
            hero.draw(DISPLAY)

            if len(enemies) > 0:
                check_collision(hero, enemies[0])


        if len(heroes) == 0:
            break

        for i, hero in enumerate(heroes):

            output = nets[i].activate((dinosaur.rect.y,
                                       distance((dinosaur.rect.x, dinosaur.rect.y),
                                        obstacle.rect.midtop)))
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        if points > highscore:
            highscore = points
        point_function()
        statistics()
        clock.tick(30)
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
    winner = pop.run(eval_genomes, 5)

    pickle.dump(winner, open('winner.pkl', 'wb'))

    visualize.plot_stats(pop.statistics)
    visualize.plot_species(pop.statistics)
    visualize.draw_net(winner, view=True, filename="xor2-all.gv")
    visualize.draw_net(winner, view=True, filename="xor2-enabled.gv", show_disabled=False)
    visualize.draw_net(winner, view=True, filename="xor2-enabled-pruned.gv", show_disabled=False, prune_unused=True)
    statistics.save_stats(pop.statistics)
    statistics.save_species_count(pop.statistics)
    statistics.save_species_fitness(pop.statistics)


# https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]
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
