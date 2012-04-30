#!/usr/bin/env python

import pygame
import os
from os.path import abspath, dirname

ROOT_DIR = dirname( abspath(__file__) )
DATA_DIR = os.path.join(ROOT_DIR, "data")

SFX_DIR = os.path.join(DATA_DIR, "sfx")

IMG_DIR = os.path.join(DATA_DIR, "images")
MUSIC_DIR = os.path.join(DATA_DIR, "music")

def play_song(song, times=-1):
    if song is not None:
        path = os.path.join(MUSIC_DIR, song + ".ogg")
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(times)

images = {}
def load_image(name):
    pygame.init()
    if name not in images:
        path = os.path.join(IMG_DIR, name)

        images[name] = pygame.image.load(path).convert()
    return images[name]

sfx = {}
def load_sfx(name):
  #  if name not in _sfx:
    #    path = os.path.join(SFX_DIR, name + ".ogg")
   #     _sfx[name] = pygame.mixer.Sound(path)
  #  return _sfx[name]
    if name not in sfx:
        path = os.path.join(SFX_DIR, name + ".ogg")
        sfx[name] = pygame.mixer.Sound(path)

    return sfx[name]
