import argparse
import os
import pickle

import neat

from classes.game import Game


def eval_genomes(genomes, config):
    global pop
    index = 0

    for genome_id, genome in genomes:
        index += 1
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        if len(genomes) == 1:
            pop = neat.Population(config)
            game = Game(genome, net, index, pop, replaymode=True)
        else:
            game = Game(genome, net, index, pop, replaymode=False)
        game.play()
        print(genome.fitness)



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
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    winner = pop.run(eval_genomes, generations)
    print('\nBest genome:\n{!s}'.format(winner))
    pickle.dump(winner, open(f'./models/winner_{generations}.pkl', 'wb'))


def replay_genome(config_path, filename):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    with open(f'./models/{filename}', 'rb') as file:
        genome = pickle.load(file)

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
