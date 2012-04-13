#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide, spritecollideany
from levels import Tile

class Player(Sprite):
    size = 12, 24
    color = 0, 0, 255
    playerspeed = 200
    gravity = 600

    def __init__(self, loc, level):
        Sprite.__init__(self)
        
        self.level = level
        self.spawnpoint = loc

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        
        self.image.fill(self.color)
        rect = self.image.get_rect().inflate(-4,-4) #what does this do?
        self.image.fill(self.color, rect)
        
        self.vx = 0
        self.vy = 0
        self.off_ground = True

        self.playerlvl = level.levelnum

    def jump(self):
        if not self.off_ground:
            self.off_ground = True
            self.vy = 200 #jump speed
            self.vx *= 0.2
            
    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def die(self):
        #insert dying animation
        self.level.reset()
        self.__init__(self.spawnpoint, self.level)

    def reset(self):
        self.level.reset()
        self.__init__(self.spawnpoint, self.level)

    def endlevel(self):
        self.playerlvl += 1
        print self.playerlvl
        self.rect.center = self.spawnpoint
    
    def update(self, dt):
        dt = dt / 1000.0
        keystate = pygame.key.get_pressed()

        self.vx = 0
        if keystate[K_LEFT]:
            self.vx -= self.playerspeed
        if keystate[K_RIGHT]:
            self.vx += self.playerspeed

        self.vy -= dt * self.gravity
        dx = self.vx * dt
        dy = -self.vy * dt

        #update position
        prev_rect = self.rect
        self.rect = self.rect.move(dx, dy)

        self.off_ground = True

        for sprite in self.touches(self.level.tiles):
            rect = sprite.rect

            #collide walls
            if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                self.rect.left = rect.right
            if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                self.rect.right = rect.left
            #collide ceilings
            if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
                self.vy /= 2.0 #half speed
                self.rect.top = rect.bottom
                
            #land
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                self.vy = 0
                self.rect.bottom = rect.top
                self.off_ground = False
            
        #collide doors
        for sprite in self.touches(self.level.door):
       # if spritecollideany(self, self.level.door):
            print "collide door"
            if self.playerlvl == self.level.levelnum:
                self.endlevel()
    

        for sprite in self.touches(self.level.pups):
            rect = sprite.rect
            for RegPuppy in self.touches(self.level.pups):
                if RegPuppy.state == 0:
                #collide top of regpuppy
                    if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top: 
                        self.vy = 0
                        self.rect.bottom = rect.top
                        self.off_ground = False

                #collide side of regpuppy:
                    if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                        self.rect.left = rect.right
                    if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                        self.rect.right = rect.left
                    
                if RegPuppy.state == 1:
                    self.die()

            
                
