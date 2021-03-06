import pygame as pg
from settings import TILESIZE
from collisions import collide_with_walls
from settings import PLAYER_HIT_RECT
from random import randint, normalvariate
from math import floor
import NN.NeuralNetwork as NeuralNetwork
import aStar

vec = pg.math.Vector2


class Person(pg.sprite.Sprite):
    def __init__(self, game, x, y, neuraltype="none", *rest):
        self.groups = game.people
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.person_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.y = y * TILESIZE + 32
        self.rect.x = x * TILESIZE + 32
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.neuralimg = NeuralNetwork.createimg()
        self.predictedtype = NeuralNetwork.predictImg(self.game.net, self.neuralimg)

        if neuraltype != "none":
            while True:
                if self.predictedtype != neuraltype:
                    self.neuralimg = NeuralNetwork.createimg()
                    self.predictedtype = NeuralNetwork.predictImg(self.game.net, self.neuralimg)
                else:
                    break

        if len(rest) == 6:
            self.age = rest[0]
            self.disease = rest[1]
            self.good = rest[2]
            self.lawful = rest[3]
            self.money = rest[4]
            self.gender = rest[5]
        else:
            self.age = randint(0, 50) + randint(0, 25) + randint(0, 25)
            self.disease = randint(0, 10)
            self.good = randint(0, 100)
            self.lawful = randint(0, 100)
            self.money = floor(normalvariate(1000, 500))
            self.gender = randint(0, 1)
        if self.predictedtype == "baby":
            self.age = randint(1, 5)
        elif self.predictedtype == "man":
            self.gender = 0
        elif self.predictedtype == "woman":
            self.gender = 1
        elif self.predictedtype == "boy":
            self.gender = 0
            self.age = randint(10, 20)
        elif self.predictedtype == "girl":
            self.gender = 1
            self.age = randint(10, 20)

    def show(self):
        NeuralNetwork.imshow(self.neuralimg)

    def banish(self):
        self.image = self.game.dead_img
        self.update()
        self.draw(self.game.map_img)

    def update(self):
        self.rect.center = self.pos
        self.pos += self.vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        for i in range(1,4):
            collide_with_walls(self, self.game.walls, 'x', 2)
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y', 2)
            self.rect.center = self.hit_rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def distanceTo(self, person):
        pom = aStar.Astar(self.game, self.pos[0], self.pos[1], person.pos[0], person.pos[1], 1)
        return pom[0].cost
