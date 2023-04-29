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

class Obstacle:
    def __init__(self, i: int, j: int, level: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.level = level
        self.variety = random.randint(0, 2) # (0, setting.OBSTACLES_VARIETY)
        
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        surface.blit(
            settings.TEXTURES["obstacles"],
            (self.x + offset_x, self.y + offset_y - 8),
            settings.FRAMES["obstacles"][self.level][self.variety],
        )