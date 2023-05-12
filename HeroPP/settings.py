"""
ISPPJ1 2023
Game: Hero++

Authors:
Coalbert Ramirez
Paul Barreto

This file contains the game settings that include the association of the
inputs with an their ids, constants of values to set up the game, sounds,
textures, frames, and fonts.
"""
from pathlib import Path

import pygame

from gale import input_handler

from src.frames_utility import generate_tile_frames
from src.frames_utility import generate_floor_frames
from src.frames_utility import generate_obstacles_frames
from src.frames_utility import generate_enemies_frames
from src.frames_utility import generate_bosses_frames
from src.frames_utility import generate_skeletons_frames


input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "down")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "left")
input_handler.InputHandler.set_mouse_click_action(input_handler.MOUSE_BUTTON_1, "click")
input_handler.InputHandler.set_mouse_motion_action(input_handler.MOUSE_MOTION_UP, "mouse_up")
input_handler.InputHandler.set_mouse_motion_action(input_handler.MOUSE_MOTION_RIGHT, "mouse_right")
input_handler.InputHandler.set_mouse_motion_action(input_handler.MOUSE_MOTION_DOWN, "mouse_down")
input_handler.InputHandler.set_mouse_motion_action(input_handler.MOUSE_MOTION_LEFT, "mouse_left")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288

BOARD_WIDTH = 8
BOARD_HEIGHT = 8

BOARD_X = 240
BOARD_Y = 16

TILE_SIZE = 32

NUM_VARIETIES = 1
NUM_COLORS = 18

NUM_FLOORS = 5
NUM_FLOOR_VARIETY = 4

BACKGROUND_SCROLL_SPEED = 40
BACKGROUND_LOOPING_POINT = -1024 + VIRTUAL_WIDTH - 4 + 51

LEVEL_TIME = 3000

BASE_DIR = Path(__file__).parent

TEXTURES = {
    "background": pygame.image.load(BASE_DIR / "graphics" / "background.png"),
    "floor": pygame.image.load(BASE_DIR / "graphics" / "floor.png"),
    "obstacles": pygame.image.load(BASE_DIR / "graphics" / "obstacles.png"),
    "enemies": pygame.image.load(BASE_DIR / "graphics" / "enemies.png"),
    "bosses": pygame.image.load(BASE_DIR / "graphics" / "bosses.png"),
    "skeletons": pygame.image.load(BASE_DIR / "graphics" / "skeletons.png"),
}

FRAMES = {"floors": generate_floor_frames(TEXTURES["floor"]),
          "obstacles": generate_obstacles_frames(TEXTURES["obstacles"]),
          "enemies": generate_enemies_frames(TEXTURES["enemies"]),
          "bosses": generate_bosses_frames(TEXTURES["bosses"]),
          "skeletons": generate_skeletons_frames(TEXTURES["skeletons"]),
          }

pygame.mixer.init()

SOUNDS = {
    "clock": pygame.mixer.Sound(BASE_DIR / "sounds" / "clock.wav"),
    "error": pygame.mixer.Sound(BASE_DIR / "sounds" / "error.wav"),
    "game-over": pygame.mixer.Sound(BASE_DIR / "sounds" / "game-over.wav"),
    "match": pygame.mixer.Sound(BASE_DIR / "sounds" / "match.wav"),
    "next-level": pygame.mixer.Sound(BASE_DIR / "sounds" / "next-level.wav"),
    "select": pygame.mixer.Sound(BASE_DIR / "sounds" / "select.wav"),
}

pygame.mixer.music.load(BASE_DIR / "sounds" / "medieval_fantasy.mp3")

pygame.font.init()

FONTS = {
    "small": pygame.font.Font(BASE_DIR / "fonts" / "font.ttf", 12),
    "medium": pygame.font.Font(BASE_DIR / "fonts" / "font.ttf", 24),
    "large": pygame.font.Font(BASE_DIR / "fonts" / "font.ttf", 48),
    "huge": pygame.font.Font(BASE_DIR / "fonts" / "font.ttf", 64),
}
