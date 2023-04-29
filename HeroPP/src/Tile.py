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


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.variety = variety
        
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=3,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        
        surface.blit(
            settings.TEXTURES["floor"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["floors"][self.color][self.variety],
        )