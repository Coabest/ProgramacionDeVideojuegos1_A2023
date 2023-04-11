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
        self.frame_freq = 15
        self.frame_timer = 0
        # Duration of the Power-up in seconds
        self.timer = 10
        self.show = True

        self.texture = settings.TEXTURES["spritesheet"]
        self.frames = settings.FRAMES["shields"]
        self.in_play = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        if not self.in_play:
            return
        
        self.timer -= dt
        if self.timer < 0:
            self.in_play = False
        
        # Barrier blink effect starts at 4 seconds remaining
        if self.timer < 4:
            mod = int(max(7, self.frame_freq - int(1/(self.timer)*2)))
            self.frame_timer = (self.frame_timer + 1)%mod
            if not self.frame_timer:
                self.show ^= 1

    def render(self, surface: pygame.Surface) -> None:
        if self.show:
            surface.blit(self.texture, (self.x, self.y), self.frames[self.frame])
            surface.blit(self.texture, (self.x + 96, self.y), self.frames[self.frame])
            surface.blit(self.texture, (self.x + 96*2, self.y), self.frames[self.frame])
            surface.blit(self.texture, (self.x + 96*3, self.y), self.frames[self.frame])
            surface.blit(self.texture, (self.x + 96*4, self.y), self.frames[self.frame])
        

    def hit(self) -> None:
        self.y += 6
        if self.y > settings.VIRTUAL_HEIGHT:
            self.in_play = False