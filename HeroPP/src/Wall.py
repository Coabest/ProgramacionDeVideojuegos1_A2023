"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Luis Galaschow
Paul Barreto

This file contains the class Wall.
"""
import pygame

import settings


class Wall:
    def __init__(self, i: int, j: int, side: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.side = side

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        pass
        # surface.blit(
        #     settings.TEXTURES["floor"],
        #     (self.x + offset_x, self.y + offset_y),
        #     settings.FRAMES["walls"][self.side],
        # )