#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle

from player import Player
from levels import Tile, L0, L1, L1A, L2, L2A, L3, L4, Last
from puppies import Puppy, RegPuppy

SCREEN_SIZE = 800,360
BG_COLOR = 255, 255, 255

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()

    file_out = open("Textdata.txt", "w") #score
    file_out.write("0")
    file_out.close()
    
    file_out = open("level.txt", "w")  #temporary: rewrites to 0 at start
    file_out.write("0")  #temp
    file_out.close()   #temp
    
    file_in = open("level.txt","r")
    for line in file_in:
        lvlnum = int(line)
    file_in.close()
    
    #initialize game
    lvls = [L0(), L1(), L1A(), L2(), L2A(), L3(), L4(), Last()]

    lvl = lvls[lvlnum]   #starting level

    file_out = open("level.txt","w")
    num = str(lvlnum)
    file_out.write(num)
    file_out.close()

   # lvl = L3()  #temporary: for testing levels
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
            if lvl.state == 1:
                if event.type == KEYDOWN and event.key == K_UP:
                    player.jump()
                elif event.type == KEYDOWN and event.key == K_r:  #reset level
                    player.reset()
                elif event.type == KEYDOWN and event.key == K_z: #whistle
                    player.whistle()
                elif event.type == KEYDOWN and event.key == K_x: #throw
                    player.throw()
            elif lvl.state == 0:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    player.endlevel()
            if lvl.state == 1:  #temporary: for skipping levels
                if event.type == KEYDOWN and event.key == K_SPACE:
                    player.endlevel()

        file_in = open("level.txt","r")
        for line in file_in:
            lvlnum = int(line)
        file_in.close()

      #  lvl = lvls[(player.playerlvl)]
        lvl = lvls[lvlnum]
        player.level = lvl

        #update
        dt = clock.tick(30)
        if lvl.state == 0 or lvl.state == 2:
            lvl.draw(screen)
        
        if lvl.state == 1:
            player.update(dt)
            player.waves.update()
            player.treats.update()
            lvl.pups.update(dt, bounds)
            lvl.tiles.update(dt, bounds)
            lvl.update()

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
