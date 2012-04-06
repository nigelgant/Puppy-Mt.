#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide

from player import Player

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

        #update
        player_grp.update()

        #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        pygame.draw.line(screen, (0, 0, 0), (0, 200), (640, 200))
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
