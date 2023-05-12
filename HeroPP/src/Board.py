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
    def __init__(self, x: int, y: int, level: int) -> None:
        self.x = x
        self.y = y
        self.score = 0
        self.floors: List[List[Tile]] = []
        self.obstacles: List[Obstacle] = []
        self.walls: List[List[Tile]] = []

        self.level = level

        # start position PLAYER
        self.start_row = 1
        self.start_col = 1
        self.player = Player(self.start_row, self.start_col)
        
        # Goal position BOSS
        self.goal_row = 6
        self.goal_col = 6
        self.boss = Enemy(self.goal_row, self.goal_col, (self.level + 1)*15)

        # Enemies
        self.enemies_in_level: List[Enemy] = []
        self.enemies: List[List[Enemy]] = []


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

        # Boss
        if self.boss is not None:
            self.boss.render(surface, self.x, self.y)
        
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
                    self.floors[i][j] = Tile(
                        i, j, color, random.randint(0, settings.NUM_FLOOR_VARIETY - 2)
                    )



    def __initialize_obstacles(self, level: int) -> None:
        
        # Obstacles
        level_1 = [[0,0],[0,1],[0,2],[1,0],[4,1],[1,2],[0,5],[1,6],
                   [2,2],[3,3],[4,4],[5,5],[7,7],[7,1],[7,2],[7,4]]
        
        level_2 = [[0,0],[0,1],[0,2],[1,0],[4,1],[1,2],[0,5],[1,6],
                   [2,2],[3,3],[4,4],[5,5],[7,7],[7,1],[7,2],[7,4]]
        
        level_3 = [[0,0],[0,1],[0,2],[1,0],[4,1],[1,2],[0,5],[1,6],
                   [2,2],[3,3],[4,4],[5,5],[7,7],[7,1],[7,2],[7,4]]
        
        level_4 = [[0,0],[0,1],[0,2],[1,0],[4,1],[1,2],[0,5],[1,6],
                   [2,2],[3,3],[4,4],[5,5],[7,7],[7,1],[7,2],[7,4]]
        
        level_5 = [[0,0],[0,1],[0,2],[1,0],[4,1],[1,2],[0,5],[1,6],
                   [2,2],[3,3],[4,4],[5,5],[7,7],[7,1],[7,2],[7,4]]

        self.obstacles = [None for _ in range(16)]

        if level == 0:
            for i in range(16):
                self.obstacles[i] = Obstacle(level_1[i][0], level_1[i][1], level)
            # self.obstacles = [None for _ in range(16)]
            # self.obstacles[0] = Obstacle(0, 0, level)
            # self.obstacles[1] = Obstacle(2, 2, level)
            # self.obstacles[2] = Obstacle(3, 3, level)
            # self.obstacles[3] = Obstacle(4, 4, level)
            # self.obstacles[4] = Obstacle(5, 5, level)
            # self.obstacles[5] = Obstacle(7, 7, level)
            

        # self.obstacles = [None for _ in range(5)]
            # self.obstacles[0] = Obstacle(0, 0, level)
            # self.obstacles[1] = Obstacle(0, 1, level)
            # self.obstacles[2] = Obstacle(0, 2, level)
            # self.obstacles[3] = Obstacle(1, 0, level)
            # self.obstacles[4] = Obstacle(4, 1, level)
            # self.obstacles[5] = Obstacle(1, 2, level)

            # self.obstacles[6] = Obstacle(0, 5, level)
            # self.obstacles[7] = Obstacle(1, 6, level)
            
        # self.obstacles[0] = Obstacle(2, 2, level)
        # self.obstacles[1] = Obstacle(3, 3, level)
        # self.obstacles[3] = Obstacle(4, 4, level)
        # self.obstacles[4] = Obstacle(5, 5, level)

            # self.obstacles[13] = Obstacle(7, 1, level)
            # self.obstacles[14] = Obstacle(7, 2, level)
            # self.obstacles[15] = Obstacle(7, 4, level)

        pass

        
        pass

    def __initializa_enemies(self) -> None:
        self.enemies = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if np.random.randint(0, 10) < 1:
                    power = random.randint(0, 5)
                    
                    if (i == self.start_row and j == self.start_col or
                        i == self.goal_row and j == self.goal_col or i == 0):
                        continue
                    else:
                        if self.floors[i][j] is not None:
                            if i != j:
                                self.enemies[i][j] = Enemy(
                                    i, j, power
                                )

    def check_fight(self) -> None:
        # Against boss
        if self.boss is not None:
            print(f"Boss: {self.boss.power}")
            if (self.player.i, self.player.j) == (self.boss.i, self.boss.j):
                self.player.health = max(0, self.player.health - self.boss.power)
                if self.player.health == 0:
                    self.player.alive = False
                    return
                self.score += self.boss.power + 1
                self.boss = None
            
        # Against normal enemies
        for j in range(settings.BOARD_HEIGHT):
            for i in range(settings.BOARD_WIDTH):
                if self.enemies[i][j] is not None:
                    if (self.player.i, self.player.j) == (self.enemies[i][j].i, self.enemies[i][j].j):
                        # print(f"fight at: {enemy.j}, {enemy.i}")
                        # print(f"adding {self.enemies[i][j].power + 1} points")
                        # self.player.health = max(0, self.player.health - self.enemies[i][j].power)
                        # if self.player.health == 0:
                        #     self.player.alive = False
                        #     return
                        # if self.player.power >= self.enemies[i][j].power:
                        self.player.power += (self.enemies[i][j].power + 1)
                        self.score += self.enemies[i][j].power + 1
                        self.enemies[i][j] = None
                        # else:
                            # self.player.alive = False
        
        self.player.level = min(4, self.score // 25)
    

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
            if obstacle is not None:
                if obstacle.i == i and obstacle.j == j:
                    print("OBSTACLE")
                    return False
        
        return True