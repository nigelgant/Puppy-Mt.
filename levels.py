import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from puppies import Puppy, RegPuppy, Bouncer, Fire, Gold

def drawtile():
    pass    

class Tile(Sprite):
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

class Between(Level):
    fg_color = 255, 255, 255
    bg_color = 0,0,0

    def __init__(self):
        self.state = 0

    def draw(self, screen):   #draw titles
        bounds = screen.get_rect()
        screen.fill(self.bg_color)

        rect = self.lvltitle.get_rect()
        rect.center = bounds.centerx, bounds.centery - bounds.height /4
        screen.blit(self.lvltitle, rect)
        
        rect = self.cont.get_rect()
        rect.center = bounds.centerx, bounds.centery + bounds.height /4
        screen.blit(self.cont, rect)

class L0(Between):
  #  levelnum = 0
    def __init__(self):
        self.spawn = (50, 200)
        self.state = 0
        font = pygame.font.Font(None, 40)
        self.lvltitle = font.render("WORLD 1 - LEVEL 1", True, self.fg_color, self.bg_color)
        font = pygame.font.Font(None, 20)
        self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color, self.bg_color)


class L1(Level):
  #  levelnum = 1
    wlimit = 5  #whistle limit
    tlimit = 5  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 220), (100, 200), (0,150,0)),
            Tile((100, 280), (160, 100), (200,150,0)),
            Tile((320, 280), (100, 100), (200,150,0)),
            Tile((420, 240), (100, 140), (0,150, 0))
            )
        ##puppies
        pup1 = RegPuppy((130, 280), 1, self.tiles)
        pup2 = RegPuppy((330, 280), 0, self.tiles)
        pup3 = Bouncer((370, 230), 2, 400, self.tiles)
        pup4 = Gold((100, 180))
        pup5 = Gold((140, 250))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(Door((470,260)))

class L1A(Between):

    def __init__(self):
        self.state = 0
        self.spawn = (50, 200)
        font = pygame.font.Font(None, 40)
        self.lvltitle = font.render("WORLD 1 - LEVEL 2", True, self.fg_color, self.bg_color)
        font = pygame.font.Font(None, 20)
        self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color, self.bg_color)

class L2(Level):
    wlimit = 3
    tlimit = 3

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

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

class L2A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 50)
        font = pygame.font.Font(None, 40)
        self.lvltitle = font.render("WORLD 1 - LEVEL 3", True, self.fg_color, self.bg_color)
        font = pygame.font.Font(None, 20)
        self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color, self.bg_color)

class L3(Level):
    wlimit = 2
    tlimit = 3

    def __init__(self):
        global counter
        self.state = 1
        self.spawn = (50, 50) #spawnpoint
        print "level 3"


        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (120, 240), (150,0,0)),
            Tile((120, 240), (120, 120), (0,150,0)),
            Tile((240, 80), (120, 280), (0,150,150)),
            Tile((360, 160), (170, 200), (0,150, 0)),
            Tile((600, 160), (40, 200), (0,150,150)),
            Tile((640, 120), (200, 240), (0,150, 0))
            )

        ##puppies
        self.pups = Group(
            Bouncer((160, 240), 2, 430, self.tiles),
           # RegPuppy((130, 160), 1, self.tiles),
            RegPuppy((400, 160), 1, self.tiles)
            )

        self.door = GroupSingle(Door((760,120)))

class L4(Level):
    wlimit = 5  #whistle limit
    tlimit = 5  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 220), (100, 200), (100,150,0)),
            Tile((100, 280), (160, 100), (100,150,0)),
            Tile((320, 280), (100, 100), (100,150,0)),
            Tile((420, 240), (100, 140), (230,150, 0))
            )

        ##puppies
        pup1 = RegPuppy((130, 280), 1, self.tiles)
        pup2 = RegPuppy((330, 280), 0, self.tiles)
        pup3 = Bouncer((370, 230), 2, 400, self.tiles)
        pup4 = Gold((100, 180))
        pup5 = Gold((140, 250))
      #  pup4 = Fire((800, 230), (-1, 0), 90, self.tiles)
      #  pup5 = Fire((330, 0), (0, 1), 90, self.tiles)
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(Door((470,260)))

class Last(Between):

    def __init__(self):
        self.state = 2
        self.spawn = (30, 20)
        font = pygame.font.Font(None, 40)
        self.lvltitle = font.render("YOU WON", True, self.fg_color, self.bg_color)
        font = pygame.font.Font(None, 20)
        self.cont = font.render("(the demo)", True, self.fg_color, self.bg_color)
