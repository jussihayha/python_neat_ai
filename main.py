import argparse
import math
import os
import pickle
import sys

import neat

from assets import *
from background import Background
from enemy import Enemy
from hero import Hero

pygame.init()
highscore = 0


# def statistics(enemies, speed, ge, pop, points):
#     heroes_alive = FONT.render(f'ALIVE  {str(len(heroes))}', True, (0, 0, 0))
#     try:
#         generation_number = FONT.render(f'GENERATION  {pop.generation + 1}', True, (0, 0, 0))
#         DISPLAY.blit(heroes_alive, (50, 450))
#         DISPLAY.blit(generation_number, (50, 480))
#     except NameError:
#         pass
#     current_points = FONT.render(f'POINTS {str(points)}', True, (0, 0, 0))
#     highscore_points = FONT.render(f'HIGHSCORE {str(highscore)}', True, (0, 0, 0))
#     game_speed = FONT.render(f'GAME SPEED  {str(speed)}', True, (0, 0, 0))
#
#     DISPLAY.blit(current_points, (900, 450))
#     DISPLAY.blit(highscore_points, (900, 480))
#     DISPLAY.blit(game_speed, (465, 480))





def eval_genomes(genomes, config):

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game(genome, net)

class Game:
    def __init__(self, genome, net):
        self.speed = 14
        self.points = 0
        self.bg_x = 0
        self.bg_y = 0
        self.hero = Hero()
        self.enemies = []
        self.genome = genome
        self.net = net
        self.highscore = 0
        self.pop = pop
        self.clock = pygame.time.Clock()
        self.background = Background()



    def check_collision(hero, index, enemy):
        current_enemy = pygame.sprite.Group(enemy)
        if pygame.sprite.spritecollide(hero, current_enemy, False, pygame.sprite.collide_mask):
            genome.fitness -= 10
            run = False
        else:
            ge[index].fitness += 0.2

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255, 255, 255))
        background.draw(DISPLAY, speed)

        if len(enemies) == 0:
            enemies.append(Enemy())

        hero.update()
        hero.draw(DISPLAY, enemies)

        distance_between_enemy = distance((hero.rect.x, hero.rect.y), (enemies[0].rect.x, enemies[0].rect.y))
        output = nets[i].activate((speed, distance_between_enemy, enemies[0].rect.y, hero.rect.y))

        if output[0] > 0.5:
            hero.hero_jumping = True

        if len(enemies) == 0:
            amount_of_enemies = random.randint(0, 1)

            if amount_of_enemies == 0:
                enemies.append(LargeEnemy(image=LARGE_ENEMY[0]))

            else:
                enemies.append(SmallEnemy(image=SMALL_ENEMY[0]))

        if len(heroes) == 0:
            break

        for enemy in enemies:
            enemy.update(speed)
            enemy.draw(DISPLAY)
            if enemy.rect.x < 0:
                enemies.pop(0)

        if points % 100 == 0:
            speed += 1
        if points > highscore:
            highscore = points
        points += 1
#        statistics()
        clock.tick(30)
        pygame.display.update()


def run(config_path, generations):
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
    statistics = neat.StatisticsReporter()
    pop.add_reporter(statistics)
    winner = pop.run(eval_genomes, generations)

    pickle.dump(winner, open(f'winner_{generations}.pkl', 'wb'))


def replay_genome(config_path, filename):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(filename, 'rb') as file:
        genome = pickle.load(file)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]
    eval_genomes(genomes, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--train', action='store_true')
    group.add_argument('--replay', action='store_true')
    parser.add_argument('arg', help='example: --train 100 or --replay winner.pkl')
    args = parser.parse_args()

    if args.train:
        generations = args.arg
        print(f'Training for {generations} generations')
        run(config_path, int(generations))

    elif args.replay:
        filename = args.arg
        replay_genome(config_path, filename)
