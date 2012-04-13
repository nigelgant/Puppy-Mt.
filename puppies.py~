#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide, spritecollideany

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

    def __init__(self, loc, state, level_tiles):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.level_tiles = level_tiles

        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.vx = -5
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

    def hitwall(self):
        self.vx *= -1
        self.rect.x += self.vx

    def edge(self):
        self.vx *= -1
        self.rect.x += self.vx

    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def update(self):
        prev_rect = self.rect

        if self.state == 0:
            self.vx = 0
            self.rect.x += self.vx

        if self.state == 1:
            spd = 4 #speed
            self.vx += spd
            if self.vx < spd:
                self.vx = -spd
            if self.vx > spd:
                self.vx = spd
        self.rect.x += self.vx
                 
       # for sprite in self.level_tiles:
        for sprite in self.touches(self.level_tiles):
            rect = sprite.rect
            
            if self.rect.bottom > rect.top:
                if self.rect.right <= rect.left:
                    self.vx *= -1
                   # print "collide right"
                elif self.rect.left >= rect.right:
                    self.vx *= -1
                   # print "collide left"
            if self.rect.bottom <= rect.top:
                if self.rect.right > (rect.right - 2):
                    self.vx *= -1
                    print "edge right"
                elif self.rect.left < (rect.left + 2):
                    self.vx *= -1
                    print "edge left"
    
                    
