import random
import sys

from assets.assets import *
from classes.background import Background
from classes.bullet import Bullet
from classes.enemy import LargeEnemy, SmallEnemy
from classes.hero import Hero

highscore = 0


class Game:

    def __init__(self, genome, net, index, pop, replaymode):
        self.speed = 14
        self.points = 0
        self.bg_x = 0
        self.bg_y = 0
        self.enemies = []
        self.bullets = []
        self.genome = genome
        self.net = net
        self.pop = pop
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.alive = True
        self.hero = Hero()
        self.index = index
        self.replaymode = replaymode
        self.enemies_hit = 0
        self.enemies_missed = 0

    def play(self):
        global highscore
        run = True

        while run:
            # Run while hero is alive
            if not self.hero.alive:
                break
            elif self.points > 8000:
                self.genome.fitness += 25
                break
            else:
                self.genome.fitness += 0.015

            # Basic for loop in Pygame for enabling closing window from X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.background.draw(self.speed)
            self.spawn_enemy()
            self.hero.draw()
            self.hero.update()
            self.get_hero_action()

            for enemy in self.enemies:
                enemy.update(self.speed)
                enemy.draw(DISPLAY)
                # Check if enemy has collided with hero
                self.check_collision(enemy)
                # If enemy has passed the screen, give fitness to genome, and pop the enemy
                if enemy.rect.x < 0:
                    self.genome.fitness += 0.02
                    self.enemies.pop(0)

            for bullet in self.bullets:
                bullet.update(self.speed)
                bullet.draw(DISPLAY)
                # Check if bullet hits enemy
                self.check_shot_enemy(bullet)
                # If bullet has passed screen -> remove bullet and give negative fitness
                if bullet.rect.x > 1200:
                    self.enemies_missed += 1
                    self.genome.fitness -= 0.02
                    self.bullets.pop(0)

            self.check_highscore_and_add_speed()
            self.points += 1
            self.statistics()
            self.clock.tick(30)
            pygame.display.update()

    def spawn_enemy(self):
        if len(self.enemies) == 0:
            amount_of_enemies = random.randint(0, 1)

            if amount_of_enemies == 0:
                self.enemies.append(LargeEnemy(image=LARGE_ENEMY[0]))

            else:
                self.enemies.append(SmallEnemy(image=SMALL_ENEMY[0]))

    def get_hero_action(self):
        # Calculate distance between enemy and hero
        distance_between_enemy = self.hero.distance((self.enemies[0].rect.x, self.enemies[0].rect.y))
        hero_position = self.hero.rect
        enemy_position = self.enemies[0].rect
        # inputs are:
        # speed of the game
        # distance between enemy and hero
        # enemy y-position
        # hero y-position
        # amount of bullets on the screen
        output = self.net.activate(
            (self.speed, distance_between_enemy, hero_position.x, enemy_position.x, hero_position.y, enemy_position.y, len(self.bullets)))

        if output[0] > 0.5:
            self.hero.hero_jumping = True
        # FIXME: This logic should not be defined here.
        if output[1] > 0.5 and len(self.bullets) < 5:
            self.bullets.append(Bullet(self.speed, self.hero.rect.x, self.hero.rect.y))

    def check_highscore_and_add_speed(self):
        global highscore
        if self.points % 100 == 0:
            self.speed += 1
        if self.points > highscore:
            highscore = self.points

    def check_shot_enemy(self, bullet):

        if len(self.enemies) > 0:
            current_enemy = pygame.sprite.Group(self.enemies[0])

            if pygame.sprite.spritecollide(bullet, current_enemy, False, pygame.sprite.collide_mask):
                self.genome.fitness += 0.5
                self.enemies_hit += 1
                self.enemies.pop(0)
                self.bullets.pop(0)
                bullet.kill()

    def check_collision(self, enemy):
        current_enemy = pygame.sprite.Group(enemy)
        if pygame.sprite.spritecollide(self.hero, current_enemy, False, pygame.sprite.collide_mask):
            self.genome.fitness -= 10
            self.hero.alive = False

    def statistics(self):
        if not self.replaymode:
            hero_number = FONT.render(f'HERO  {str(self.index)} OUT OF {str(len(self.pop.population))}', True,
                                      (0, 0, 0))
            generation_number = FONT.render(f'GENERATION  {str(self.pop.generation + 1)}', True, (0, 0, 0))
            DISPLAY.blit(hero_number, (50, 450))
            DISPLAY.blit(generation_number, (50, 480))

        shot_enemies = FONT.render(f'HIT {str(self.enemies_hit)}', True, (0, 0, 0))
        missed_enemies = FONT.render(f'MISSED {str(self.enemies_missed)}', True, (0, 0, 0))
        # Add miss%
        current_points = FONT.render(f'POINTS {str(self.points)}', True, (0, 0, 0))
        highscore_points = FONT.render(f'HIGHSCORE {str(highscore)}', True, (0, 0, 0))

        game_speed = FONT.render(f'GAME SPEED  {str(self.speed)}', True, (0, 0, 0))

        DISPLAY.blit(missed_enemies, (900, 390))
        DISPLAY.blit(shot_enemies, (900, 420))
        DISPLAY.blit(current_points, (900, 450))
        DISPLAY.blit(highscore_points, (900, 480))
        DISPLAY.blit(game_speed, (465, 480))
