"""
ISPPJ1 2023
Study Case: Breakout

Author: Coalbert Ramirez
coabest15@gmail.com

This file contains the specialization of PowerUp to shoot 2
lasers from the sides of the paddle that destroy bricks.
"""
import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.LaserBall import LaserBall
from src.powerups.PowerUp import PowerUp


class Laser(PowerUp):
    """
    Power-up to shoot 2 lasers from the sides of the paddle that destroy bricks
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 4)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        play_state.paddle.addLasers()

        self.in_play = False

