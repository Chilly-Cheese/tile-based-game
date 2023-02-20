import pygame as pg
from settings import *
from os import path

class Map:
    def __init__(self, game_folder, levelMaps, mapIndex):
        self.map_data = []
        with open(path.join(game_folder, levelMaps[mapIndex]), 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())

        self.tilewidth = len(self.map_data[0])
        self.tileheight = len(self.map_data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
    def checkIndex(self, mapIndex, levelMaps):
        if mapIndex < (len(levelMaps)-1):
            return mapIndex + 1
        else:
            return 0

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
