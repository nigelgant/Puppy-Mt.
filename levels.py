import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide



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
    
    def __init__(self):
        pass

    def create_htiles(self):  #creates horizontal tiles
        tile1 = Tile((0, 400), (206, 6), (0,150,0)) #coordinates, size, color
        tile2 = Tile((325, 400), (200, 6), (0,150,0))
        htiles = Group() #creates a sprite group for tiles
        htiles.add(tile1,tile2)
        return htiles
        
    def create_vtiles(self):  #creates vertical tiles
        tile3 = Tile((200, 406), (6, 64), (0,0,150))
        tile4 = Tile((325, 406), (6, 64), (0,0,150))
        tile5 = Tile((450, 300), (6, 100), (0,0,150))
        vtiles = Group()
        vtiles.add(tile3, tile4, tile5)
        return vtiles
