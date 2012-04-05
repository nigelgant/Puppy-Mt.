
def drawtile():
    #finish later

class Tile(Sprite):
    size = 64, 10
    color = 100, 100, 100

    def __init__(self, loc, bounds, tiletype):
        Sprite.__init__(self)

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

        if tiletype == jungle:
            color = 0, 150, 0
        elif tiletype == cliff:
            color = 222, 184, 135
        elif tiletype == lab:
            color = 190, 190, 0

        self.image.fill(self.color)

    
