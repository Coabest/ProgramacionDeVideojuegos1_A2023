"""
ISPPJ1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""
from typing import Dict, Any, List

import pygame
import numpy as np

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

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        # Mouse position
        self.mx = -1
        self.my = -1
        self.grabbed_tile = None


        # Original position of grabbed tile
        self.record_position = False
        self.old_i = -1
        self.old_j = -1
        self.old_y = -1
        self.old_x = -1
        
        # Grabbed tile position following cursor
        self.new_y = -1
        self.new_x = -1

        self.matches_found = False

        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 10000

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
        # Check if there are no posible matches to be made
        while not self.board.matches_posible():
            self.board = Board(settings.BOARD_X, settings.BOARD_Y)

        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = self.mx * settings.VIRTUAL_WIDTH / settings.WINDOW_WIDTH
        self.my = self.my * settings.VIRTUAL_HEIGHT / settings.WINDOW_HEIGHT
        
        if self.record_position:
            self.old_y = self.board.tiles[self.highlighted_i1][self.highlighted_j1].y
            self.old_x = self.board.tiles[self.highlighted_i1][self.highlighted_j1].x
            self.old_i = self.board.tiles[self.highlighted_i1][self.highlighted_j1].i
            self.old_j = self.board.tiles[self.highlighted_i1][self.highlighted_j1].j
            self.record_position = False
        
        if self.grabbed_tile is not None:                
            # put center of the grabbed tile on cursor
            new_y = self.my - settings.BOARD_Y - settings.TILE_SIZE / 2
            new_x = self.mx - settings.BOARD_X - settings.TILE_SIZE / 2

            # Dont allow the tile to go further than a tile away in any direction
            # Vertical
            # - Above
            new_y = max(
                new_y,
                0,
                (self.highlighted_i1 - 1) * settings.TILE_SIZE + 1
            )
            # - Bellow
            new_y = min(
                new_y,
                (settings.BOARD_HEIGHT - 1) * settings.TILE_SIZE,
                (self.highlighted_i1 + 1) * settings.TILE_SIZE - 1
            )
            # Horizontal
            # - To the left
            new_x = max(
                new_x,
                0,
                (self.highlighted_j1 - 1) * settings.TILE_SIZE + 1
            )
            # - To the right
            new_x = min(
                new_x,
                (settings.BOARD_WIDTH - 1) * settings.TILE_SIZE,
                (self.highlighted_j1 + 1) * settings.TILE_SIZE - 1
            )

            # Don't allow diagonal movement
            # if np.abs(new_x - self.old_x) <= np.abs(new_y - self.old_y):
            #     new_x = self.old_x
            # else:
            #     new_y = self.new_y

            self.new_x = new_x
            self.new_y = new_y

            self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = new_y
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = new_x

        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.highlighted_tile:
            # Render grabbed tile above other tiles
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].render(surface, settings.BOARD_X, settings.BOARD_Y)
            self.board.tiles[self.highlighted_i1][self.highlighted_j1].render(surface, settings.BOARD_X, settings.BOARD_Y)
            
            x = self.board.tiles[self.highlighted_i1][self.highlighted_j1].x + settings.BOARD_X
            y = self.board.tiles[self.highlighted_i1][self.highlighted_j1].y + settings.BOARD_Y
            surface.blit(self.tile_alpha_surface, (x, y))

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
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
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

    def pop_cross(self) -> None:
        i = self.old_i
        j = self.old_j

        print(f" Called pop_cross from tile ({i}, {j})")
        matches = self.board.calculate_cross_matches([self.board.tiles[i][j]])
        self.score += settings.BOARD_HEIGHT + settings.BOARD_WIDTH - 1
        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            1.0,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

    def pop_star(self) -> None:
        i = self.old_i
        j = self.old_j

        print(f" Called pop_cross from tile ({i}, {j})")
        matches = self.board.calculate_star_matches([self.board.tiles[i][j]])
        self.score += len(matches) * 50
        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            1.0,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        # Grabbing tile
        if input_id == "click" and input_data.pressed:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE
            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j <= settings.BOARD_WIDTH:
                self.highlighted_tile = True
                self.highlighted_i1 = i
                self.highlighted_j1 = j
                
                self.grabbed_tile = self.board.tiles[self.highlighted_i1][
                            self.highlighted_j1
                        ]
                self.record_position = True

        # Releasing tile
        elif input_id == "click" and input_data.released:
            if self.highlighted_tile:
                pos_x, pos_y = input_data.position
                pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
                pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE

                tile_swapped = False

                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j <= settings.BOARD_WIDTH:
                    self.highlighted_tile = True
                    self.highlighted_i2 = i
                    self.highlighted_j2 = j
                    
                    di = abs(self.highlighted_i2 - self.highlighted_i1)
                    dj = abs(self.highlighted_j2 - self.highlighted_j1)
                    if di <= 1 and dj <= 1 and di != dj:
                        tile_swapped = True
                        self.active = False
                        tile1 = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                        tile1.y = self.old_y
                        tile1.x = self.old_x
                        tile2 = self.board.tiles[self.highlighted_i2][self.highlighted_j2]

                        def arrive():
                            tile1 = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                            tile2 = self.board.tiles[self.highlighted_i2][self.highlighted_j2]
                            
                            (self.board.tiles[tile1.i][tile1.j], self.board.tiles[tile2.i][tile2.j],) = (
                             self.board.tiles[tile2.i][tile2.j], self.board.tiles[tile1.i][tile1.j],)
                            
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                            tile2.i, tile2.j, tile1.i, tile1.j,)

                            self.__calculate_matches([tile1, tile2])

                            if not self.matches_found:
                                tile1 = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                                tile2 = self.board.tiles[self.highlighted_i2][self.highlighted_j2]
                                
                                (self.board.tiles[tile1.i][tile1.j], self.board.tiles[tile2.i][tile2.j],) = (
                                self.board.tiles[tile2.i][tile2.j], self.board.tiles[tile1.i][tile1.j],)
                                
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                tile2.i, tile2.j, tile1.i, tile1.j,)

                                Timer.tween(
                                    0.25,
                                    [
                                        (tile1, {"x": tile2.x, "y": tile2.y}),
                                        (tile2, {"x": tile1.x, "y": tile1.y}),
                                    ],
                                )
                        
                        # if self.matches_found:
                        # Swap tiles
                        Timer.tween(
                            0.25,
                            [
                                (tile1, {"x": tile2.x, "y": tile2.y}),
                                (tile2, {"x": tile1.x, "y": tile1.y}),
                            ],
                            on_finish=arrive,
                        )
                        self.matches_found = False

                # if there is not a tile swap, return the grabbed tile to its original position
                if not tile_swapped:
                    if self.board.tiles[self.highlighted_i1][self.highlighted_j1].is_cross:
                        print("Picked up a cross power up")
                        self.pop_cross()
                    elif self.board.tiles[self.highlighted_i1][self.highlighted_j1].is_star:
                        print("Picked up a star power up")
                        self.pop_star()
                    else:
                        self.board.tiles[self.highlighted_i1][self.highlighted_j1].y = self.old_y
                        self.board.tiles[self.highlighted_i1][self.highlighted_j1].x = self.old_x
            self.grabbed_tile = None
            self.highlighted_tile = False
            

    def __calculate_matches(self, tiles: List) -> None:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            self.matches_found = False
            self.active = True
            return
        
        self.matches_found = True

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            if len(match) == 4:
                tile = match[-1]
                self.board.tiles[tile.i][tile.j].is_cross = True
                for match_ in self.board.matches:
                    for tile in match_:
                        print(f"({tile.i},{tile.j})", end='')
                print("")
                self.board.matches[0] = self.board.matches[0][:-1]
                match = match[:-1]
                self.score += 50
            
            if len(match) >= 5:
                tile = match[-1]
                self.board.tiles[tile.i][tile.j].is_star = True
                self.board.matches[0] = self.board.matches[0][:-1]
                match = match[:-1]
                self.score += 50
                
            self.score += len(match) * 50

        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
