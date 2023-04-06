"""
ISPPJ1 2023
Study Case: Breakout

Author: Coalbert Ramirez
coabest15@gmail.com

This file contains the specialization of PowerUp to Stick one ball to the paddle
"""
import random
from typing import TypeVar

import settings
from src.powerups.PowerUp import PowerUp

class StickyPaddle(PowerUp):
    """
    Power-up to Stick one ball to the paddle
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 9)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        # Define StickyPaddle behaviour

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        play_state.paddle.sticky = True

        self.in_play = False
