"""
ISPPJ1 2023
Study Case: Breakout

Authors:
Alejandro Mujica alejandro.j.mujic4@gmail.com
Coalbert Ramirez coabest15@gmail.com

This file contains the class LaserBall.
"""
from typing import Any, Tuple, Optional

import pygame

import settings


class LaserBall:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.vy = -350

        self.texture = settings.TEXTURES["spritesheet"]
        self.in_play = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def solve_world_boundaries(self) -> None:
        if not self.in_play:
            return
        r = self.get_collision_rect()

        if r.top < 0:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.in_play = False

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def update(self, dt: float, x: float, fired: bool) -> None:
        if not self.in_play:
            return
        
        if fired:
            self.y += self.vy * dt
        else:
            self.x = x