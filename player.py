#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, groupcollide, spritecollideany
from levels import Tile
from resources import load_image, load_sfx
from spritesheet import SpriteSheet
from anim import Animation
from random import randint


class PlayerAnimation(Animation):
    _rows = {(1, 0): 0,
             (-1, 0): 2,
             (0, -1): 0,
             (0, 1) : 0,
             (1, 1): 0,
             (-1, -1): 2,
             (-1, 1): 2,
             (1, -1): 0,
             (1, 7): 1,   #7 = die
             (-1, 7): 3
             } #add the dying rows later?
        
    def __init__(self, player, image, duration):
        self.player = player
        self.duration = duration
        self.y = self._rows[(1, 0)] #need to fix?

        spritesheet = SpriteSheet(image, (3, 4))
        self.frames = [ (self.duration, 0),
                   (self.duration, 1),
                   (self.duration, 2),
                   (self.duration, 1) ]
        
        Animation.__init__(self, spritesheet, self.frames)

    def update(self, dt):
        vx, vy = self.player.vx, self.player.vy

        #calculate the direction facing
        try:
            vx /= abs(vx)
        except:
            vx = 0
        try:
            vy /= abs(vy)
        except:
            vy = 0

        #figure out spritesheet row
        if vx == 0 and vy == 0:
            self.time = 0
            self.x = 1

        elif self.player.off_ground == True and self.player.facing == "right":
            self.x = 2
            self.y = 0
        elif self.player.off_ground == True and self.player.facing == "left":
            self.x = 0
            self.y = 2

        else:
            self.time += dt
            self.x = self.get_frame_data(self.time)
            self.y = self._rows[(vx, vy)]
        if self.player.dying == True:
            if self.player.facing == "right":
                self.y = 1
            if self.player.facing == "left":
                self.y = 3
            if self.player.dyingcounter <= 0.5:
                self.x = 0
            if self.player.dyingcounter > 1:
                self.x = 1
            if self.player.dyingcounter >= 1.5:
                self.x = 2

class Player(Sprite):
    size = 18, 34
    playerspeed = 200
    gravity = 600

    def __init__(self, loc, level, bounds):
        Sprite.__init__(self)
        self.vx = 0
        self.vy = 0

        self.collect = False

        self.facing = "right"  #facing right

        self.level = level
        self.spawnpoint = loc
        self.bounds = bounds
        self.dying = False

        self.anim = PlayerAnimation(self, "chetanim.png", 120)
        self.image = self.anim.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = loc
        
        rect = self.image.get_rect().inflate(-4,-4) #what does this do?        

        self.off_ground = True
        self.waves = Group() #soundwaves
        self.treats = Group() #dog treats
        self.whistlecount = 0
        self.treatcount = 0
        self.dyingcounter = 0
        self.diefalling = False
        self.scorenum = 0
        self.has_played = False
        self.has_fallen = False
        self.has_splat = False

        self.falls = ["fall1","fall2","fall3","fall4","fall5","fall6"]
        self.fallsound = str(self.falls[(randint(0, 5))])
        self.fallingsound = load_sfx(self.fallsound)

        self.splats = ["splat1","splat2","splat3","splat4"]
        self.splatsound = str(self.splats[(randint(0, 3))])
        self.hitsound = load_sfx(self.splatsound)

    def jump(self, mute):
        if not self.off_ground:
            self.off_ground = True
            self.vy = 280 #jump speed
            self.jumpsound = load_sfx("jump")
            if mute == False:
                self.jumpsound.play()

    def whistle(self, mute):
        if self.whistlecount < self.level.wlimit and self.level.wlimit > 0:
            soundwave = Wave(self.bounds, self.level, self.facing)
            self.whistlesound = load_sfx("whistle")
            if mute == False:
                self.whistlesound.play()
            if self.facing == "right":
                soundwave.rect.left = self.rect.right
                soundwave.rect.midleft = self.rect.midright
            elif self.facing == "left":
                soundwave.rect.right = self.rect.left
                soundwave.rect.midright = self.rect.midleft
            self.waves.add(soundwave)
            self.whistlecount += 1

    def throw(self, mute):
        if self.treatcount < self.level.tlimit and self.level.tlimit > 0:
            treat = Treat(self.bounds, self.level, self.facing)
            self.throwsound = load_sfx("throw")
            if mute == False:
                self.throwsound.play()
            if self.facing == "right":
                treat.rect.left = self.rect.right
                treat.rect.midleft = self.rect.midright
            elif self.facing == "left":
                treat.rect.right = self.rect.left
                treat.rect.midright = self.rect.midleft
            self.treats.add(treat)
            self.treatcount += 1

    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) #grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching
    
    def die(self, dt):
        self.level.reset()
        self.__init__(self.level.spawn, self.level, self.bounds)

    def reset(self):
        self.level.reset()
        self.__init__(self.level.spawn, self.level, self.bounds)

    def endlevel(self):
        file_in = open("level.txt","r")
        for line in file_in:
            lvlnum = int(line)
            lvlnum += 1
        file_in.close()

        file_in = open("score.txt","r")
        for line in file_in:
            self.levelnew = int(line)
        file_in.close()

        file_out = open("score.txt","w")
        file_out.write(str(int(self.scorenum) + self.levelnew))
        file_out.close()
        
        file_out = open("level.txt","w")
        num = str(lvlnum)
        file_out.write(num)
        file_out.close()
        self.__init__(self.level.spawn, self.level, self.bounds)
        
       
    def update(self, dt, mute):
        self.mute = mute
        #animation
        self.anim.update(dt)
        self.image = self.anim.get_current_frame()

        keystate = pygame.key.get_pressed()
        self.vx = 0
        if self.dying == False:
            if keystate[K_LEFT]:
                self.vx -= self.playerspeed
                self.facing = "left"
            if keystate[K_RIGHT]:
                self.vx += self.playerspeed
                self.facing = "right"

        dt = dt / 1000.0
        self.vy -= dt * self.gravity
        dx = self.vx * dt
        dy = -self.vy * dt

        self.collect = False

        if self.off_ground == True:  #slow jumping
            dx *= 0.7
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
                if sprite.state == 0 or sprite.state == 3:
                    if not self.has_played:
                        self.bark = load_sfx("bark")
                        if self.mute == False:
                            self.bark.play()
                        self.has_played = True
                
                self.vy = 0
                self.rect.bottom = rect.top
                self.off_ground = False
            
        if self.has_played and self.off_ground:
            self.has_played = False

        if self.dying == True:  #death pause
            if self.diefalling == True:
                self.dyingcounter += dt*3
                if not self.has_fallen:
                    self.fallingsound.play()
                    self.has_fallen = True
                    self.diefalling = False
            else:
                self.dyingcounter += dt*10
            if self.dyingcounter > 2:
                self.dying = False
        if self.dyingcounter > 2:
            self.die(dt)

        #collide doors
        for sprite in self.touches(self.level.door):
            self.endsound = load_sfx("endlevel")
            if self.mute == False:
                self.endsound.play()
            self.endlevel()

        #fall off bottom
        if self.rect.bottom > self.bounds.bottom:
            self.diefalling = True
            self.dying = True

        if self.rect.left < self.bounds.left: #left side of screen
            self.vx = 0
            self.rect.left = self.bounds.left

        elif self.rect.right > self.bounds.right:
            self.vx = 0
            self.rect.right = self.bounds.right

        for sprite in self.touches(self.level.pups):
            rect = sprite.rect
            for RegPuppy in self.touches(self.level.pups):
                #killed by puppy
                if RegPuppy.state == 1 or RegPuppy.state == 2 or RegPuppy.state == 4:
                    if not self.has_splat:
                        if self.mute == False:
                            self.hitsound.play()
                            self.fallingsound.play()
                        self.has_splat = True
                    self.vx = 0
                    self.vy = 0
                    self.dying = True
      
                #collect gold puppy
                elif RegPuppy.state == 5:
                    self.goldsound = load_sfx("collect")
                    if self.mute == False:
                        self.goldsound.play()
                    RegPuppy.kill()
                    self.scorenum += 1
                    self.level.score = self.scorenum
        
            for Gold in self.touches(self.level.pups):
                if Gold.state == 5:
                    Gold.collected()
          
class Projectile(Sprite):
    speed = 17
    size = 20, 15

    def __init__(self, bounds, level, facing):
        Sprite.__init__(self)
        self.image = self.proj
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
    def __init__(self, bounds, level, facing):
        if facing == "right":
            self.proj = load_image("soundwaveright.png")
        elif facing == "left":
            self.proj = load_image("soundwaveleft.png")
        self.proj.set_colorkey((255,255,255))
        Projectile.__init__(self, bounds, level, facing)

    def update(self):
        Projectile.update(self)
        
        for RegPuppy in self.touches(self.level.tiles):
            if RegPuppy.state == 0:
                RegPuppy.state = 1
                self.kill()
            
        for Bouncer in self.touches(self.level.tiles):
            if Bouncer.state == 3:  #if bouncer is frozen
                Bouncer.state = 2   #bouncer is unfrozen
                self.kill()

        for pup in self.touches(self.level.pups):
            if pup.state != 5:
                self.kill()
  
    def draw(self, screen):
        rect = self.proj.get_rect()
        rect.center = self.rect.center
        screen.blit(self.proj, rect)

class Treat(Projectile):
    
    def __init__(self, bounds, level, facing):
        if facing == "right":
            self.proj = load_image("treatright.png")
        if facing == "left":
            self.proj = load_image("treatleft.png")
        self.proj.set_colorkey((255,255,255))
        Projectile.__init__(self, bounds, level, facing)
       # self.image.fill(self.color)

    def update(self):
        Projectile.update(self)
        
        for RegPuppy in self.touches(self.level.pups):
            if RegPuppy.state == 1:
                RegPuppy.state = 0
                self.kill()
        
        for Bouncer in self.touches(self.level.pups):
            if Bouncer.state == 2:   #if bouncer is active
                Bouncer.state = 3    #bouncer is frozen
                self.kill()

    def draw(self, screen):
        rect = self.proj.get_rect()
        rect.center = self.rect.center
        screen.blit(self.proj, rect)
        
        

