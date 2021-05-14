import math
import os
import pickle
import sys

import neat

from assets import *
from enemy import Enemy
from hero import Hero

pygame.init()
highscore = 0


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def eval_genomes(genomes, config):
    global speed, points, bg_x, bg_y, heroes, enemies, ge, nets, highscore, pop, obstacles
    clock = pygame.time.Clock()
    points = 0
    bg_x = 0
    bg_y = 0
    speed = 15
    ge = []
    nets = []
    heroes = []
    enemies = []
    obstacles = []
    points = 0

    for genome_id, genome in genomes:
        heroes.append(Hero())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def background():
        global bg_x, bg_y
        BG_WIDTH = BG.get_width()
        DISPLAY.blit(BG, (bg_x, bg_y))
        DISPLAY.blit(BG, (BG_WIDTH + bg_x, bg_y))

        if bg_x <= -BG_WIDTH:
            bg_x = 0
        bg_x -= speed

    def statistics():
        global enemies, speed, ge, pop, points
        points += 1
        heroes_alive = FONT.render(f'ALIVE  {str(len(heroes))}', True, (0, 0, 0))
        try:
            generation_number = FONT.render(f'GENERATION  {pop.generation + 1}', True, (0, 0, 0))
            DISPLAY.blit(heroes_alive, (50, 450))
            DISPLAY.blit(generation_number, (50, 480))
        except NameError:
            pass
        current_points = FONT.render(f'POINTS {str(points)}', True, (0, 0, 0))
        highscore_points = FONT.render(f'HIGHSCORE {str(highscore)}', True, (0, 0, 0))
        game_speed = FONT.render(f'GAME SPEED  {str(speed)}', True, (0, 0, 0))


        DISPLAY.blit(current_points, (900, 450))
        DISPLAY.blit(highscore_points, (900, 480))
        DISPLAY.blit(game_speed, (465, 480))

    def check_collision(hero, index, enemy):
        current_enemy = pygame.sprite.Group(enemy)
        if pygame.sprite.spritecollide(hero, current_enemy, False, pygame.sprite.collide_mask):
            ge[index].fitness -= 10
            heroes.pop(0)
            nets.pop(0)
            ge.pop(0)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255, 255, 255))
        background()

        if len(enemies) == 0:
            enemies.append(Enemy())

        for i, hero in enumerate(heroes):
            hero.update()
            hero.draw(DISPLAY)
            ge[i].fitness += 0.1
            distance_between_enemy_and_hero = distance(hero.rect, enemies[0].rect)
            output = nets[i].activate(
                (speed, hero.rect.x, distance_between_enemy_and_hero))
            if output[0] > 0.5 and hero.rect.x == hero.X_position:
                hero.hero_jumping = True


            if len(enemies) > 0:
                check_collision(hero, i, enemies[0])



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
    statistics = neat.StatisticsReporter()
    pop.add_reporter(statistics)
    winner = pop.run(eval_genomes, 100)

    pickle.dump(winner, open('winner.pkl', 'wb'))

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
        print("Default run 100")
        run(config_path)
    else:
        print("Doing replay")
        replay_genome(config_path)
