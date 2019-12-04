import pygame
import numpy as np
import neat
import os
import pickle

pygame.init()

X = 400
Y = 600
win = pygame.display.set_mode((X, Y))

enemy_width = 60
enemy_height = 10
enemy_vel = 20

player_width = 10
player_height = 10
player_vel = 10

tick = 100

pygame.display.set_caption("My Game")


class Player(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # win.blit(pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height)))
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))


class Enemy(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # win.blit(rock, (self.x, self.y))
        pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def is_collided_with(self, player):
        collide = False
        if self.y >= player.y and self.x <= player.x and self.x + self.width >= player.x + player.width:
            collide = True
        if self.y >= player.y and player.x <= self.x <= player.x + player.width:
            collide = True
        if self.y >= player.y and player.x <= self.x + self.width <= player.x + player.width:
            collide = True
        return collide


best_ever = 0


def redrawGameWindow(players, enemies, ge, gen, best):
    global best_ever
    win.fill((0, 0, 0))  # Fills the screen with black
    if best_ever < best:
        best_ever = best
        print(best_ever)

    try:
        font = pygame.font.SysFont("comicsans", 20, True)
        text = font.render('Best score: ' + str(ge[0].fitness), 1, (255, 0, 0))
        win.blit(text, (0, 10))

        font = pygame.font.SysFont("comicsans", 20, True)
        text = font.render('Survivors: ' + str(len(ge)), 1, (255, 0, 0))
        win.blit(text, (0, 30))
    except:
        pass

    font = pygame.font.SysFont("comicsans", 20, True)
    text = font.render('Generation: ' + str(gen), 1, (255, 0, 0))
    win.blit(text, (0, 50))

    font = pygame.font.SysFont("comicsans", 20, True)
    text = font.render('Best score ever: ' + str(best_ever), 1, (255, 0, 0))
    win.blit(text, (0, 70))

    # win.blit(bg, (0, 0))
    for player in players:
        player.draw()

    for enemy in enemies:
        enemy.draw()

    pygame.display.update()


run = True
gen = 0

def main(genomes, config):
    global run, gen
    gen += 1
    enemies = []
    delta = 0
    for i in range(1): # for multiple enemies
        enemies.append(
            Enemy(np.random.randint(-enemy_width, X), -delta, np.random.randint(50, enemy_width), enemy_height,
                  enemy_vel))
        delta += Y // 2

    nets = []
    players = []
    ge = []
    best = 0
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player((X - player_width) // 2, Y - 40, player_width, player_height, player_vel))
        ge.append(genome)

    clock = pygame.time.Clock()

    while run and len(players) > 0:
        clock.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for enemy in enemies:
            enemy.y += enemy.vel
        for x, player in enumerate(players):  # give each bird a fitness of 0.1 for each frame it stays alive
            input = (player.x,
                     enemies[0].x,
                     enemies[0].y,
                     enemies[0].width)
            # enemies[1].x, #for multiple enemies and some tested inputs
            # enemies[1].y,
            # enemies[1].width)
            # X-enemies[0].x)
            # player.x+player_width//2-enemies[0].x-enemies[0].width//2,
            # np.sign(player.x+player_width//2-enemies[0].x)*(player.x+player_width//2-enemies[0].x-enemies[0].width))
            output = nets[players.index(player)].activate(input)

            print("input: ", input)

            if output[0] >= 0.5:
                # player.x -= player.vel
                if player.x - player.vel > 0:
                    player.x -= player.vel
                else:
                    player.x += player.vel

            elif output[0] < 0.5:
                # player.x += player.vel
                if player.x + player.vel + player.width <= X:
                    player.x += player.vel
                else:
                    player.x -= player.vel
            print("Output: ", output)

            for enemy in enemies:
                if enemy.is_collided_with(player):
                    try:
                        nets.pop(players.index(player))
                        ge.pop(players.index(player))
                        players.pop(players.index(player))
                    except:
                        pass
                elif enemy.y > player.y and not enemy.is_collided_with(player):
                    try:
                        ge[x].fitness += 1
                    except:
                        pass
        try:
            if best < ge[0].fitness:
                best = ge[0].fitness
        except:
            pass

        for enemy in enemies:
            if enemy.y >= Y:
                enemy.y = 0
                enemy.x = np.random.randint(-enemy_width, X)
                enemy.width = np.random.randint(50, enemy_width)

        redrawGameWindow(players, enemies, ge, gen, best)
        if best >= 500:
            pickle.dump(nets[0], open("best.pickle", "wb"))
            break


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter())
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1000))
    winner = p.run(main, 5)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
