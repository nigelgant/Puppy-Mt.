#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide, spritecollideany

class Puppy(Sprite):
    size = 22, 15
    def __init__(self):
        pass

class RegPuppy(Puppy):

    def __init__(self, loc, state, level_tiles):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.level_tiles = level_tiles

        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.vx = 5

        self.state = state

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
    
    def update(self, dt, bounds):
        prev_rect = self.rect
        dt = dt / 1000.0

        if self.state == 0:
            self.vx = 0
            self.rect.x += self.vx
            self.color = 205, 133, 63

        if self.state == 1:
            spd = 4 #speed
            self.vx += spd
            if self.vx < spd:
                self.vx = -spd
            if self.vx > spd:
                self.vx = spd
            self.color = 150, 0, 0

        self.image.fill(self.color)

        self.rect.x += self.vx
                 
        for sprite in self.touches(self.level_tiles):
            rect = sprite.rect

            if self.rect.bottom > rect.top:
                if self.rect.right >= (rect.left + 2):
                    self.vx *= -1
                elif self.rect.left <= (rect.right - 2):
                    self.vx *= -1

            elif self.rect.bottom <= rect.top: #on top of tile
                if self.rect.right >= (rect.right - 2):
                    self.vx *= -1
                elif self.rect.left <= (rect.left + 2):
                    self.vx *= -1

            elif self.rect.bottom == rect.bottom and self.rect.top == rect.top: #collide puppies
                if self.rect.right > (rect.right - 2):
                    self.vx *= -1
                elif self.rect.left < (rect.left + 2):
                    self.vx *= -1

                    
class Bouncer(Puppy):
    gravity = 600
    
    def __init__(self, loc, state, height, level_tiles):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.level_tiles = level_tiles
        self.height = height
        self.state = state

        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        rect = self.image.get_rect().inflate(-4,-4)
        
        self.vy = 5
        self.off_ground = True

    def jump(self):
        if not self.off_ground:
            self.off_ground = True
            self.vy = self.height

    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def update(self, dt, bounds):
        dt = dt / 1000.0
        
        self.vy -= dt * self.gravity
        dy = -self.vy * dt
        prev_rect = self.rect
        self.rect = self.rect.move(0, dy)

        if self.state == 2:
            self.color = 150, 0, 0
        if self.state == 3:
            self.vy = 0
            self.color =  205, 133, 63

        self.image.fill(self.color)

        for sprite in self.touches(self.level_tiles):
            rect = sprite.rect

            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                self.vy = 0
                self.rect.bottom = rect.top
                self.off_ground = False
                self.jump()
    
class Fire(Puppy):
    color = 255, 140, 0
    size = 22, 22

    def __init__(self, loc, direction, interval, level_tiles):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.vx, self.vy = direction
        self.direction = direction
        self.vx *= 10
        self.vy *= 10
        self.loc = loc
        self.interval = interval
        self.state = 4
        self.level_tiles = level_tiles
        self.image.fill(self.color)
        self.spawncounter = 0
        print self.interval

        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        
    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def update(self, dt, bounds):
        self.bounds = bounds
        self.spawncounter += 1
        self.rect.x += self.vx
        self.rect.y += self.vy
        prev_rect = self.rect
        
        if self.rect.right > self.bounds.right or self.rect.left < self.bounds.left or self.rect.top < self.bounds.top or self.rect.bottom > self.bounds.bottom:
            if self.spawncounter >= self.interval:
                self.__init__(self.loc, self.direction, self.interval, self.level_tiles)
                self.spawncounter = 0


        for sprite in self.touches(self.level_tiles):
            rect = sprite.rect
            if sprite.state != "tile":  
                self.vx *= -1
                self.vy *= -1

class Gold(Puppy):
    def __init__(self, loc):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.state = 5
        self.color = 255, 215, 0
        self.image.fill(self.color)


    def collected(self):
        self.kill()        
