import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from puppies import Puppy, RegPuppy, Bouncer, Fire

def drawtile():
    pass    

class Tile(Sprite):
  #  size = 64, 6
  #  color = 0, 150, 0
    def __init__(self, loc, size, color):
        self.size = size
        self.color = color
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = loc
        self.image.fill(self.color)
        self.state = "tile"

class Door(Sprite):
    
    size = 18,30
    color = 0,0,0

    def __init__(self, loc):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.color)

    def next(self):
        pass

class Level(object):

    def __init__(self):
        self.pups = Group()
        self.tiles = Group()

    def reset(self):
        self.__init__()

    def update(self):
        for pup in self.pups:
            if pup.state == 0 or pup.state == 3:
               self.pups.remove(pup)
               self.tiles.add(pup)

        for pup in self.tiles:
            if pup.state == 1 or pup.state == 2:
                self.tiles.remove(pup)
                self.pups.add(pup)

class L1(Level):
    levelnum = 0
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

    def __init__(self):
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 220), (100, 200), (0,150,0)),
            Tile((100, 280), (140, 100), (200,150,0)),
            Tile((320, 280), (100, 100), (200,150,0)),
            Tile((420, 240), (100, 140), (0,150, 0))
            )

        ##puppies
        pup1 = RegPuppy((130, 280), 1, self.tiles)
        pup2 = RegPuppy((330, 280), 0, self.tiles)
        pup3 = Bouncer((370, 230), 2, self.tiles)
      #  pup4 = Fire((800, 230), (-1, 0), 90, self.tiles)
      #  pup5 = Fire((330, 0), (0, 1), 90, self.tiles)
        self.pups = Group(pup1, pup2, pup3)
        """
        self.pups = Group(   
            RegPuppy((130, 380), 1, self.tiles),
            RegPuppy((400, 381), 0, self.tiles)
            )
        """
        self.door = GroupSingle(Door((470,260)))
        

class L2(Level):
    levelnum = 1
    wlimit = 3
    tlimit = 3

    def __init__(self):
        self.spawn = (50, 255) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 280), (200, 80), (150,0,0)),
            Tile((200, 240), (40, 120), (0,150,0)),
            Tile((240, 200), (40, 160), (0,150,150)),
            Tile((280, 160), (160, 200), (0,150, 0)),
            Tile((440, 240), (160, 120), (0,150,150)),
            Tile((680, 280), (120, 80), (0,150, 0))
            )


        ##puppies
        self.pups = Group(   
            RegPuppy((285, 160), 1, self.tiles),
            RegPuppy((445, 240), 1, self.tiles)
            )

        self.door = GroupSingle(Door((760,280)))

class L3(Level):
    levelnum = 2
    wlimit = 2
    tlimit = 3

    def __init__(self):
        self.spawn = (50, 115) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (120, 240), (150,0,0)),
            Tile((120, 240), (120, 120), (0,150,0)),
            Tile((240, 80), (120, 280), (0,150,150)),
            Tile((360, 160), (120, 200), (0,150, 0)),
            Tile((600, 160), (40, 200), (0,150,150)),
            Tile((640, 120), (200, 240), (0,150, 0))
            )

        ##puppies
        self.pups = Group(
            Bouncer((160, 235), 2, self.tiles),
            RegPuppy((130, 381), 1, self.tiles),
            RegPuppy((400, 381), 0, self.tiles)
            )

        self.door = GroupSingle(Door((760,120)))
