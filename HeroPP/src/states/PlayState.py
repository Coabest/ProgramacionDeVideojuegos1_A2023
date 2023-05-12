"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class PlayState.
"""
from typing import Dict, Any, List

import pygame
import numpy as np
import copy

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text
from gale.timer import Timer

from src.Board import Board
import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        # self.board = Board(settings.BOARD_X, settings.BOARD_Y, level=self.level)
        self.score = enter_params["score"]

        self.timer = settings.LEVEL_TIME
        self.steps = 0
        self.moving = False

        # self.goal_score = self.level * 1.25 * 10000
        self.goal_score = 0
        for row in self.board.enemies:
            for enemy in row:
                if enemy is not None:
                    self.goal_score += enemy.power + 1

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 536), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (186, 186, 180, 244), pygame.Rect(0, 0, 212, 536)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, _: float) -> None:
        
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        surface.blit(self.text_alpha_surface, (16, 0))

        text_x = 30
        text_y = 6
        render_text(
            surface,
            f"Level {self.level}",
            settings.FONTS["medium"],
            text_x + 40,
            text_y,
            (115, 55, 115),
            shadowed=True,
        )
        render_text(
            surface,
            f"Steps: {self.steps}",
            settings.FONTS["medium"],
            text_x,
            text_y + 28,
            (99, 155, 255),
            shadowed=True,
        )
        if self.board.boss is not None:
            render_text(
                surface,
                f"BOSS PWR: {self.board.boss.power}",
                settings.FONTS["medium"],
                text_x,
                text_y + 56,
                (99, 155, 255),
                shadowed=True,
            )
        render_text(
            surface,
            f"PLAYER PWR: {self.board.player.power}",
            settings.FONTS["medium"],
            text_x,
            text_y + 84,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"PLAYER HP: {self.board.player.health}",
            settings.FONTS["medium"],
            text_x,
            text_y + 112,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            text_x,
            text_y + 140,
            (99, 155, 255),
            shadowed=True,
        )
        
        enemy_x = 30
        enemy_y = 170

        for i in range(6):
            render_text(
                surface,
                f"x {self.board.enemyType[i]}",
                settings.FONTS["medium"],
                70 if i < 3 else 170,
                enemy_y + (i*30 if i < 3 else (i-3)*30),
                (99, 155, 255),
                shadowed=True,
            )
            # render_text(
            #     surface,
            #     f"x {i+4}",
            #     settings.FONTS["medium"],
            #     170,
            #     enemy_y + i*30,
            #     (99, 155, 255),
            #     shadowed=True,
            # )
        # render_text( surface, "x 1", settings.FONTS["medium"],  70, enemy_y, (99, 155, 255), shadowed=True, )
        # render_text( surface, "x 2", settings.FONTS["medium"],  70, enemy_y + 30, (99, 155, 255), shadowed=True, )
        # render_text( surface, "x 3", settings.FONTS["medium"],  70, enemy_y + 60, (99, 155, 255), shadowed=True, )
        # render_text( surface, "x 4", settings.FONTS["medium"], 170, enemy_y, (99, 155, 255), shadowed=True, )
        # render_text( surface, "x 5", settings.FONTS["medium"], 170, enemy_y + 30, (99, 155, 255), shadowed=True, )
        # render_text( surface, "x 6", settings.FONTS["medium"], 170, enemy_y + 60, (99, 155, 255), shadowed=True, )
        render_text( surface, f"x {(self.level+1)*7 }",
                                     settings.FONTS["medium"], 120, enemy_y + 90, (99, 155, 255), shadowed=True, )

        surface.blit(settings.TEXTURES["enemies"], (enemy_x, enemy_y - 10), settings.FRAMES["enemies"][0][0],)
        surface.blit(settings.TEXTURES["enemies"], (enemy_x, enemy_y + 20), settings.FRAMES["enemies"][1][0],)
        surface.blit(settings.TEXTURES["enemies"], (enemy_x, enemy_y + 50), settings.FRAMES["enemies"][2][0],)
        surface.blit(settings.TEXTURES["enemies"], (enemy_x + 100, enemy_y - 10), settings.FRAMES["enemies"][3][0],)
        surface.blit(settings.TEXTURES["enemies"], (enemy_x + 100, enemy_y + 20), settings.FRAMES["enemies"][4][0],)
        surface.blit(settings.TEXTURES["enemies"], (enemy_x + 100, enemy_y + 50), settings.FRAMES["enemies"][5][0],)
        surface.blit(settings.TEXTURES["bosses"],  (enemy_x + 45, enemy_y + 85), settings.FRAMES["bosses"][0][1],)

    def move_player(self, direction: str):
        self.moving = True

        j, i = self.board.player.j, self.board.player.i
        old_i = copy.deepcopy(i)
        old_j = copy.deepcopy(j)
        new_i = copy.deepcopy(i)
        new_j = copy.deepcopy(j)
        moved = True
        if direction == "up":
            new_i = new_i - 1
            if not self.board.accessible_tile(new_i, j):
                new_i = copy.deepcopy(old_i)
                # self.board.player.i = max(0, self.board.player.i - 1)
        elif direction == "down":
            new_i = new_i + 1
            if not self.board.accessible_tile(new_i, j):
                new_i = copy.deepcopy(old_i)
                # self.board.player.i = min(settings.BOARD_HEIGHT - 1, self.board.player.i + 1)
        elif direction == "left":
            new_j = new_j - 1
            if not self.board.accessible_tile(i, new_j):
                new_j = copy.deepcopy(old_j)
                # self.board.player.j = max(0, self.board.player.j - 1)
        elif direction == "right":
            new_j = new_j + 1
            if not self.board.accessible_tile(i, new_j):
                moved = False
                # new_j = copy.deepcopy(old_j)
                # self.board.player.j = min(settings.BOARD_WIDTH - 1, self.board.player.j + 1)
        
        # if (j, i) != (self.board.player.j, self.board.player.i):
        #     self.steps += 1


        def move_completed():
            self.moving = False

        def tried():
            # print("tried")
            pass
        self.board.player.j = copy.deepcopy(new_j)
        self.board.player.i = copy.deepcopy(new_i)

        # print(f"old: {old_i}, {old_j}  new: {new_i}, {new_j}  player: {self.board.player.i}, {self.board.player.j}")
        Timer.tween(
            0.2,
            [
                (self.board.player, {"x": self.board.player.j * settings.TILE_SIZE,
                                     "y": self.board.player.i * settings.TILE_SIZE})
            ],
            on_finish=tried
        )

        # print(f"Values are {i}, {j}  ==  {new_i}, {new_j}")
        # if (j, i) != (new_j, new_i):
        if moved:
            self.steps += 1
            self.moving = False
        else:        
            
            print("Couldnt move")
            self.board.player.j = copy.deepcopy(old_j)
            self.board.player.i = copy.deepcopy(old_i)
            Timer.tween(
                0.2,
                [
                    (self.board.player, {"x": self.board.player.j * settings.TILE_SIZE,
                                         "y": self.board.player.i * settings.TILE_SIZE})
                ],
                on_finish=move_completed,
            )


    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_id == "click" and input_data.pressed:
            pass
        elif input_id == "click" and input_data.released:
            pass
        
        if not self.moving:
            if input_id == "up" and input_data.pressed:
                self.move_player("up")

            elif input_id == "down" and input_data.pressed:
                self.move_player("down")

            elif input_id == "left" and input_data.pressed:
                self.move_player("left")

            elif input_id == "right" and input_data.pressed:
                self.move_player("right")
            
            self.board.check_fight()
            print(f"HP: {self.board.player.health}")
            if self.board.player.health == 0:
                settings.SOUNDS["game-over"].play()
                self.state_machine.change("game-over", score=self.score)

            if self.board.check_win():
                Timer.clear()
                settings.SOUNDS["next-level"].play()
                if self.level < 4:
                    self.state_machine.change("begin", score=self.score, level=self.level+1)
                else:
                    self.state_machine.change("start") #self.state_machine.change("win")