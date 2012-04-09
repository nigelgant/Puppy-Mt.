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
    player = Player(spawn, bounds)
    player_grp = GroupSingle(player) #spritegroup for player
    lvl1 = Level_1()
    lvl2 = Level_2()
    lvl = lvl1
    pups = Group(lvl.create_puppies())
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
                player.kill()
                player = Player(spawn, bounds)
                player_grp.add(player)


        #update
        player_grp.update()
        htiles = lvl.create_htiles()
        vtiles = lvl.create_vtiles()
        door = GroupSingle(lvl.door())

       # pups.add(lvl.create_puppies())
       # print pups
        pups.update()

        #collisions
        for Tile in htiles:
            if spritecollideany(Tile, player_grp):
              #  print player.rect.bottom, Tile.rect.top
                if player.rect.bottom > Tile.rect.top:
                    player.rect.bottom = Tile.rect.top
                    player.rect.bottom += 1
                    player.land()
                elif player.rect.right <= Tile.rect.left:
                    player.hitwall()
                    player.rect.right = Tile.rect.left
                    print "collide"
               # else:
                #    player.fall()

        for Tile in vtiles:
            if spritecollideany(Tile, player_grp):
                if Tile.rect.left < player.rect.right:
                    player.rect.left = Tile.rect.right
                    player.hitwall()

                elif Tile.rect.right > player.rect.left:
                    player.rect.right = Tile.rect.left
                    player.hitwall()

        if groupcollide(player_grp, door, True, True):
            lvl = lvl2
            pups.empty() #TEMPORARY
            pups.add(lvl.create_puppies())
            player = Player((spawn), bounds)
            player_grp.add(player)
            
        if not groupcollide(player_grp, htiles, False, False, None):
            player.fall()
            
        for player in player_grp:
            if player.rect.top > 480:
                player.kill()
                player = Player((spawn), bounds)
                player_grp.add(player)
                
        for RegPuppy in pups:
            if spritecollideany(RegPuppy, vtiles):
                RegPuppy.hitwall()
            if spritecollideany(RegPuppy, player_grp):
                if RegPuppy.state == 1:
                    player.kill()
                    player = Player((spawn), bounds)
                    player_grp.add(player)
                    
                if RegPuppy.state == 0:
                    if player.rect.bottom > RegPuppy.rect.top and player.rect.bottom < RegPuppy.rect.bottom:
                        player.rect.bottom = RegPuppy.rect.top
                        player.rect.bottom += 1
                        player.land()
      
                    elif player.rect.right < RegPuppy.rect.right:
                        player.rect.right = RegPuppy.rect.left
                    elif player.rect.left > RegPuppy.rect.left:
                        player.rect.left = RegPuppy.rect.right
 
            if not spritecollideany(RegPuppy, htiles):
                RegPuppy.edge()

        #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        htiles.draw(screen)
        vtiles.draw(screen)
        pups.draw(screen)
        door.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
