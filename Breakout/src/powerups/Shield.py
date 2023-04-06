"""
ISPPJ1 2023
Study Case: Breakout

Author: Coalbert Ramirez
coabest15@gmail.com

This file contains the specialization of PowerUp to stop the balls from falling past the paddle for a while
"""
import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class Shield(PowerUp):
    """
    Power-up to stop the balls from falling past the paddle for a while
    """

    def __init__(self, x: int, y: int) -> None:
        # Set  Powerup frame other than 8
        super().__init__(x, y, 8)
        self.ball_factory = Factory(Ball)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        # Define Shield behaviour
        self.in_play = False
