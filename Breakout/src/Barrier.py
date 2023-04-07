"""
ISPPJ1 2023
Study Case: Breakout

Authors:
Coalbert Ramirez coabest15@gmail.com

This file contains the class Barrier.
"""
import pygame

import settings

from gale.factory import Factory


class Barrier:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 96*5
        self.height = 16

        # Green paddle segment
        self.frame = 0
        self.in_play = True

        self.texture = settings.TEXTURES["spritesheet"]
        self.frames = settings.FRAMES["shields"]

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y), self.frames[self.frame])
        surface.blit(self.texture, (self.x + 96, self.y), self.frames[self.frame])
        surface.blit(self.texture, (self.x + 96*2, self.y), self.frames[self.frame])
        surface.blit(self.texture, (self.x + 96*3, self.y), self.frames[self.frame])
        surface.blit(self.texture, (self.x + 96*4, self.y), self.frames[self.frame])

    def hit(self) -> None:
        self.y += 6
        if self.y > settings.VIRTUAL_HEIGHT:
            self.in_play = False