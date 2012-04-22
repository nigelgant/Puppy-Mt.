#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide, spritecollideany
from levels import Tile
from resources import load_image
from spritesheet import SpriteSheet
from anim import Animation

class Player(Sprite):
    size = 18, 34
    color = 0, 0, 255
    playerspeed = 200
    gravity = 600

    def __init__(self, loc, level, bounds):
        Sprite.__init__(self)
        
        self.facing = "right"  #facing right

        self.level = level
        self.spawnpoint = loc
        self.bounds = bounds

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        
        self.image.fill(self.color)
        rect = self.image.get_rect().inflate(-4,-4) #what does this do?
        self.image.fill(self.color, rect)
        
        self.vx = 0
        self.vy = 0
        self.off_ground = True
        self.waves = Group() #soundwaves
        self.treats = Group() #dog treats
        self.whistlecount = 0
        self.treatcount = 0

        self.playerlvl = level.levelnum

    def jump(self):
        if not self.off_ground:
            self.off_ground = True
            self.vy = 260 #jump speed
    

    def whistle(self):
        if self.whistlecount < self.level.wlimit and self.level.wlimit > 0:
            soundwave = Wave(self.bounds, self.level, self.facing)
            if self.facing == "right":
                soundwave.rect.left = self.rect.right
                soundwave.rect.midleft = self.rect.midright
            elif self.facing == "left":
                soundwave.rect.right = self.rect.left
                soundwave.rect.midright = self.rect.midleft
            self.waves.add(soundwave)
            self.whistlecount += 1
            print "whistles:", self.whistlecount

    def throw(self):
        if self.treatcount < self.level.tlimit and self.level.tlimit > 0:
            treat = Treat(self.bounds, self.level, self.facing)
            treat.rect.left = self.rect.right
            treat.rect.midleft = self.rect.midright
            self.treats.add(treat)
            self.treatcount += 1
            print "treats:", self.treatcount

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
        self.__init__(self.spawnpoint, self.level, self.bounds)

    def reset(self):
        self.level.reset()
        file_out = open("Textdata.txt","w")
        file_out.write("0")
        file_out.close
        self.__init__(self.spawnpoint, self.level, self.bounds)

    def endlevel(self):
        self.playerlvl += 1
        self.rect.center = self.spawnpoint
    
    def update(self, dt):
        dt = dt / 1000.0
        keystate = pygame.key.get_pressed()

        self.vx = 0
        if keystate[K_LEFT]:
            self.vx -= self.playerspeed
            self.facing = "left"
        if keystate[K_RIGHT]:
            self.vx += self.playerspeed
            self.facing = "right"

        self.vy -= dt * self.gravity
        dx = self.vx * dt
        dy = -self.vy * dt

        if self.off_ground == True:
            dx *= 0.5

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
            if self.playerlvl == self.level.levelnum:
                self.endlevel()
                file_in = open("level.txt","r")
                for line in file_in:
                    lvlnum = int(line)
                    lvlnum += 1
                    print lvlnum
                file_in.close()
                  #  except IOError: 
                   #     pass

                file_out = open("level.txt","w")
                num = str(lvlnum)
                file_out.write(lvlnum)
                file_out.close()

        #fall off bottom
        if self.rect.bottom > self.bounds.bottom:
            self.die()

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

                #collect gold puppy
                elif RegPuppy.state == 5:
                    RegPuppy.kill()
                    file_in = open("Textdata.txt","r")
                    for line in file_in:
                        num = int(line)
                        num += 1
                        print num
                    file_in.close()
                  #  except IOError: 
                    file_out = open("Textdata.txt","w")
                    num = str(num)
                    file_out.write(num)
                    file_out.close

            for Bouncer in self.touches(self.level.pups):
                self.die()

            for Fire in self.touches(self.level.pups):
                self.die()
            
            for Gold in self.touches(self.level.pups):
                Gold.collected()
                
class Projectile(Sprite):
    speed = 15
    size = 20, 15

    def __init__(self, bounds, level, facing):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.facing = facing
        self.rect = self.image.get_rect()
        self.bounds = bounds
        self.level = level

    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def update(self):
        if self.facing == "right":
            self.rect.x += self.speed
        elif self.facing == "left":
            self.rect.x -= self.speed

        if self.rect.right > self.bounds.right:  #remove if leaves screen
            self.kill()
        elif self.rect.left < self.bounds.left:
            self.kill()

        for sprite in self.touches(self.level.tiles):
            rect = sprite.rect

            #collide walls
            if self.rect.left <= rect.right:
                self.kill()
            if self.rect.right >= rect.left:
                self.kill()

class Wave(Projectile):
    color = 0, 0, 230

    def __init__(self, bounds, level, facing):
        Projectile.__init__(self, bounds, level, facing)
        self.image.fill(self.color)

    def update(self):
        Projectile.update(self)
        
        for RegPuppy in self.touches(self.level.tiles):
            if RegPuppy.state == 0:
                RegPuppy.state = 1
                self.kill()
            
        for Bouncer in self.touches(self.level.tiles):
            if Bouncer.state == 3:
                Bouncer.state = 2
                self.kill()

        for pup in self.touches(self.level.pups):
            self.kill()

class Treat(Projectile):
    color = 139, 69, 19
    
    def __init__(self, bounds, level, facing):
        Projectile.__init__(self, bounds, level, facing)
        self.image.fill(self.color)

    def update(self):
        Projectile.update(self)
        
        for RegPuppy in self.touches(self.level.pups):
            if RegPuppy.state == 1:
                RegPuppy.state = 0
                self.kill()
        
        for Bouncer in self.touches(self.level.pups):
            if Bouncer.state == 2:
                Bouncer.state = 3
                self.kill()
        
        

