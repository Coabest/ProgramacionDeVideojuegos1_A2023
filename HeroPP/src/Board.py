"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class Board.
"""
from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from src.Tile import Tile
from src.Obstacle import Obstacle
from src.Wall import Wall
from src.Player import Player
from src.Enemy import Enemy
import numpy as np

class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.score = 0
        self.floors: List[List[Tile]] = []
        self.obstacles: List[Obstacle] = []
        self.walls: List[List[Tile]] = []

        # start position
        self.start_row = 1
        self.start_col = 1

        # Goal position
        self.goal_row = 6
        self.goal_col = 6
        
        self.player = Player(self.start_row, self.start_col)

        self.enemies: List[List[Enemy]] = []

        self.level = 0

        self.__initialize_tiles()
        self.__initialize_obstacles(self.level)
        self.__initializa_enemies()
        


    def render(self, surface: pygame.Surface, r: int=None, c: int=None) -> None:
        # Floor
        for row in self.floors:
            for tile in row:
                tile.render(surface, self.x, self.y)

        for obstacle in self.obstacles:
            if obstacle is not None:
                obstacle.render(surface, self.x, self.y)

        # Enemies
        for row in self.enemies:
            for enemy in row:
                if enemy is not None:
                    enemy.render(surface, self.x, self.y)
        
        # Player    
        self.player.render(surface, self.x, self.y)
        
    def __initialize_tiles(self) -> None:
        self.floors = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]

        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):

                # Background floor
                # color = 0 # color = game.level
                color = self.level
                if (i == self.start_row and j == self.start_col or
                    i == self.goal_row and j == self.goal_col):
                    self.floors[i][j] = Tile(
                        i, j, color, settings.NUM_FLOOR_VARIETY - 1
                    )
                else:
                    # for wall in self.walls_1:
                    # if i == j:
                    #     self.floors[i][j] = Tile(
                    #         i, j, 1, random.randint(0, settings.NUM_FLOOR_VARIETY - 2)
                    #     )
                    # else:
                    self.floors[i][j] = Tile(
                        i, j, color, random.randint(0, settings.NUM_FLOOR_VARIETY - 2)
                    )


                # # Walls
                # if i == 0:
                #     self.walls[i][j] = Wall(i, j, 3)
                # if i == settings.BOARD_HEIGHT:
                #     self.walls[i][j] = Wall(i, j, 1)
                # if j == 0:
                #     self.walls[i][j] = Wall(i, j, 0)
                # if j == settings.BOARD_WIDTH:
                #     self.walls[i][j] = Wall(i, j, 2)

    def __initialize_obstacles(self, level: int) -> None:
        
        if level == 0:
            self.obstacles = [None for _ in range(6)]
            self.obstacles[0] = Obstacle(0, 0, level)
            self.obstacles[1] = Obstacle(2, 2, level)
            self.obstacles[2] = Obstacle(3, 3, level)
            self.obstacles[3] = Obstacle(4, 4, level)
            self.obstacles[4] = Obstacle(5, 5, level)
            self.obstacles[5] = Obstacle(7, 7, level)
        pass

    def __initializa_enemies(self) -> None:
        self.enemies = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if np.random.randint(0, 10) < 3:
                    power = random.randint(0, 5)
                    
                    if (i == self.start_row and j == self.start_col or
                        i == self.goal_row and j == self.goal_col):
                        continue
                    else:
                        if self.floors[i][j] is not None:
                            if i != j:
                                self.enemies[i][j] = Enemy(
                                    i, j, power
                                )

    def check_fight(self) -> None:
        for j in range(settings.BOARD_HEIGHT):
            for i in range(settings.BOARD_WIDTH):
                if self.enemies[i][j] is not None:
                    if (self.player.i, self.player.j) == (self.enemies[i][j].i, self.enemies[i][j].j):
                        # print(f"fight at: {enemy.j}, {enemy.i}")
                        # print(f"adding {self.enemies[i][j].power + 1} points")
                        self.score += self.enemies[i][j].power + 1
                        self.enemies[i][j] = None
        
        self.player.level = self.score // 25
    

    def check_win(self) -> bool:
        for row in self.enemies:
            for enemy in row:
                if enemy is not None:
                    return False
        return True

    def accessible_tile(self, i: int, j: int) -> bool:
        if ( i < 0 or i > settings.BOARD_HEIGHT - 1 or
             j < 0 or j > settings.BOARD_WIDTH - 1):
            print("NO FUERA DE RANGO")
            return False
        for obstacle in self.obstacles:
            if obstacle.i == i and obstacle.j == j:
                print("OBSTACLE")
                return False
        
        return True