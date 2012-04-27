import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from puppies import Puppy, RegPuppy, Bouncer, Fire, Gold
from resources import load_image, play_song

jungle = 0, 150, 0
cliff = 200, 150, 0
lab = 80, 80, 80

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
    fg_color = 0, 0, 0
    global jungle, cliff, lab

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

    def draw(self, screen, player):
        bounds = screen.get_rect()
        pygame.font.init()
        pixfont = "./data/fonts/pixelated.ttf"
        self.player = player

        font = pygame.font.Font(pixfont, 15)
        if self.wlimit > 0: 
            self.whistles = font.render(("WHISTLES:"+" "+str(self.wlimit - self.player.whistlecount)), True, self.fg_color)
            rect = self.whistles.get_rect()
            rect.center = bounds.centerx + 340, bounds.centery - 140
            screen.blit(self.whistles, rect)

        if self.tlimit > 0:
            self.treats = font.render(("TREATS:"+" "+str(self.tlimit - self.player.treatcount)), True, self.fg_color)
            rect = self.treats.get_rect()
            rect.center = bounds.centerx + 350, bounds.centery - 160
            screen.blit(self.treats, rect)

class Between(Level):
    fg_color = 255, 255, 255
    bg_color = 0,0,0

    def __init__(self):
        self.state = 0

    def draw(self, screen):
        bounds = screen.get_rect()
        file_in = open("score.txt","r")
        for line in file_in:
            self.score = str(line)

        pygame.font.init()
        pixfont = "./data/fonts/pixelated.ttf"

        rect = self.bg.get_rect()
        rect.center = bounds.centerx, bounds.centery
        screen.blit(self.bg, rect)

        if self.state == 0:
            font = pygame.font.Font(pixfont, 30)
            self.lvltitle = font.render(("CURRENT SCORE:"+" "+self.score), True, self.fg_color)


            rect = self.lvltitle.get_rect()
            rect.center = bounds.centerx, bounds.centery - bounds.height /6
            screen.blit(self.lvltitle, rect)
        
        font = pygame.font.Font(pixfont, 15)
        self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color)
        rect = self.cont.get_rect()
        rect.center = bounds.centerx, bounds.centery + bounds.height /2.5
        screen.blit(self.cont, rect)

class Menu(Between):   #finish later
    def __init__(self):
        pass 

class L0(Between):
    def __init__(self):
        self.spawn = (50, 160)
        self.state = 0
        self.bg = load_image("jungle1.bmp")

class L1(Level):
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 100) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 200), (240, 160), jungle),
            Tile((240, 280), (200, 80), jungle),
            Tile((520, 280), (120, 80), jungle),
            Tile((640, 240), (160, 120), jungle),
            Tile((320, 160), (140, 20), jungle)
            )
        ##puppies
        pup1 = RegPuppy((245, 280), 1, self.tiles)
        pup2 = RegPuppy((520, 280), 1, self.tiles)
        pup3 = RegPuppy((325, 160), 1, self.tiles)
        pup4 = Gold((360, 160))
        self.pups = Group(pup1, pup2, pup3, pup4)

        self.door = GroupSingle(Door((720,240)))

class FoundTreat(Between):
    def __init__(self):
        self.spawn = (50, 230)
        self.state = 3
        self.bg = load_image("foundtreat.bmp")


class L1A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 230)
        self.bg = load_image("jungle2.bmp")

class L2(Level):
    wlimit = 0
    tlimit = 2

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 280), (200, 80), (0,150,0)),
            Tile((200, 240), (40, 120), (200,150,0)),
            Tile((240, 200), (40, 160), (200,150,0)),
            Tile((280, 160), (160, 200), (0,150, 0)),
            Tile((440, 240), (160, 120), (200,150,0)),
            Tile((680, 280), (120, 80), (0,150, 0)),
            Tile((120, 100), (120, 20), (0,150, 0))
            )
        ##puppies
        pup1 = RegPuppy((285, 160), 1, self.tiles)
        pup2 = RegPuppy((445, 240), 1, self.tiles)
        pup3 = RegPuppy((685, 280), 1, self.tiles)
        pup4 = RegPuppy((170, 100), 1, self.tiles)
        pup5 = Gold((160, 100))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(Door((720,280)))

class L2A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 160)
        self.bg = load_image("jungle3.bmp")

class L3(Level):
    wlimit = 0
    tlimit = 1
    def __init__(self):
        self.state = 1
        self.spawn = (50, 160)
        self.tiles = Group(     
            Tile((0, 200), (400, 160), (0,150,0)),
            Tile((120, 160), (120, 40), (200,150,0)),
            Tile((200, 120), (160, 40), (200,150,0)),
            Tile((480, 200), (80, 200), (0,150, 0)),
            Tile((560, 160), (80, 200), (200,150,0)),
            Tile((620, 120), (120, 240), (0,150, 0)),
            Tile((720, 80), (80, 280), (0, 150, 0))
            )
        ##puppies
        pup1 = RegPuppy((165, 160), 1, self.tiles)
        pup2 = RegPuppy((275, 120), 1, self.tiles)
        pup4 = RegPuppy((655, 120), 1, self.tiles)
        pup5 = Gold((285, 200))
        pup6 = RegPuppy((295, 200), 1, self.tiles)
        self.pups = Group(pup1, pup2, pup4, pup5, pup6)

        self.door = GroupSingle(Door((730,80)))

class L3A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 70)
        self.bg = load_image("jungle4.bmp")

class L4(Level):
    wlimit = 0  #whistle limit
    tlimit = 2  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 70) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (40, 240), (0,150,0)),
            Tile((40, 120), (160, 120), (200,150,0)),
            Tile((40, 320), (240, 40), (200,150,0)),
            Tile((120, 280), (80, 40), (0,150, 0)),
            Tile((280, 280), (40, 80), (200,150,0)),
            Tile((320, 240), (40, 120), (0,150, 0)),
            Tile((360, 200), (40, 160), (0,150, 0)),
            Tile((400, 240), (120, 120), (200,150,0)),
            Tile((600, 280), (120, 80), (0,150, 0)),
            Tile((720, 200), (80, 160), (0,150, 0))
            )
        ##puppies
        self.pups = Group(
            RegPuppy((205, 320), 1, self.tiles),
            RegPuppy((405, 240), 1, self.tiles),
            RegPuppy((605, 280), 1, self.tiles),
            Gold((45, 320)))
        self.door = GroupSingle(Door((730,200)))

class L5(Level):
    wlimit = 0
    tlimit = 3
    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint
        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 240), (40, 240), (0,150,0)),
            Tile((120, 200), (160, 120), (200,150,0)),
            Tile((200, 120), (240, 40), (200,150,0)),
            Tile((320, 160), (80, 40), (0,150, 0)),
            Tile((480, 160), (40, 80), (200,150,0)),
            Tile((560, 200), (40, 120), (0,150, 0)),
            Tile((600, 240), (40, 160), (0,150, 0)),
            Tile((760, 120), (120, 120), (200,150,0)),
            Tile((560, 100), (120, 80), (0,150, 0))
            )
        ##puppies
        pup1 = RegPuppy((125, 200), 1, self.tiles)
        pup2 = RegPuppy((325, 160), 1, self.tiles)
        pup3 = RegPuppy((485, 160), 1, self.tiles)
        pup4 = RegPuppy((565, 100), 1, self.tiles)
        pup5 = RegPuppy((605, 240), 1, self.tiles)
        pup6 = RegPuppy((685, 240), 1, self.tiles)
        pup7 = Gold((725, 120))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(Door((730,200)))

class FoundWhistle(Between):
    def __init__(self):
        self.spawn = (50, 230)
        self.state = 3
        self.bg = load_image("foundwhistle.png")

class Last(Between):
    def __init__(self):
        self.state = 2
