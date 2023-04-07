"""
ISPPJ1 2023
Study Case: Breakout

Authors:
Alejandro Mujica alejandro.j.mujic4@gmail.com
Coalbert Ramirez coabest15@gmail.com

This file contains the class LaserBalls.
"""
import random
from typing import Any, Tuple, Optional

import pygame

import settings
from src.LaserBall import LaserBall


class LaserBalls:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0
        self.frame = 0
        self.frame_freq = 15
        self.frame_timer = 0
        self.loaded = True
        self.fired = False
        self.in_play = True

        self.LLaser = LaserBall(x + 4, y + 4)
        self.RLaser = LaserBall(x + 56 - 4, y + 4)

    def update(self, dt: float, paddle_x: float, paddle_size: int, loaded: bool) -> None:
        self.LLaser.solve_world_boundaries()
        self.RLaser.solve_world_boundaries()
        self.in_play = self.LLaser.in_play or self.RLaser.in_play

        if not self.in_play:
            return
        
        self.loaded = loaded
        self.x = paddle_x
        
        # Laser blink effect
        self.frame_timer = (self.frame_timer + 1)%self.frame_freq
        if not self.frame_timer:
            self.frame ^= 1

        self.LLaser.update(dt, self.x + 4, self.fired)
        self.RLaser.update(dt, self.x + 32 + 32*paddle_size - 12, self.fired)
        
    def render(self, surface):
        if self.LLaser.in_play:
            surface.blit(
                self.LLaser.texture, (self.LLaser.x, self.LLaser.y), 
                settings.FRAMES["lasers"][self.frame]
            )

        if self.RLaser.in_play:
            surface.blit(
                self.RLaser.texture, (self.RLaser.x, self.RLaser.y),
                settings.FRAMES["lasers"][self.frame]
            )

    @staticmethod
    def get_intersection(r1: pygame.Rect, r2: pygame.Rect) -> Optional[Tuple[int, int]]:
        """
        Compute, if exists, the intersection between two
        rectangles.
        """
        if r1.x > r2.right or r1.right < r2.x or r1.bottom < r2.y or r1.y > r2.bottom:
            # There is no intersection
            return None

        # Compute x shift
        if r1.centerx < r2.centerx:
            x_shift = r2.x - r1.right
        else:
            x_shift = r2.right - r1.x

        # Compute y shift
        if r1.centery < r2.centery:
            y_shift = r2.y - r1.bottom
        else:
            y_shift = r2.bottom - r1.y

        return (x_shift, y_shift)
    
    def fire(self):
        self.fired = True

    def destroy(self, another: Any):
        ARect = another.get_collision_rect()
        
        LRect = self.get_intersection(self.LLaser.get_collision_rect(), ARect)
        if LRect is not None:
            self.LLaser.in_play = False

        RRect = self.get_intersection(self.RLaser.get_collision_rect(), ARect)
        if RRect is not None:
            self.RLaser.in_play = False