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
  #  size = 30,50
    color = 0,0,0

    def __init__(self, loc):
        Sprite.__init__(self)
      #  self.image = self.door
       # self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
      #  self.image.fill(self.color)
        

class TreeDoor(Door):
    def __init__(self, loc):
        Sprite.__init__(self)
        self.door = load_image("tree.png")
        self.door.set_colorkey((255,255,255))
        self.image = self.door
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc

    def draw(self, screen):
        rect = self.door.get_rect()
      #  rect.center = self.rect.center
        screen.blit(self.door, rect)

class CliffDoor(Door):
    def __init__(self, loc):
        Sprite.__init__(self)
        self.door = load_image("cave.png")
        self.door.set_colorkey((255,255,255))
        self.image = self.door
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc

    def draw(self, screen):
        rect = self.door.get_rect()
      #  rect.center = self.rect.center
        screen.blit(self.door, rect)


class Level(object):
    fg_color = 0, 0, 0
    global jungle, cliff, lab  #for tile colors

    def __init__(self):
        self.pups = Group()
        self.tiles = Group()

        file_in = open("score.txt","r")
        for line in file_in:
            self.score = str(line)

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
        file_in = open("score.txt","r")
        for line in file_in:
            self.score = str(line)

        if self.type == "jungle":
            self.bg = load_image("junglebg1.png")
        elif self.type == "cliff":
            self.bg = load_image("cliffbg.png")
        rect = self.bg.get_rect()
        rect.center = bounds.centerx, bounds.centery
        screen.blit(self.bg, rect)

        font = pygame.font.Font(pixfont, 15)

        self.scoredisplay = font.render(("SCORE:"+" "+str(self.score)), True, self.fg_color)
        rect = self.scoredisplay.get_rect()
        rect.center = bounds.centerx - 360, bounds.centery - 160
        screen.blit(self.scoredisplay, rect)

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
        if self.state != "menu":
            font = pygame.font.Font(pixfont, 15)
            self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color)
            rect = self.cont.get_rect()
            rect.center = bounds.centerx, bounds.centery + bounds.height /2.5
            screen.blit(self.cont, rect)

class Menu(Between):   #finish later
    def __init__(self):
        self.state = "menu"
        self.bg = load_image("menu.png")
        
    def update(self):
        keystate = pygame.key.get_pressed()
            

class L0(Between):
    song = "jungle1"

    def __init__(self):
      #  play_song(self.song)

        self.spawn = (50, 160)
        self.state = 0
        self.bg = load_image("jungle1.bmp")

class L1(Level):
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 100) #spawnpoint
        self.type = "jungle"
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
        self.pups = Group(pup1, pup2, pup3, pup4) #remove pup5 later

        self.door = GroupSingle(TreeDoor((720,240)))

class FoundTreat(Between):
    song = "cypress"

    def __init__(self):
        self.spawn = (50, 230)
        self.state = 3
        self.bg = load_image("foundtreat.bmp")


class L1A(Between):
    song = "cypress"

    def __init__(self):
       # play_song(self.song)
        self.state = 0
        self.spawn = (50, 230)
        self.bg = load_image("jungle2.bmp")

class L2(Level):
    wlimit = 0
    tlimit = 2

    def __init__(self):
        self.state = 1
        self.spawn = (50, 230) #spawnpoint
        self.type = "jungle"

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

        self.door = GroupSingle(TreeDoor((720,280)))

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
        self.type = "jungle"
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

        self.door = GroupSingle(TreeDoor((730,80)))

class L3A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 70)
        self.bg = load_image("jungle4.bmp")

class L4(Level):
    wlimit = 0
    tlimit = 2
    def __init__(self):
        self.state = 1
        self.spawn = (50, 70) #spawnpoint
        self.type = "jungle"
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
        self.door = GroupSingle(TreeDoor((730,200)))

class L4A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 200)
        self.bg = load_image("jungle5.png")

class L5(Level):
    wlimit = 0
    tlimit = 3
    def __init__(self):
        self.state = 1
        self.spawn = (50, 200)
        self.type = "jungle"
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

        self.door = GroupSingle(CliffDoor((730,200)))

class FoundWhistle(Between):
    def __init__(self):
        self.spawn = (50, 50)
        self.state = 3
        self.bg = load_image("foundwhistle.png")

class L5A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (50, 50)
        self.bg = load_image("cliffs1.bmp")

class L6(Level):
    wlimit = 2  #whistle limit
    tlimit = 2  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 50) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (120, 240), (cliff)),
            Tile((120, 240), (120, 120), (cliff)),
            Tile((240, 80), (120, 280), (cliff)),
            Tile((360, 160), (120, 200), (cliff)),
            Tile((600, 160), (40, 200), (cliff)),
            Tile((640, 120), (200, 240), (cliff)),
            Tile((440, 60), (120, 20), (cliff))
            )
        ##puppies
        pup1 = Bouncer((165, 240), 2, 430, self.tiles)
        pup2 = RegPuppy((365, 160), 1, self.tiles)
        pup3 = RegPuppy((640, 120), 0, self.tiles)
        pup4 = RegPuppy((500, 60), 1, self.tiles)
        pup5 = Gold((445, 60))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(CliffDoor((740,120)))

class L6A(Between):
    def __init__(self):
        self.state = 0
        self.spawn = (40, 140)
        self.bg = load_image("cliffs2.png")


class L7(Level):
    wlimit = 2  #whistle limit
    tlimit = 3  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (40, 140) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (cliff)),
            Tile((80, 280), (40, 80), (cliff)),
            Tile((200, 280), (80, 80), (cliff)),
            Tile((280, 200), (200, 160), (cliff)),
            Tile((480, 320), (200, 40), (cliff)),
            Tile((680, 200), (120, 160), (cliff))
            )
        ##puppies
        pup1 = RegPuppy((205, 280), 1, self.tiles)
        pup2 = RegPuppy((285, 200), 1, self.tiles)
        pup3 = RegPuppy((365, 200), 0, self.tiles)
        pup4 = RegPuppy((400, 200), 1, self.tiles)
        pup5 = Bouncer((525, 320), 2, 440, self.tiles)
        pup6 = Bouncer((595, 320), 2, 460, self.tiles)
        pup7 = Gold((560, 320))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(CliffDoor((740,200)))

class L8(Level):
    wlimit = 2  #whistle limit
    tlimit = 3  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 220) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 240), (160, 120), (0,150,0)),
            Tile((160, 100), (120, 260), (0,150,0)),
            Tile((360, 200), (80, 160), (200,150,0)),
            Tile((480, 160), (80, 200), (200,150,0)),
            Tile((600, 200), (40, 160), (0,150, 0)),
            Tile((680, 120), (80, 240), (0,150, 0)),
            Tile((400, 60), (160, 20), (200,150,0)),
            Tile((440, 280), (40, 80), (0,150, 0))
            )
        ##puppies
        pup1 = Bouncer((80, 240), 2, 200, self.tiles)
        pup2 = Bouncer((120, 240), 2, 200, self.tiles)
        pup3 = RegPuppy((165, 100), 1, self.tiles)
        pup4 = Bouncer((445, 280), 2, 200, self.tiles)
        pup5 = Bouncer((605, 200), 2, 200, self.tiles)
        pup6 = RegPuppy((540, 60), 1, self.tiles)
        pup7 = Gold((560, 320))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(CliffDoor((750, 120)))

class L9(Level):
    wlimit = 2  #whistle limit
    tlimit = 2  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 130) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (cliff)),
            Tile((80, 160), (80, 200), (cliff)),
            Tile((280, 80), (200, 40), (cliff)),
            Tile((240, 120), (240, 40), (cliff)),
            Tile((160, 160), (320, 40), (cliff)),
            Tile((160, 240), (320, 120), (cliff)),
            Tile((480, 280), (80, 80), (cliff)),
            Tile((600, 200), (40, 160), (cliff)),
            Tile((680, 200), (40, 160), (cliff)),
            Tile((720, 200), (40, 160), (cliff))
            )
        ##puppies
        pup1 = RegPuppy((85, 160), 1, self.tiles)
        pup2 = RegPuppy((285, 80), 1, self.tiles)
        pup3 = RegPuppy((360, 80), 0, self.tiles)
        pup4 = RegPuppy((420, 80), 1, self.tiles)
        pup5 = Bouncer((525, 280), 2, 200, self.tiles)
        pup6 = Fire((800, 240), (-1, 0), 60, self.tiles)
        pup7 = Fire((800, 80), (-1, 0), 100, self.tiles)
        pup8 = Gold((170, 240))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8)

        self.door = GroupSingle(CliffDoor((750,120)))


class L10(Level):
    wlimit = 2  #whistle limit
    tlimit = 2  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 50) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (cliff)),
            Tile((120, 80), (80, 200), (cliff)),
            Tile((160, 160), (200, 40), (cliff)),
            Tile((200, 80), (240, 40), (cliff)),
            Tile((320, 80), (320, 40), (cliff)),
            Tile((360, 120), (320, 120), (cliff)),
            Tile((360, 160), (80, 80), (cliff)),
            Tile((400, 320), (40, 160), (lab)),
            Tile((480, 240), (40, 160), (lab)),
            Tile((600, 120), (40, 160), (lab)),
            Tile((640, 120), (40, 160), (lab)),
            Tile((720, 280), (40, 160), (lab)),
            Tile((640, 80), (40, 40), (lab))
            )
        ##puppies
        pup1 = Bouncer((170, 160), 2, 200, self.tiles)
        pup2 = RegPuppy((365, 120), 1, self.tiles)
        pup3 = Bouncer((565, 240), 2, 200, self.tiles)
        pup4 = RegPuppy((490, 320), 0, self.tiles)
        pup5 = Fire((800, 40), (-1, 0), 90, self.tiles)
        pup6 = Fire((800, 80), (-1, 0), 60, self.tiles)
        pup7 = Fire((720, 0), (-1, 1), 120, self.tiles)
        pup8 = Gold((720, 120))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8)

        self.door = GroupSingle(CliffDoor((750,280)))

class Last(Between):
    def __init__(self):
        self.state = 2
