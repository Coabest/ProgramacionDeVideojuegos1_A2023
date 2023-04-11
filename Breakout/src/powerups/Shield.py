"""
ISPPJ1 2023
Study Case: Breakout

Author: Coalbert Ramirez
coabest15@gmail.com

This file contains the specialization of PowerUp to stop the balls from falling past the paddle for a while
"""
from typing import TypeVar

from gale.factory import Factory
from src.Barrier import Barrier
from src.powerups.PowerUp import PowerUp


class Shield(PowerUp):
    """
    Power-up to stop the balls from falling past the paddle for a while
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 1)
        self.barrier_factory = Factory(Barrier)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.barrier = self.barrier_factory.create(-24, play_state.paddle.y + 16)
        self.in_play = False
