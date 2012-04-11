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
    
    size = 24,32
    color = 0,0,0

    def __init__(self, loc):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.color)

    def next(self):
        pass



class Level_1(object):

    def create_htiles(self):  #creates horizontal tiles
        tile1 = Tile((0, 350), (105, 5), (0,150,0)) #(coordinates) (length, height) (RGB)
        tile2 = Tile((100, 380), (140, 5), (0,150,0))
        tile3 = Tile((335, 380), (100, 5), (0,150,0))
        tile4 = Tile((430, 350), (100, 5), (0,150, 0))
        htiles = Group() #creates a sprite group for tiles
        htiles.add(tile1,tile2, tile3, tile4)
        return htiles
        
    def create_vtiles(self):  #creates vertical tiles
        tile1 = Tile((100, 355), (5, 30), (0,0,150))
        tile2 = Tile((235, 385), (5, 200), (0,0,150))
        tile3 = Tile((335, 385), (5, 200), (0,0,150))
        tile4 = Tile((430, 355), (5, 25), (0,0,150))
        vtiles = Group()
        vtiles.add(tile1, tile2, tile3, tile4)
        return vtiles

    def create_puppies(self):
        pup1 = RegPuppy((130, 381), 1)
        pup2 = RegPuppy((390, 381), 0)
        pups = Group()
        pups.add(pup1, pup2)
        return pups

    def door(self):
        door = Door((470,350))
        door_grp = GroupSingle()
        door_grp.add(door)
        return door_grp

class Level_2(object):
    
    def create_htiles(self):
        tile1 = Tile((0, 400), (206, 6), (0,150,150))
        tile2 = Tile((500, 400), (100, 6), (0,150,150))
        htiles = Group()
        htiles.add(tile1,tile2)
        return htiles
        
    def create_vtiles(self):
        tile3 = Tile((200, 406), (6, 64), (0,0,150))
        vtiles = Group()
        vtiles.add(tile3)
        return vtiles
    
    def create_puppies(self):
        pup1 = RegPuppy((550, 401), 1)
        pups = Group()
        pups.add(pup1)
        return pups

    def door(self):
        door = Door((150,400))
        door_grp = GroupSingle()
        door_grp.add(door)
        return door_grp
    
