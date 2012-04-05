#!/usr/bin/env python

class Player(Sprite):
    size = 48, 32
    color = 0, 0, 255
    vx, vy = 0, 0

    def __init__(self, loc, bounds):
        Sprite.__init__(self)

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

        self.rect.center = loc #where player respawns?
        self.bounds = bounds

        self.image.fill(self.color)
        
    def moveright(self):
        self.vx += 5
        
    def moveleft(self):
        self.vx -=5

    def update(self):
        self.rect.x += self.vx

    
    

