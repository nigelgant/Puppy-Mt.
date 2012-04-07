#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide, spritecollideany

from player import Player
from levels import Tile, Level_1
from puppies import Puppy, RegPuppy

SCREEN_SIZE = 640,480
BG_COLOR = 255, 255, 255

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect

    #initialize game
    player = Player((200,200), bounds)
    player_grp = GroupSingle(player) #spritegroup for player
    lvl1 = Level_1()
    pups = Group(lvl1.create_puppies())

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
                player.kill()
                player = Player((200,200), bounds)
                player_grp.add(player)


        #update
        player_grp.update()
        htiles = lvl1.create_htiles()
        vtiles = lvl1.create_vtiles()
        pups.update()

        #collisions
        if groupcollide(player_grp, htiles, False, False):
            player.land()
        if groupcollide(player_grp, vtiles, False, False):
            player.hitwall()
        elif not groupcollide(player_grp, htiles, False, False, None):
            player.fall()
        for RegPuppy in pups:
            if spritecollideany(RegPuppy, vtiles):
                RegPuppy.hitwall()
            if spritecollideany(RegPuppy, player_grp):
                if RegPuppy.state == 1:
                    player.kill()1
                if RegPuppy.state == 0:
                    player.land()
                if RegPuppy.state == 0 and player.off_ground == False:
                    player.hitwall()
            if not spritecollideany(RegPuppy, htiles):
                RegPuppy.edge()

        #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        htiles.draw(screen)
        vtiles.draw(screen)
        pups.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
