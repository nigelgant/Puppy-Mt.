#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide, spritecollideany, collide_rect

from player import Player
from levels import Tile, Level_1, Level_2
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
    lvl1 = Level_1()
    lvl2 = Level_2()
    lvl = lvl1
    player = Player(lvl.spawn, lvl)
    player_grp = GroupSingle(player) #spritegroup for player

  #  pups = Group(lvl.create_puppies())
#    pups = Group()
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
                

        #update
        dt = clock.tick(30)
                
      #  player_grp.update()
        player.update(dt)
      #  door = GroupSingle(lvl.door())

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
