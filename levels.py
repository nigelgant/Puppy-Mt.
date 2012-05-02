import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from puppies import Puppy, RegPuppy, Bouncer, Fire, Gold
from resources import load_image, play_song

blinkcounter = 0

class TiledImage(object):
    def __init__(self, image, rect=None):
        self.image = image
        if rect is None:
            self.rect = image.get_rect()
        else:
            self.rect = rect
    
    def draw(self, surf, rect=None):
        # if no rect is given, use surfaces rect
        if rect is None:
            rect = surf.get_rect()

        w, h = self.rect.size
        x, y = self.rect.topleft

        # calculate the start and end points
        x0 = rect.x - (-x % w)
        x1 = rect.x + rect.width

        y0 = rect.y - (-y % h)
        y1 = rect.y + rect.height

        # loop through and draw images
        for y in xrange(y0, y1, h):
            for x in xrange(x0, x1, w):
                surf.blit(self.image, (x, y))

class Tile(Sprite):
    def __init__(self, loc, size, img):
        self.size = size
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        tiled_img = TiledImage(img)
        tiled_img.draw(self.image)

        self.rect.topleft = loc
        self.state = "tile"

class Door(Sprite):
    def __init__(self, loc):
        Sprite.__init__(self)
        self.rect.bottomleft = loc        

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
        screen.blit(self.door, rect)

class LabDoor(Door):
    def __init__(self, loc):
        Sprite.__init__(self)
        self.door = load_image("labdoor.png")
        self.door.set_colorkey((255,255,255))
        self.image = self.door
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc

    def draw(self, screen):
        rect = self.door.get_rect()
        screen.blit(self.door, rect)

class Level(object):
    fg_color = 0, 0, 0
    jungle = load_image("tilegrass.png")
    cliff = load_image("tilecliff.png")
    lab = load_image("tilemetal.png")

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

    def draw_hud(self, screen, player):
        bounds = screen.get_rect()
        pixfont = "./data/fonts/pixelated.ttf"
        self.player = player

        file_in = open("score.txt","r")
        for line in file_in:
            self.score = str(line)
        self.currentscore = self.score

        self.display_score = int(self.currentscore) + int(self.player.scorenum)            
        font = pygame.font.Font(pixfont, 15)
       
        self.scoredisplay = font.render(("SCORE:"+" "+str(self.display_score)), True, self.fg_color)
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

    def draw(self, screen, player):
        bounds = screen.get_rect()
        if self.type == "jungle":
            self.bg = load_image("junglebg1.png")
        elif self.type == "cliff":
            self.bg = load_image("cliffbg.png")
        elif self.type == "lab":
            self.bg = load_image("labbg.png")
        rect = self.bg.get_rect()
        rect.center = bounds.centerx, bounds.centery
        screen.blit(self.bg, rect)

class Between(Level):
    fg_color = 255, 255, 255
    bg_color = 0,0,0

    def __init__(self):
        self.state = 0

    def blinker(self, dt):
        global blinkcounter
        blinkcounter += dt/10
        if blinkcounter > 100:
            blinkcounter = 0
        return blinkcounter

    def draw(self, screen, dt):
        self.dt = dt
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

        if self.state == "last":
            font = pygame.font.Font(pixfont, 30)
            self.lvltitle = font.render(("FINAL SCORE:"+" "+self.score), True, self.fg_color)

            rect = self.lvltitle.get_rect()
            rect.center = bounds.centerx + 160, bounds.centery + bounds.height /16
            screen.blit(self.lvltitle, rect)

            if int(self.score) == 15:
                font = pygame.font.Font(pixfont, 20)
                self.award = font.render(("GOLDEN  RETRIEVER  AWARD"), True, (255, 215, 0))
                rect = self.award.get_rect()
                rect.center = bounds.centerx + 160, bounds.centery + bounds.height /8
                screen.blit(self.award, rect)

        if self.state != "menu" and self.state != "last":
          #  print self.blinker(dt)
            if self.blinker(dt) > 50:
                font = pygame.font.Font(pixfont, 15)
                self.cont = font.render("PRESS SPACE TO CONTINUE", True, self.fg_color)
                rect = self.cont.get_rect()
                rect.center = bounds.centerx, bounds.centery + bounds.height /2.5
                screen.blit(self.cont, rect)
            else:
                pass

class Menu(Between):   #finish later
    song = "menu"

    def __init__(self):
        play_song(self.song)

        self.state = "menu"
        self.bg = load_image("menu.png")
        self.spawn = (0, 160)
        self.newlvlnum = 0
        self.inst = False
        self.done = False
        self.mute = False

    def draw(self, screen):
        bounds = screen.get_rect()
        rect = self.bg.get_rect()
        rect.center = bounds.centerx, bounds.centery
        screen.blit(self.bg, rect)

    def draw_titles(self, screen, dt):
        bounds = screen.get_rect()
        pygame.font.init()
        pixfont = "./data/fonts/pixelated.ttf"
        font = pygame.font.Font(pixfont, 40)
        if self.inst == False:
            self.newgame = font.render(("NEW GAME"), True, self.fg_color)
            self.newgamerect = self.newgame.get_rect()
            self.newgamerect.center = bounds.centerx - 210, bounds.centery - 30
            screen.blit(self.newgame, self.newgamerect)

            self.contgame = font.render(("CONTINUE GAME"), True, self.fg_color)
            self.contgamerect = self.contgame.get_rect()
            self.contgamerect.center = bounds.centerx - 210, bounds.centery + 30
            screen.blit(self.contgame, self.contgamerect)

            self.instructions = font.render(("INSTRUCTIONS"), True, self.fg_color)
            self.instrect = self.instructions.get_rect()
            self.instrect.center = bounds.centerx - 210, bounds.centery + 90
            screen.blit(self.instructions, self.instrect)

            font = pygame.font.Font(pixfont, 20)
            self.quit = font.render(("EXIT GAME"), True, self.fg_color)
            self.quitrect = self.quit.get_rect()
            self.quitrect.center = bounds.centerx - 210, bounds.centery + 145
            screen.blit(self.quit, self.quitrect)

        if self.inst == True:
            self.bg = load_image("instructions.png")
            if self.blinker(dt/2) > 50:
                font = pygame.font.Font(pixfont, 18)
                self.cont = font.render("PRESS X TO RETURN TO MENU", True, self.fg_color)
                rect = self.cont.get_rect()
                rect.center = bounds.centerx + 270, bounds.centery - 150
                screen.blit(self.cont, rect)
        elif self.inst == False:
            self.bg = load_image("menu.png")

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == QUIT:
                self.done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.done = True
            if event.type == KEYDOWN and event.key == K_m: #mute
                if self.mute == False:
                    self.mute = True
                    pygame.mixer.music.pause()
                elif self.mute == True:
                    self.mute = False
                    pygame.mixer.music.unpause()
                    
            if event.type == MOUSEBUTTONDOWN:
                if self.newgamerect.collidepoint(event.pos):
                    file_out = open("score.txt", "w") #reset score
                    file_out.write("0") 
                    file_out.close()

                    file_out = open("level.txt", "w")
                    file_out.write("1") 
                    file_out.close()
                    self.newlvlnum = 1
                    
                if self.contgamerect.collidepoint(event.pos):
                    file_in = open("level.txt","r")
                    for line in file_in:
                        self.newlvlnum = int(line)
                    file_in.close()

                if self.instrect.collidepoint(event.pos):
                    self.inst = True

                if self.quitrect.collidepoint(event.pos):
                    self.done = True

            if event.type == KEYDOWN and event.key == K_x:
                self.inst = False
    
class Prologue1(Between):
    song = None
    def __init__(self):
        self.spawn = (50, 160)
        self.state = 3
        self.bg = load_image("prologue1.png")
class Prologue2(Between):
    song = None
    def __init__(self):
        self.spawn = (50, 160)
        self.state = 3
        self.cutscene = True
        self.bg = load_image("prologue2.png")

class L1A(Between):
    song = "jungle1"

    def __init__(self):
        self.spawn = (50, 160)
        self.state = 0
        self.bg = load_image("jungle1.png")

class L1(Level):
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 100) #spawnpoint
        self.type = "jungle"
        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 200), (240, 160), self.jungle),
            Tile((240, 280), (200, 80), self.jungle),
            Tile((520, 280), (120, 80), self.jungle),
            Tile((640, 240), (160, 120), self.jungle),
            Tile((320, 160), (140, 20), self.jungle)
            )
        ##puppies
        pup1 = RegPuppy((245, 280), 1, self.tiles)
        pup2 = RegPuppy((520, 280), 1, self.tiles)
        pup3 = RegPuppy((325, 160), 1, self.tiles)
        pup4 = Gold((360, 160))
        self.pups = Group(pup1, pup2, pup3, pup4) #remove pup5 later

        self.door = GroupSingle(TreeDoor((720,240)))

class FoundTreat(Between):
    song = None

    def __init__(self):
        self.spawn = (50, 230)
        self.state = 3
        self.bg = load_image("foundtreat.bmp")


class L2A(Between):
    song = None

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
            Tile((0, 280), (200, 80), self.jungle),
            Tile((200, 240), (40, 120), self.jungle),
            Tile((240, 200), (40, 160), self.jungle),
            Tile((280, 160), (160, 200), self.jungle),
            Tile((440, 240), (160, 120), self.jungle),
            Tile((680, 280), (120, 80), self.jungle),
            Tile((120, 100), (120, 20), self.jungle)
            )
        ##puppies
        pup1 = RegPuppy((285, 160), 1, self.tiles)
        pup2 = RegPuppy((445, 240), 1, self.tiles)
        pup3 = RegPuppy((685, 280), 1, self.tiles)
        pup4 = RegPuppy((170, 100), 1, self.tiles)
        pup5 = Gold((160, 100))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(TreeDoor((720,280)))

class L3A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (50, 160)
        self.bg = load_image("jungle3.bmp")

class L3(Level):
    wlimit = 0
    tlimit = 2
    def __init__(self):
        self.state = 1
        self.spawn = (50, 160)
        self.type = "jungle"

        self.tiles = Group(     
            Tile((0, 200), (400, 160), self.jungle),
            Tile((120, 160), (120, 40), self.jungle),
            Tile((200, 120), (160, 40), self.jungle),
            Tile((480, 200), (80, 200), self.jungle),
            Tile((560, 160), (80, 200), self.jungle),
            Tile((620, 120), (120, 240), self.jungle),
            Tile((720, 80), (80, 280), self.jungle)
            )
        ##puppies
        pup2 = RegPuppy((275, 120), 1, self.tiles)
        pup4 = RegPuppy((655, 120), 1, self.tiles)
        pup5 = Gold((285, 200))
        pup6 = RegPuppy((295, 200), 1, self.tiles)
        self.pups = Group(pup2, pup4, pup5, pup6)

        self.door = GroupSingle(TreeDoor((730,80)))

class L4A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (50, 70)
        self.bg = load_image("jungle4.bmp")

class L4(Level):
    wlimit = 0
    tlimit = 3
    def __init__(self):
        self.state = 1
        self.spawn = (50, 70) #spawnpoint
        self.type = "jungle"
        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (40, 240), self.jungle),
            Tile((40, 120), (160, 120), self.jungle),
            Tile((40, 320), (240, 40), self.jungle),
            Tile((120, 280), (80, 40), self.jungle),
            Tile((280, 280), (40, 80), self.jungle),
            Tile((320, 240), (40, 120), self.jungle),
            Tile((360, 200), (40, 160), self.jungle),
            Tile((400, 240), (120, 120), self.jungle),
            Tile((600, 280), (120, 80), self.jungle),
            Tile((720, 220), (80, 160), self.jungle)
            )
        ##puppies
        self.pups = Group(
            RegPuppy((205, 320), 1, self.tiles),
            RegPuppy((405, 240), 1, self.tiles),
            RegPuppy((605, 280), 1, self.tiles),
            Gold((45, 320)))
        self.door = GroupSingle(TreeDoor((730,220)))

class L5A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (50, 200)
        self.bg = load_image("jungle5.png")

class L5(Level):
    wlimit = 0
    tlimit = 4
    def __init__(self):
        self.state = 1
        self.spawn = (50, 200)
        self.type = "jungle"
        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 240), (120, 120), self.jungle),
            Tile((120, 200), (80, 160), self.jungle),
            Tile((200, 140), (40, 240), self.jungle),
            Tile((280, 160), (120, 200), self.jungle),
            Tile((480, 160), (80, 200), self.jungle),
            Tile((560, 200), (40, 160), self.jungle),
            Tile((600, 240), (160, 120), self.jungle),
            Tile((760, 120), (40, 240), self.jungle),
            Tile((560, 100), (240, 20), self.jungle),
            Tile((720, 160), (240, 20), self.jungle),   
            )
        ##puppies
        pup1 = RegPuppy((125, 200), 1, self.tiles)
        pup2 = RegPuppy((325, 160), 1, self.tiles)
        pup3 = RegPuppy((485, 160), 1, self.tiles)
        pup4 = RegPuppy((565, 100), 1, self.tiles)
        pup5 = RegPuppy((605, 240), 1, self.tiles)
        pup6 = RegPuppy((685, 240), 1, self.tiles)
        pup7 = Gold((725, 160))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(CliffDoor((730,100)))

class FoundWhistle(Between):
    song = None
    def __init__(self):
        self.spawn = (50, 50)
        self.state = 3
        self.bg = load_image("foundwhistle.png")

class L6A(Between):
    song = "cliffs"
    def __init__(self):
        self.state = 0
        self.spawn = (50, 100)
        self.bg = load_image("cliffs1.bmp")

class L6(Level):
    wlimit = 2  #whistle limit
    tlimit = 3  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 100) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (120, 240), (self.cliff)),
            Tile((120, 240), (120, 120), (self.cliff)),
            Tile((240, 80), (120, 280), (self.cliff)),
            Tile((360, 160), (120, 200), (self.cliff)),
            Tile((600, 160), (40, 200), (self.cliff)),
            Tile((640, 120), (200, 240), (self.cliff)),
            Tile((440, 60), (120, 20), (self.cliff))
            )
        ##puppies
        pup1 = Bouncer((165, 240), 2, 430, self.tiles)
        pup2 = RegPuppy((365, 160), 1, self.tiles)
        pup3 = RegPuppy((640, 120), 0, self.tiles)
        pup4 = RegPuppy((500, 60), 1, self.tiles)
        pup5 = Gold((445, 60))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(CliffDoor((740,120)))

class L7A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (40, 100)
        self.bg = load_image("cliffs2.png")


class L7(Level):
    wlimit = 2  #whistle limit
    tlimit = 4  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (40, 100) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (self.cliff)),
            Tile((80, 280), (40, 80), (self.cliff)),
            Tile((200, 280), (80, 80), (self.cliff)),
            Tile((280, 220), (200, 160), (self.cliff)),
            Tile((480, 320), (200, 40), (self.cliff)),
            Tile((680, 210), (120, 160), (self.cliff))
            )
        ##puppies
        pup1 = RegPuppy((205, 280), 1, self.tiles)
        pup3 = RegPuppy((365, 220), 0, self.tiles)
        pup4 = RegPuppy((400, 220), 1, self.tiles)
        pup5 = Bouncer((525, 320), 2, 400, self.tiles)
        pup6 = Bouncer((595, 320), 2, 400, self.tiles)
        pup7 = Gold((560, 320))
        self.pups = Group(pup1, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(CliffDoor((740,210)))

class L8A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 220)
        self.bg = load_image("cliffs3.png")

class L8(Level):
    wlimit = 2  #whistle limit
    tlimit = 4  #treat limit
    song = None

    def __init__(self):
        self.state = 1
        self.spawn = (20, 220) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 240), (160, 120), self.cliff),
            Tile((160, 140), (120, 260), self.cliff),
            Tile((360, 200), (80, 160), self.cliff),
            Tile((480, 160), (80, 200), self.cliff),
            Tile((600, 200), (40, 160), self.cliff),
            Tile((680, 120), (120, 240), self.cliff),
            Tile((400, 60), (160, 20), self.cliff),
            Tile((440, 280), (40, 80), self.cliff)
            )
        ##puppies
        pup1 = Bouncer((80, 240), 2, 300, self.tiles)
        pup2 = Bouncer((120, 240), 2, 400, self.tiles)
        pup4 = Bouncer((445, 280), 2, 400, self.tiles)
        pup5 = Bouncer((605, 200), 2, 350, self.tiles)
        pup6 = RegPuppy((530, 60), 1, self.tiles)
        pup7 = Gold((460, 60))
        self.pups = Group(pup1, pup2, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(CliffDoor((750, 120)))

class L9A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 100)
        self.bg = load_image("cliffs4.png")

class L9(Level):
    wlimit = 2  #whistle limit
    tlimit = 3  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 100) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (self.cliff)),
            Tile((80, 160), (85, 200), (self.cliff)),
            Tile((280, 80), (160, 40), (self.cliff)),
            Tile((240, 120), (200, 40), (self.cliff)),
            Tile((160, 160), (280, 40), (self.cliff)),
            Tile((160, 240), (320, 120), (self.cliff)),
            Tile((480, 280), (80, 80), (self.cliff)),
            Tile((600, 200), (40, 160), (self.cliff)),
            Tile((680, 200), (40, 160), (self.cliff)),
            Tile((760, 200), (40, 160), (self.cliff))
            )
        ##puppies
        pup1 = RegPuppy((85, 160), 1, self.tiles)
        pup3 = RegPuppy((360, 80), 0, self.tiles)
        pup4 = RegPuppy((400, 80), 1, self.tiles)
        pup5 = Bouncer((525, 280), 2, 300, self.tiles)
        pup6 = Fire((800, 240), (-1, 0), 60, self.tiles)
        pup7 = Fire((800, 80), (-1, 0), 100, self.tiles)
        pup8 = Gold((170, 240))
        self.pups = Group(pup1, pup3, pup4, pup5, pup6, pup7, pup8)

        self.door = GroupSingle(CliffDoor((765,200)))

class L10A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 50)
        self.bg = load_image("cliffs5.png")


class L10(Level):
    wlimit = 3  #whistle limit
    tlimit = 3  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 50) #spawnpoint
        self.type = "cliff"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (80, 240), (self.cliff)),
            Tile((120, 80), (40, 280), (self.cliff)),
            Tile((160, 160), (40, 200), (self.cliff)),
            Tile((200, 80), (40, 280), (self.cliff)),
            Tile((320, 80), (40, 280), (self.cliff)),
            Tile((360, 120), (160, 40), (self.cliff)),
            Tile((360, 160), (200, 40), (self.cliff)),
            Tile((400, 320), (400, 40), (self.lab)),
            Tile((480, 240), (120, 40), (self.lab)),
            Tile((600, 120), (40, 160), (self.lab)),
            Tile((640, 120), (160, 40), (self.lab)),
            Tile((720, 280), (80, 40), (self.lab)),
            Tile((640, 80), (40, 40), (self.lab))
            )
        ##puppies
        pup1 = Bouncer((170, 160), 2, 400, self.tiles)
        pup2 = RegPuppy((365, 120), 1, self.tiles)
        pup3 = Bouncer((565, 240), 2, 430, self.tiles)
        pup4 = RegPuppy((490, 320), 0, self.tiles)
        pup5 = Fire((800, 40), (-1, 0), 90, self.tiles)
        pup6 = Fire((800, 80), (-1, 0), 100, self.tiles)
        pup7 = Fire((720, 0), (-1, 1), 120, self.tiles)
        pup8 = Gold((720, 120))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8)

        self.door = GroupSingle(LabDoor((750,280)))
class L11A(Between):
    song = "lab"
    def __init__(self):
        self.state = 0
        self.spawn = (20, 100)
        self.bg = load_image("lab1.png")

class L11(Level):
    wlimit = 3  #whistle limit
    tlimit = 4  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 100) #spawnpoint
        self.type = "lab"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 120), (120, 120), self.lab),
            Tile((0, 240), (400, 120), self.lab),
            Tile((0, 0), (240, 40), self.lab),
            Tile((120, 160), (40, 80), self.lab),
            Tile((160, 200), (40, 40), self.lab),
            Tile((240, 0), (80, 200), self.lab),
            Tile((320, 0), (480, 80), self.lab),
            Tile((320, 140), (40, 20), self.lab),
            Tile((400, 280), (280, 80), self.lab),
            Tile((440, 240), (40, 40), self.lab),
            Tile((480, 160), (40, 40), self.lab),
            Tile((480, 200), (160, 80), self.lab),
            Tile((720, 280), (80, 80), self.lab)
            )
        ##puppies
        pup1 = RegPuppy((285, 240), 0, self.tiles)
        pup2 = Bouncer((410, 280), 2, 350, self.tiles)
        pup3 = Bouncer((450, 280), 2, 300, self.tiles)
        pup4 = RegPuppy((525, 200), 1, self.tiles)
        pup5 = Fire((800, 160), (-1, 0), 90, self.tiles)
        pup6 = Fire((800, 80), (-1, 0), 60, self.tiles)
        pup7 = Gold((325, 140))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7)

        self.door = GroupSingle(LabDoor((750,280)))

class L12A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 130)
        self.bg = load_image("lab2.png")

class L12(Level):
    wlimit = 3  #whistle limit
    tlimit = 5  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 130) #spawnpoint
        self.type = "lab"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 0), (80, 80), (self.lab)),
            Tile((0, 80), (400, 40), (self.lab)),
            Tile((0, 200), (80, 80), (self.lab)),
            Tile((0, 280), (645, 80), (self.lab)),
            Tile((80, 0), (280, 40), (self.lab)),
            Tile((320, 220), (80, 80), (self.lab)),
            Tile((360, 120), (120, 40), (self.lab)),
            Tile((440, 160), (80, 40), (self.lab)),
            Tile((560, 120), (160, 40), (self.lab)),
            Tile((640, 160), (40, 200), (self.lab)),
            Tile((680, 320), (120, 40), (self.lab)),
            Tile((720, 200), (40, 40), (self.lab)),
            Tile((395, 260), (250, 20), (self.lab)),
            Tile((760, 120), (80, 80), (self.lab))
            )
        ##puppies
        pup1 = RegPuppy((85, 280), 1, self.tiles)
        pup2 = RegPuppy((295, 280), 1, self.tiles)
        pup3 = RegPuppy((450, 260), 1, self.tiles)
        pup4 = RegPuppy((565, 120), 1, self.tiles)
        pup5 = RegPuppy((320, 80), 0, self.tiles)
        pup6 = Bouncer((525, 280), 2, 350, self.tiles)
        pup7 = Bouncer((445, 120), 2, 400, self.tiles)
        pup8 = Fire((0, 80), (1, 0), 60, self.tiles)
        pup9 = Gold((240, 80))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8, pup9)

        self.door = GroupSingle(LabDoor((750,320)))

class L13A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 120)
        self.bg = load_image("lab3.png")

class L13(Level):
    wlimit = 2  #whistle limit
    tlimit = 4  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 120) #spawnpoint
        self.type = "lab"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 140), (80, 160), (self.lab)),
            Tile((0, 240), (120, 120), (self.lab)),
            Tile((120, 0), (40, 120), (self.lab)),
            Tile((160, 0), (120, 40), (self.lab)),
            Tile((160, 80), (160, 40), (self.lab)),
            Tile((160, 320), (40, 40), (self.lab)),
            Tile((240, 320), (40, 40), (self.lab)),
            Tile((320, 180), (160, 180), (self.lab)),
            Tile((400, 80), (240, 40), (self.lab)),
            Tile((440, 120), (40, 80), (self.lab)),
            Tile((480, 340), (320, 20), (self.lab)),
            Tile((520, 240), (280, 40), (self.lab)),
            Tile((640, 80), (40, 120), (self.lab)),
            Tile((680, 160), (40, 40), (self.lab)),
            Tile((720, 80), (40, 120), (self.lab))

            )
        ##puppies
        pup1 = RegPuppy((255, 80), 0, self.tiles)
        pup2 = Bouncer((165, 320), 2, 350, self.tiles)
        pup3 = Bouncer((245, 320), 2, 400, self.tiles)
        pup4 = Bouncer((325, 175), 2, 350, self.tiles)
        pup5 = RegPuppy((405, 80), 1, self.tiles)
        pup6 = Bouncer((530, 240), 2, 300, self.tiles)
        pup7 = Bouncer((605, 235), 2, 300, self.tiles)
        pup8 = Bouncer((685, 160), 2, 400, self.tiles)
        pup9 = Fire((0, 80), (1, 0), 90, self.tiles)
        pup10 = Gold((230, 80))
        pup11 = RegPuppy((485, 340), 1, self.tiles)


        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8, pup9, pup10, pup11)

        self.door = GroupSingle(LabDoor((750,340)))
class L14A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 200)
        self.bg = load_image("lab4.png")

class L14(Level):
    wlimit = 3  #whistle limit
    tlimit = 5  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 200) #spawnpoint
        self.type = "lab"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 0), (240, 40), (self.lab)),
            Tile((0, 40), (40, 40), (self.lab)),
            Tile((0, 80), (280, 40), (self.lab)),
            Tile((0, 240), (80, 40), (self.lab)),
            Tile((0, 260), (600, 100), (self.lab)),
            Tile((240, 120), (120, 40), (self.lab)),
            Tile((240, 200), (360, 80), (self.lab)),
            Tile((480, 140), (40, 60), (self.lab)),
            Tile((520, 100), (80, 100), (self.lab)),
            Tile((595, 100), (85, 20), (self.lab)),
            Tile((600, 320), (200, 40), (self.lab)),
            Tile((640, 160), (42, 120), (self.lab)),
            Tile((680, 160), (40, 40), (self.lab)),
            Tile((720, 0), (80, 200), (self.lab))

            )
        ##puppies
        pup1 = RegPuppy((45, 80), 1, self.tiles)
        pup2 = RegPuppy((245, 80), 0, self.tiles)
        pup3 = RegPuppy((85, 260), 1, self.tiles)
        pup4 = RegPuppy((285, 200), 0, self.tiles)
        pup5 = Bouncer((365, 200), 2, 350, self.tiles)
        pup6 = RegPuppy((645, 100), 1, self.tiles)
        pup7 = RegPuppy((645, 320), 0, self.tiles)
        pup8 = Fire((280, 360), (-1, -1), 60, self.tiles)
        pup9 = Gold((210, 80))

        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8, pup9)

        self.door = GroupSingle(LabDoor((750,320)))

class L15A(Between):
    song = None
    def __init__(self):
        self.state = 0
        self.spawn = (20, 100)
        self.bg = load_image("lab5.png")

class L15(Level):
    wlimit = 3  #whistle limit
    tlimit = 5  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (20, 100) #spawnpoint
        self.type = "lab"

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 0), (360, 40), (self.lab)),
            Tile((0, 120), (160, 40), (self.lab)),
            Tile((0, 280), (40, 40), (self.lab)),
            Tile((0, 320), (480, 40), (self.lab)),
            Tile((80, 200), (240, 40), (self.lab)),
            Tile((40, 220), (240, 20), (self.lab)),
            Tile((200, 240), (40, 80), (self.lab)),
            Tile((240, 100), (120, 100), (self.lab)),
            Tile((360, 120), (80, 80), (self.lab)),
            Tile((360, 280), (40, 40), (self.lab)),
            Tile((440, 80), (40, 120), (self.lab)),
            Tile((440, 280), (40, 40), (self.lab)),
            Tile((520, 160), (80, 40), (self.lab)),
            Tile((520, 280), (40, 80), (self.lab)),
            Tile((600, 80), (200, 120), (self.lab)),
            Tile((600, 200), (40, 80), (self.lab)),
            Tile((560, 320), (240, 40), (self.lab)),
            Tile((200, 160), (40, 40), (self.lab)),
            Tile((0, 260), (10, 20), (self.lab))
            )
        ##puppies
        pup1 = RegPuppy((45, 320), 1, self.tiles)
        pup2 = Bouncer((165, 190), 2, 400, self.tiles)
        pup3 = Bouncer((365, 115), 2, 350, self.tiles)
        pup4 = RegPuppy((330, 320), 1, self.tiles)
        pup5 = Bouncer((405, 320), 2, 350, self.tiles)
        pup6 = RegPuppy((605, 80), 1, self.tiles)
        pup7 = RegPuppy((615, 320), 0, self.tiles)
        pup8 = Fire((-80, 320), (1, 0), 55, self.tiles)
        pup9 = Fire((240, -80), (1, 1), 60, self.tiles)
        pup10 = Fire((600, -80), (0, 2), 65, self.tiles)
        pup11 = Fire((880, 60), (-1, 1), 50, self.tiles)
        pup12 = Gold((140, 320))

        self.pups = Group(pup1, pup2, pup3, pup4, pup5, pup6, pup7, pup8, pup9, pup10, pup11, pup12)

        self.door = GroupSingle(LabDoor((750,320)))

class Almost(Between):
    song = "ending"
    def __init__(self):
        self.state = 3
        self.spawn = (20, 200)
        self.bg = load_image("almost.png")

class Last(Between):
    song = None

    def __init__(self):
        self.state = "last"
        self.spawn = (20, 200)
        self.bg = load_image("ending.png")
