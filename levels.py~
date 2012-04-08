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

class Level_1(object):

    def create_htiles(self):  #creates horizontal tiles
        tile1 = Tile((0, 400), (206, 6), (0,150,0)) #(coordinates) (length, height) (RGB)
        tile2 = Tile((325, 400), (200, 6), (0,150,0))
        htiles = Group() #creates a sprite group for tiles
        htiles.add(tile1,tile2)
        return htiles
        
    def create_vtiles(self):  #creates vertical tiles
        tile3 = Tile((200, 406), (6, 64), (0,0,150))
        tile4 = Tile((325, 406), (6, 64), (0,0,150))
        tile5 = Tile((480, 300), (6, 100), (0,0,150))
        tile6 = Tile((380, 300), (6, 20), (0,0,150))
        tile7 = Tile((70, 300), (6, 100), (0,0,150))
        vtiles = Group()
        vtiles.add(tile3, tile4, tile5, tile6, tile7)
        return vtiles

    def create_puppies(self):
        pup1 = RegPuppy((100, 401), 0)
        pup2 = RegPuppy((400, 401), 1)
        pups = Group()
        pups.add(pup1, pup2)
        return pups

class Level_2(object):
    
    def create_htiles(self):
        tile1 = Tile((0, 400), (206, 6), (0,150,150))
        tile2 = Tile((500, 400), (100, 6), (0,150,150))
        htiles = Group()
        htiles.add(tile1,tile2)
        return htiles
        
