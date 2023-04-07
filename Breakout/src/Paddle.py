"""
ISPPJ1 2023
Study Case: Breakout

Authors:
Alejandro Mujica alejandro.j.mujic4@gmail.com
Coalbert Ramirez coabest15@gmail.com

This file contains the class Paddle.
"""
import pygame

import settings

from gale.factory import Factory
from src.LaserBall import LaserBall
from src.LaserBalls import LaserBalls


class Paddle:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 64
        self.height = 16

        # By default, the blue paddle
        self.skin = 0

        # By default, the 64-pixels-width paddle.
        self.size = 1

        self.texture = settings.TEXTURES["spritesheet"]
        self.frames = settings.FRAMES["paddles"]

        # The paddle only moves horizontally
        self.vx = 0

        self.sticky = False
        self.ballStuck = False

        self.laser_factory = Factory(LaserBalls)
        self.laserBalls = None
        self.loaded = False

    def resize(self, size: int) -> None:
        self.size = size
        self.width = (self.size + 1) * 32

    def dec_size(self):
        self.resize(max(0, self.size - 1))

    def inc_size(self):
        self.resize(min(3, self.size + 1))

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        next_x = self.x + self.vx * dt
        if self.vx < 0:
            self.x = max(0, next_x)
        else:
            self.x = min(settings.VIRTUAL_WIDTH - self.width, next_x)

        if self.laserBalls is not None:
            # Remove lasers that are not in play
            if not self.laserBalls.in_play:
                self.laserBalls = None
                self.loaded = False
                return
            self.laserBalls.update(dt, self.x, self.size, self.loaded)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y), self.frames[self.skin][self.size])
        if self.laserBalls is not None:
            self.laserBalls.render(surface)

    def addLasers(self) -> None:
        self.laserBalls = self.laser_factory.create(self.x, self.y)
        self.loaded = True

    def fire(self) -> None:
        self.laserBalls.fire()
        self.loaded = False
