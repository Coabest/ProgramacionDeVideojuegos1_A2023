"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the main program to run the game.
"""
import settings
from src.HeroPP import HeroPP

if __name__ == "__main__":
    heroPP = HeroPP(
        "HERO++",
        settings.WINDOW_WIDTH,
        settings.WINDOW_HEIGHT,
        settings.VIRTUAL_WIDTH,
        settings.VIRTUAL_HEIGHT,
    )
    heroPP.exec()
