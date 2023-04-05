"""
ISPPJ1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the specialization of PowerUp to add two more ball to the game.
"""
import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class TwoMoreBall(PowerUp):
    """
    Power-up to add two more ball to the game.
    """

    def __init__(self, x: int, y: int) -> None:
        # Set  Powerup frame other than 8
        super().__init__(x, y, 8)
        self.ball_factory = Factory(Ball)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        # Define Shield behaviour
        self.in_play = False
