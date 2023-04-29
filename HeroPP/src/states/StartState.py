"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the class StartState.
"""
import random

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState, StateMachine
from gale.text import render_text
from gale.timer import Timer

import settings


class StartState(BaseState):
    # colors we'll use to change the title text
    colors = [
        (32, 32, 250),
        (64, 64, 250),
        (96, 96, 250),
        (128, 128, 250),
        (160, 160, 250),
        (192, 192, 250),
    ]

    # A list of frames just for display.
    frames = []

    def __init__(self, state_machine: StateMachine, game) -> None:
        super().__init__(state_machine)
        self.game = game

    def enter(self) -> None:
        self.current_menu_item = 1

        def shift_colors():
            last = self.colors[5]

            for i in range(5, 0, -1):
                self.colors[i] = self.colors[i - 1]

            self.colors[0] = last

        self.color_timer = Timer.every(0.075, shift_colors)

        self.alpha_transition = 0

        # Generate the full tile list for display
        for _ in range(settings.BOARD_WIDTH * settings.BOARD_HEIGHT * 4):
            color = random.randint(0, settings.NUM_FLOORS - 1)
            variety = random.randint(0, settings.NUM_FLOOR_VARIETY - 1)
            self.frames.append(settings.FRAMES["floors"][color][variety])

        # def shif_floors():
        #     for frame in self.frames:
        #         color = random.randint(0, settings.NUM_FLOORS - 1)
        #         variety = random.randint(0, settings.NUM_FLOOR_VARIETY - 1)
        #         frame = settings.FRAMES["floors"][color][variety]
        
        # self.floor_timer = Timer.every(0.3, shif_floors)

        # A surface that supports alpha for the screen
        self.screen_alpha_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA
        )

        # A surface that supports alpha for each tile to draw
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (0, 0, 0, 255),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=3,
        )

        # A surface that supports alpha for the title and the menu
        self.text_alpha_surface = pygame.Surface((300, 58), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (200, 200, 250, 210), pygame.Rect(0, 0, 300, 58)
        )

        # If we have selected an option, we need to deactivate inputs while we
        # animate out.
        self.active = True

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def render(self, surface: pygame.Surface) -> None:
        # Render all the tiles and their shadows
        for i in range(settings.BOARD_HEIGHT - 1):
            for j in range(settings.BOARD_WIDTH + 6):
                x = j * (settings.TILE_SIZE + 4) + 6
                y = i * (settings.TILE_SIZE + 4) + 18

                # Frame position in the list
                f = i * settings.BOARD_HEIGHT + j

                surface.blit(self.tile_alpha_surface, (x + 2, y + 2))
                surface.blit(settings.TEXTURES["floor"], (x, y), self.frames[f])

        # keep the background and tiles a little darker than normal
        pygame.draw.rect(
            self.screen_alpha_surface,
            (0, 0, 0, 64),
            pygame.Rect(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT),
        )
        surface.blit(self.screen_alpha_surface, (0, 0))
        self.__draw_heroPP_text(surface, -60)
        self.__draw_options(surface, 12)

        # draw our transition rect; is normally fully transparent, unless we're
        # moving to a new state
        pygame.draw.rect(
            self.screen_alpha_surface,
            (255, 255, 255, self.alpha_transition),
            pygame.Rect(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT),
        )
        surface.blit(self.screen_alpha_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id in ("up", "down") and input_data.pressed:
            self.current_menu_item = 1 if self.current_menu_item == 2 else 2
            settings.SOUNDS["select"].play()
        elif input_id == "enter" and input_data.pressed:
            if self.current_menu_item == 1:
                self.active = False
                Timer.tween(
                    0.5,
                    [(self, {"alpha_transition": 255})],
                    on_finish=lambda: self.state_machine.change("begin"),
                )
            else:
                self.game.quit()

    def __draw_heroPP_text(self, surface: pygame.Surface, y: int) -> None:
        # draw semi-transparent rect behind HERO++
        surface.blit(
            self.text_alpha_surface,
            (settings.VIRTUAL_WIDTH // 2 - 152, settings.VIRTUAL_HEIGHT // 2 + y - 32),
        )
        title = "HERO++"
        offset_x = -108
        for i, letter in enumerate(title):
            render_text(
                surface,
                letter,
                settings.FONTS["huge"],
                (settings.VIRTUAL_WIDTH // 2) + offset_x,
                settings.VIRTUAL_HEIGHT // 2 - 60,
                self.colors[i],
                center=True,
                shadowed=True
            )
            offset_x += 44
        
    def __draw_options(self, surface: pygame.Surface, y: int) -> None:
        # surface.blit(
        #     self.text_alpha_surface,
        #     (settings.VIRTUAL_WIDTH // 2 - 152, settings.VIRTUAL_HEIGHT // 2 + y),
        # )

        text_color = (
            (99, 155, 255, 255) if self.current_menu_item == 1 else (48, 96, 130, 255)
        )

        render_text(
            surface,
            " Start ",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + y - 15,
            text_color,
            (200, 200, 250, 210),
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            " Best scores ",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + y + 45,
            (48, 96, 130, 255),
            (200, 200, 250, 210),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            " Select Level ",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + y + 15,
            (48, 96, 130, 255),
            (200, 200, 250, 210),
            center=True,
            shadowed=True,
        )

        text_color = (
            (99, 155, 255, 255) if self.current_menu_item == 2 else (48, 96, 130, 255)
        )

        render_text(
            surface,
            " Quit Game ",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + y + 75,
            text_color,
            (200, 200, 250, 210),
            center=True,
            shadowed=True,
        )
