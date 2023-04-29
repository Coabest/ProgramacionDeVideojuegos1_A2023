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
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
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

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Steps: {self.steps}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"POWER: {self.board.score}/{self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

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
            print("tried")
        self.board.player.j = copy.deepcopy(new_j)
        self.board.player.i = copy.deepcopy(new_i)

        print(f"old: {old_i}, {old_j}  new: {new_i}, {new_j}  player: {self.board.player.i}, {self.board.player.j}")
        Timer.tween(
            0.6,
            [
                (self.board.player, {"x": self.board.player.j * settings.TILE_SIZE,
                                     "y": self.board.player.i * settings.TILE_SIZE})
            ],
            on_finish=tried
        )

        print(f"Values are {i}, {j}  ==  {new_i}, {new_j}")
        # if (j, i) != (new_j, new_i):
        if moved:
            self.steps += 1
            self.moving = False
        else:        
            
            print("Couldnt move")
            self.board.player.j = copy.deepcopy(old_j)
            self.board.player.i = copy.deepcopy(old_i)
            Timer.tween(
                0.6,
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
            if self.board.check_win():
                Timer.clear()
                settings.SOUNDS["next-level"].play()
                self.state_machine.change("begin", score=self.score, level=self.level+1)