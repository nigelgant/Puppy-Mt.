#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide, spritecollideany, collide_rect

from player import Player
from levels import Tile, L1, L2
from puppies import Puppy, RegPuppy

SCREEN_SIZE = 800,360
BG_COLOR = 255, 255, 255

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()

    #initialize game
    lvl1 = L1()
    lvl2 = L2()
    lvls = [lvl1, lvl2]

    lvl = lvl1   #starting level
    player = Player(lvl.spawn, lvl, bounds)
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
            elif event.type == KEYDOWN and event.key == K_z: #whistle
                player.whistle()
            elif event.type == KEYDOWN and event.key == K_x: #throw
                player.throw()

        lvl = lvls[(player.playerlvl)]
        player.level = lvl
        #update
        dt = clock.tick(30)

        player.update(dt)
        player.waves.update()
        player.treats.update()
        lvl.update()
        lvl.pups.update(dt, bounds)
        lvl.tiles.update(dt, bounds)
        #collisions
        """
 
            if not spritecollideany(RegPuppy, htiles):
                RegPuppy.edge()
        """
        #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        player.waves.draw(screen)
        player.treats.draw(screen)
        lvl.tiles.draw(screen)

        lvl.pups.draw(screen)
        lvl.door.draw(screen)
        pygame.display.flip()
     #   clock.tick(30)

if __name__ == "__main__":
    main()
