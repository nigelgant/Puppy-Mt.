!#/usr/bin/env python

class L1(Level):
  #  levelnum = 1
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 200), (240, 160), (0,150,0)),
            Tile((240, 280), (200, 80), (200,150,0)),
            Tile((520, 280), (120, 80), (200,150,0)),
            Tile((620, 240), (160, 120), (0,150, 0)),
            Tile((320, 140), (80, 20), (0,150, 0))
            )
        ##puppies
        pup1 = RegPuppy((245, 280), 1, self.tiles)
        pup2 = RegPuppy((520, 280), 1, self.tiles)
        pup3 = RegPuppy((325, 140), 1, self.tiles)
        pup4 = Gold((360, 140))
        self.pups = Group(pup1, pup2, pup3, pup4)

        self.door = GroupSingle(Door((720,240)))


class L2(Level):
  #  levelnum = 1
    wlimit = 0  #whistle limit
    tlimit = 0  #treat limit

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
            Tile((120, 100), (80, 20), (0,150, 0))


            )
        ##puppies
        pup1 = RegPuppy((285, 160), 1, self.tiles)
        pup2 = RegPuppy((445, 240), 1, self.tiles)
        pup3 = RegPuppy((685, 280), 1, self.tiles)
        pup4 = RegPuppy((170, 100), 1, self.tiles)
        pup5 = Gold((120, 100))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(Door((720,280)))

class L3(Level):
  #  levelnum = 1
    wlimit = 2  #whistle limit
    tlimit = 1  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

        ##tiles - (coordinates) (length, height) (RGB)
        self.tiles = Group(     
            Tile((0, 200), (400, 160), (0,150,0)),
            Tile((160, 160), (120, 40), (200,150,0)),
            Tile((240, 120), (160, 40), (200,150,0)),
            Tile((480, 200), (80, 200), (0,150, 0)),
            Tile((560, 160), (80, 200), (200,150,0)),
            Tile((640, 120), (80, 240), (0,150, 0)),
            Tile((720, 80), (80, 280), (0,150, 0))


            )
        ##puppies
        pup1 = RegPuppy((165, 160), 1, self.tiles)
        pup2 = RegPuppy((245, 120), 1, self.tiles)
        pup3 = RegPuppy((565, 160), 1, self.tiles)
        pup4 = RegPuppy((645, 120), 1, self.tiles)
        pup5 = Gold((285, 200))
        self.pups = Group(pup1, pup2, pup3, pup4, pup5)

        self.door = GroupSingle(Door((730,80)))


class L4(Level):
  #  levelnum = 1
    wlimit = 2  #whistle limit
    tlimit = 2  #treat limit

    def __init__(self):
        self.state = 1
        self.spawn = (50, 200) #spawnpoint

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
        pup1 = RegPuppy((205, 320), 1, self.tiles)
        pup2 = RegPuppy((405, 240), 1, self.tiles)
        pup3 = RegPuppy((605, 280), 1, self.tiles)
        pup4 = Gold((45, 320))
        self.pups = Group(pup1, pup2, pup3, pup4)

        self.door = GroupSingle(Door((730,200)))


class L5(Level):
  #  levelnum = 1
    wlimit = 3  #whistle limit
    tlimit = 3  #treat limit

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


