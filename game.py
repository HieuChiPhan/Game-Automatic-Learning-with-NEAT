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


def redrawGameWindow(player, enemy, score, gameover):
    win.fill((0, 0, 0))  # Fills the screen with black
    # if best_ever < best:
    #     best_ever = best
    #     print(best_ever)
    #
    # try:
    #     font = pygame.font.SysFont("comicsans", 20, True)
    #     text = font.render('Your score: ' + str(ge[0].fitness), 1, (255, 0, 0))
    #     win.blit(text, (0, 10))
    #
    #     font = pygame.font.SysFont("comicsans", 20, True)
    #     text = font.render('Survivors: ' + str(len(ge)), 1, (255, 0, 0))
    #     win.blit(text, (0, 30))
    # except:
    #     pass
    font = pygame.font.SysFont("comicsans", 20, True)
    font2 = pygame.font.SysFont("comicsans", 40, True)
    if not gameover:

        text = font.render('Your score: ' + str(score), 1, (255, 255, 255))
        win.blit(text, (0, 10))
        player.draw()
        enemy.draw()
    else:
        text = font2.render("Game over", 10, (255, 0, 0))
        win.blit(text, (X//2-80, Y//2))


    pygame.display.update()


run = True
gameover=False
score=0

enemies = []
delta = 0
for i in range(1): # for multiple enemies
    enemies.append(
        Enemy(np.random.randint(-enemy_width, X), -delta, np.random.randint(50, enemy_width), enemy_height,
              enemy_vel))
    delta += Y // 2


player = Player((X - player_width) // 2, Y - 40, player_width, player_height, player_vel)
enemy=Enemy(np.random.randint(-enemy_width, X), 0, np.random.randint(50, enemy_width), enemy_height, enemy_vel)
clock = pygame.time.Clock()

while run:
    clock.tick(tick)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    enemy.y += enemy.vel

    if keys[pygame.K_LEFT] and player.x >= 0:
        player.x -= player.vel
    if keys[pygame.K_RIGHT] and player.x + player.width < X:
        player.x += player.vel

    if enemy.is_collided_with(player):
        gameover=True
    elif enemy.y > player.y and not enemy.is_collided_with(player):
        score += 1

    if enemy.y >= Y:
        enemy.y = 0
        enemy.x = np.random.randint(-enemy_width, X)
        enemy.width = np.random.randint(50, enemy_width)

    redrawGameWindow(player, enemy, score, gameover)




