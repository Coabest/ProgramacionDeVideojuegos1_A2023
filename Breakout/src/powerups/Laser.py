"""
ISPPJ1 2023
Study Case: Breakout

Author: Coalbert Ramirez
coabest15@gmail.com

This file contains the specialization of PowerUp to shoot 2 lasers from the sides of the paddle that destroy bricks.
"""
import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class Laser(PowerUp):
    """
    Power-up to shoot 2 lasers from the sides of the paddle that destroy bricks
    """

    def __init__(self, x: int, y: int) -> None:
        # Set Laser Powerup frame other than 8
        super().__init__(x, y, 8)
        self.ball_factory = Factory(Ball)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        # Define Laser behaviour
        self.in_play = False

