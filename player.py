#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide
from levels import Tile

class Player(Sprite):
    size = 12, 24
    color = 0, 0, 255


    def __init__(self, loc, bounds):
        Sprite.__init__(self)

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

        self.rect.center = loc #where player respawns?
        self.bounds = bounds

        self.image.fill(self.color)
        self.off_ground = True
        self.vx = 0
        self.vy = 0

    def jump(self):
        keystate =  pygame.key.get_pressed()
        if self.off_ground == False:
            self.vy = -3
            self.vx *= 0.3
            self.off_ground = True

    def update(self):
        keystate = pygame.key.get_pressed()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.off_ground:
            self.vy += 0.2
            if keystate[K_RIGHT]:
                if self.vx < 10:
                    self.vx += 0.5
                else:
                    self.vx = 10
            if keystate[K_LEFT]:
                if self.vx > -10:
                    self.vx -= 0.5
                else:
                    self.vx = -10
          #  if self.vy > 0:
           #     self.vy *= 1.2
            if keystate[K_DOWN]:  #thurst down while mid-air
                if self.vy < 0:
                    self.vy *= -1
                self.vy *= 1.5
        if not self.off_ground:
            self.walk()

    def land(self):
        self.vy = 0
        self.off_ground = False
    def hitwall(self):
        self.vx = 0
        self.off_ground = True
    def fall(self):
        self.off_ground = True 

    def walk(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT] and keystate[K_LEFT]:
            pass
        elif keystate[K_RIGHT]:
            self.vx = 7  #move right
        elif keystate[K_LEFT]:
            self.vx = -7  #move left
        elif not self.off_ground:
            self.vx = 0
