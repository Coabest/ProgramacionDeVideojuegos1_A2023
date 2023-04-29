"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class Enemy.
"""
import pygame

import settings
from gale.timer import Timer
import numpy as np

class Enemy:
    def __init__(self, i: int, j: int, power: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE

        self.frame = 0
        self.power = power
        
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

        def change_frame():
            self.frame = (self.frame + 1)%3

        Timer.every(np.random.randint(15,25)/100, change_frame)

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        if self.power < 7:
            surface.blit(
                settings.TEXTURES["enemies"],
                (self.x + offset_x, self.y + offset_y - 12),
                settings.FRAMES["enemies"][self.power][self.frame],
            )
        else:
            surface.blit(
                settings.TEXTURES["bosses"],
                (self.x + offset_x, self.y + offset_y),
                settings.FRAMES["bosses"][0][1],
            )