#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group

class Player(Sprite):
    size = 24, 48
    color = 0, 0, 255

    def __init__(self, loc, bounds):
        Sprite.__init__(self)

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

        self.rect.center = loc #where player respawns?
        self.bounds = bounds

        self.image.fill(self.color)
        self.off_ground = False
        self.vx = 0
        self.vy = 0

    def jump(self):
        keystate =  pygame.key.get_pressed()
        if self.off_ground == False:
            self.vy = -6
            self.vx *= 0.5
            self.off_ground = True

    def update(self):
        keystate = pygame.key.get_pressed()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.off_ground:
            self.vy += 0.2
            if keystate[K_RIGHT]:
                while self.vx <= 0:
                    self.vx += 0.7
            if keystate[K_LEFT]:
                while self.vx >= 0:
                    self.vx -= 0.7
        if not self.off_ground:
            self.walk()
        if self.rect.bottom >= 200:
            self.vy = 0
            self.off_ground = False

    def walk(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT] and keystate[K_LEFT]:
            pass
        elif keystate[K_RIGHT]:
            self.vx = 10  #move right
        elif keystate[K_LEFT]:
            self.vx = -10  #move left
        elif not self.off_ground:
            self.vx = 0

