#!/usr/bin/env python

import pygame
import os
from os.path import abspath, dirname

ROOT_DIR = dirname( abspath(__file__) )
DATA_DIR = os.path.join(ROOT_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "images")
MUSIC_DIR = os.path.join(DATA_DIR, "music")

def play_song(song, times=-1):
    path = os.path.join(MUSIC_DIR, song + ".ogg")
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(times)

images = {}
def load_image(name):
    if name not in images:
      #  path = os.path.join(IMG_DIR, name + ".bmp")
        path = os.path.join(IMG_DIR, name)

        images[name] = pygame.image.load(path).convert()
    return images[name]
