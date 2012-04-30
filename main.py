#!/usr/bin/env python


import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle

pygame.init()
SCREEN_SIZE = 800,360
screen = pygame.display.set_mode(SCREEN_SIZE)

from player import Player
from levels import Tile, Menu, Prologue1, Prologue2, L1A, L1, FoundTreat, L2, L2A, L3, L3A, L4, L4A, L5, FoundWhistle, L5A, L6, L6A, L7A, L7, L8A, L8, L9A, L9, L10A, L10, L11A, L11, L12A, L12, L13A, L13, L14A, L14, L15A, L15, Almost, Last
from puppies import Puppy, RegPuppy
from resources import play_song

SCREEN_SIZE = 800,360
BG_COLOR = 0, 200, 200  #remove later?

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    
    file_in = open("level.txt","r")
    for line in file_in:
        lvlnum = int(line)
    file_in.close()
    
    #initialize game
    lvls = [Menu(), Prologue1(), Prologue2(), L1A(), L1(), FoundTreat(), L2A(), L2(), L3A(), L3(), L4A(), L4(), L5A(), L5(), FoundWhistle(), L6A(), L6(), L7A(), L7(), L8A(), L8(), L9A(), L9(), L10A(), L10(), L11A(), L11(), L12A(), L12(), L13A(), L13(), L14A(), L14(), L15A(), L15(), Almost(), Last()]

    lvl = lvls[0]  #starting level

    in_menu = True
    player = Player(lvl.spawn, lvl, bounds)
    player_grp = GroupSingle(player) #spritegroup for player
    #game loop
    done = False
    clock = pygame.time.Clock()
    
    while not done:
        while in_menu == True:
            lvl = lvls[0]
            lvl.update()
            lvl.draw(screen)
            lvl.draw_titles(screen)
            pygame.display.flip()
            if lvl.newlvlnum > 0:
                in_menu = False
                level = lvl.newlvlnum
                lvl = lvls[lvl.newlvlnum]
                if lvl.state == 1:
                    file_in = open("level.txt","r")
                    for line in file_in:
                        level = (int(line) - 1)
                    file_in.close()
                    level = str(level)

                    file_out = open("level.txt", "w")  #temporary: rewrites to 0 at start
                    file_out.write(level)  #temp
                    file_out.close()   #temp

                    if lvl.type == "jungle":
                        lvl.song = "jungle1"
                        play_song(lvl.song)
                    elif lvl.type == "cliff":
                        lvl.song = "cliffs"
                        play_song(lvl.song)
                    elif lvl.type == "lab":
                        lvl.song = "lab"
                        play_song(lvl.song)
        # input
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
        
            if lvl.state == 1 and player.dying == False:
                if event.type == KEYDOWN and event.key == K_UP:
                    player.jump()
                elif event.type == KEYDOWN and event.key == K_r:  #reset level
                    player.reset()
                elif event.type == KEYDOWN and event.key == K_x: #whistle
                    player.whistle()
                elif event.type == KEYDOWN and event.key == K_z: #throw
                    player.throw()

            elif lvl.state == 0 or lvl.state == 3:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    player.endlevel()
                    play_song(lvl.song)
            if lvl.state != "menu" and lvl.state != "last":  #temporary: for skipping levels
                if event.type == KEYDOWN and event.key == K_k:
                    player.endlevel()

        file_in = open("level.txt","r")
        for line in file_in:
            lvlnum = int(line)
        file_in.close()

        lvl = lvls[lvlnum]
        player.level = lvl

        #update
        dt = clock.tick(30)
        if lvl.state == 1:
            pass
      #      lvl.draw_hud(screen, player)
        else:
            lvl.draw(screen)
        if lvl.state == "menu":
            lvl.update()
            lvl.draw_titles(screen)

        if lvl.state == 1:
            player.update(dt)
            player.waves.update()
            player.treats.update()
            lvl.pups.update(dt, bounds)
            lvl.tiles.update(dt, bounds)
            lvl.update()

        #draw
            screen.fill(BG_COLOR)
            lvl.draw(screen, player)
            player_grp.draw(screen)
            player.waves.draw(screen)
            player.treats.draw(screen)
            lvl.tiles.draw(screen)
            lvl.door.draw(screen)
            lvl.pups.draw(screen)
            lvl.draw_hud(screen, player)
 
            
        pygame.display.flip()
     #   clock.tick(30)

if __name__ == "__main__":
    main()
