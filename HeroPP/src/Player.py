"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class Player.
"""
import pygame

import settings
from gale.timer import Timer

class Player:
    def __init__(self, i: int, j: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE

        self.level = 0
        self.frame = 0
        self.power = 3
        self.health = 20
        self.alive = True
        
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

        def change_frame():
            self.frame = (self.frame + 1)%3

        Timer.every(0.3, change_frame)

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        
        surface.blit(
            settings.TEXTURES["skeletons"],
            (self.x + offset_x, self.y + offset_y - 12),
            settings.FRAMES["skeletons"][self.level][self.frame],
        )