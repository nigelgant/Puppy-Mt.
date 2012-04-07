#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide

class Puppy(Sprite):
    
    def __init__(self):
        pass
    #    Sprite.__init__(self)

     #   self.rect = self.image.get_rect()
      #  self.rect.bottom = loc
      #  self.vx = 0
      #  self.vy = 0

class RegPuppy(Puppy):
    size = 16, 12

    def __init__(self, loc, state):
        Sprite.__init__(self)
        self.image = Surface(self.size)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.vx = 0
        self.vy = 0

        self.state = state

        if self.state == 0:
            self.color = 205, 133, 63
        if self.state == 1:
            self.color = 150, 0, 0
        self.image.fill(self.color)

    def anger(self):
        self.state = 1

    def pacify(self):
        self.state = 0

    def update(self):
        self.rect.y += self.vy

        if self.state == 0:
            self.vx = 0
            self.rect.x += self.vx

        if self.state == 1:
            self.vx += 2
            if self.vx < 2:
                self.vx = -2
            if self.vx > 2:
                self.vx = 2
        self.rect.x += self.vx
            
    def hitwall(self):
        self.vx *= -1
        self.rect.x += self.vx

    def edge(self):
        self.vx *= -1
        print "reach edge"
        self.rect.x += self.vx


        
