"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains a function to fetch and store the tile frames.
"""
from typing import List

import pygame

import settings


def generate_tile_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    rows_counter = 0

    # There are 9 rows
    for _ in range(9):

        # There are two sets of 6 tiles of the same color and different
        # variety.
        for _ in range(2):
            frames.append([])
            for _ in range(6):
                frames[rows_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
                x += settings.TILE_SIZE
            rows_counter += 1

        y += settings.TILE_SIZE
        x = 0

    return frames

def generate_floor_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    col_counter = 0

    for _ in range(5):
        frames.append([])
        for _ in range(4):
            frames[col_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
            y += settings.TILE_SIZE
        col_counter += 1

        x += settings.TILE_SIZE
        y = 0

    return frames

def generate_obstacles_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    rows_counter = 0

    for _ in range(5):
        frames.append([])

        for _ in range(6):
            frames[rows_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
            x += settings.TILE_SIZE
        rows_counter += 1

        y += settings.TILE_SIZE
        x = 0

    return frames

# Enemies frames
def generate_enemies_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    rows_counter = 0

    for _ in range(7):
        frames.append([])
        for _ in range(3):
            frames[rows_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
            x += settings.TILE_SIZE

        rows_counter += 1

        y += settings.TILE_SIZE
        x = 0

    return frames

def generate_bosses_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    rows_counter = 0

    for _ in range(1):
        frames.append([])
        for _ in range(2):
            frames[rows_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
            x += settings.TILE_SIZE

        rows_counter += 1

        y += settings.TILE_SIZE
        x = 0

    return frames

def generate_skeletons_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    frames = []
    x, y = 0, 0
    rows_counter = 0

    # There are 9 rows
    for _ in range(5):
        for _ in range(1):
            frames.append([])
            for _ in range(3):
                frames[rows_counter].append(pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
                x += settings.TILE_SIZE
            rows_counter += 1
        y += settings.TILE_SIZE
        x = 0

    return frames
