"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class Tile.
"""
import pygame

import settings
import random
from gale.timer import Timer

class Obstacle:
    def __init__(self, i: int, j: int, level: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.level = level
        self.frame = random.randint(0, 5) # (0, setting.OBSTACLES_FRAMES)

        def change_frame():
            self.frame = (self.frame + 1)%6

        if self.level > 2:
            Timer.every(0.3, change_frame)
        
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:

        centering_y = -8
        if self.level == 4:
            centering_y = 0

        surface.blit(
            settings.TEXTURES["obstacles"],
            (self.x + offset_x, self.y + offset_y + centering_y),
            settings.FRAMES["obstacles"][self.level][self.frame],
        )