#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide, spritecollideany, collide_rect

from player import Player
from levels import Tile, L1, L2
from puppies import Puppy, RegPuppy

SCREEN_SIZE = 640,480
BG_COLOR = 255, 255, 255

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect

    #initialize game
    spawn = (50, 300) #spawnpoint
    lvl1 = L1()
    lvl2 = L2()
    lvls = [lvl1, lvl2]

    lvl = lvl1
    lvls = [lvl1, lvl2]
    player = Player(lvl.spawn, lvl)
    player_grp = GroupSingle(player) #spritegroup for player

    #game loop
    done = False
    clock = pygame.time.Clock()
    
    while not done:

        # input
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
            elif event.type == KEYDOWN and event.key == K_UP:
                player.jump()
            elif event.type == KEYDOWN and event.key == K_r:  #reset level
                player.reset()

        lvl = lvls[(player.playerlvl)]
        player.level = lvl
        #update
        dt = clock.tick(30)
                
      #  player_grp.update()
        player.update(dt)
      #  door = GroupSingle(lvl.door())
        lvl.update()
       # pups.add(lvl.create_puppies())
       # print pups
        lvl.pups.update()

        #collisions
        """
 
            if not spritecollideany(RegPuppy, htiles):
                RegPuppy.edge()
        """
        #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
      #  player.draw(screen)
        lvl.tiles.draw(screen)

        lvl.pups.draw(screen)
        lvl.door.draw(screen)
        pygame.display.flip()
     #   clock.tick(30)

if __name__ == "__main__":
    main()
