import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from puppies import Puppy, RegPuppy


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
        

class Level_1(Level):

    def __init__(self):
        self.spawn = (50, 300) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 350), (100, 150), (0,150,0)),
            Tile((100, 380), (140, 100), (0,150,0)),
            Tile((335, 380), (100, 100), (0,150,0)),
            Tile((430, 350), (100, 150), (0,150, 0))
            )

        ##puppies
        self.pups = Group(   
            RegPuppy((130, 381), 1, self.tiles),
            RegPuppy((400, 381), 0, self.tiles)
            )

        self.door = GroupSingle(Door((470,350)))
        
class Level_2(Level):
    pass
