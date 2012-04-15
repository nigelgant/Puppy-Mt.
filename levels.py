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
        self.state = "TEST"

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
        pass

    def reset(self):
        self.__init__()

  #  def update(self):
        

class L1(Level):
    levelnum = 0
    whistlelimit = 3
    treatlimit = 2

    def __init__(self):
        self.spawn = (50, 300) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 350), (100, 150), (0,150,0)),
            Tile((100, 380), (140, 100), (200,150,0)),
            Tile((330, 380), (100, 100), (200,150,0)),
            Tile((430, 350), (100, 150), (0,150, 0))
            )

        ##puppies
        pup1 = RegPuppy((130, 380), 1, self.tiles)
        pup2 = RegPuppy((400, 380), 0, self.tiles)
        pup3 = Bouncer((370, 330), 2, self.tiles)
        pup4 = Fire((80, 50), (0, 1), 90)
        self.pups = Group(pup1, pup2, pup3, pup4)
        """
        self.pups = Group(   
            RegPuppy((130, 380), 1, self.tiles),
            RegPuppy((400, 381), 0, self.tiles)
            )
        """
 
        self.door = GroupSingle(Door((470,350)))

    def update(self):
        for pup in self.pups:
            if pup.state == 0 or pup.state == 3:
               self.pups.remove(pup)
               self.tiles.add(pup)

        for pup in self.tiles:
            if pup.state == 1 or pup.state == 2:
                self.tiles.remove(pup)
                self.pups.add(pup)
        
        
class L2(Level):
    levelnum = 1

    def __init__(self):
        self.spawn = (50, 300) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 350), (100, 150), (150,0,0)),
            Tile((100, 380), (140, 100), (0,150,0)),
            Tile((335, 380), (100, 100), (0,150,150)),
            Tile((430, 350), (100, 150), (0,150, 0))
            )

        ##puppies
        self.pups = Group(   
           # RegPuppy((130, 381), 1, self.tiles),
            RegPuppy((400, 381), 0, self.tiles)
            )

        self.door = GroupSingle(Door((470,350)))
        
    def update(self):
        for pup in self.pups:
            if pup.state == 0:
               self.pups.remove(pup)
               self.tiles.add(pup)

        for pup in self.tiles:
            if pup.state == 1:
                self.tiles.remove(pup)
                self.pups.add(pup)
        
