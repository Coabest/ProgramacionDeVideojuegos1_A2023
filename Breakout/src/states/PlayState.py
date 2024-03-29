"""
ISPPJ1 2023
Study Case: Breakout

Authors:
Alejandro Mujica alejandro.j.mujic4@gmail.com
Coalbert Ramirez coabest15@gmail.com

This file contains the class to define the Play state.
"""
import random

import pygame

from gale.factory import AbstractFactory
from gale.state_machine import BaseState
from gale.input_handler import InputHandler, InputData, InputData
from gale.text import render_text

import settings
import src.powerups


class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])

        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-160, -120)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")
        
        #   65% chance of not dropping anything
        #   35% chance divided between the available Power-ups
        #       - Two more balls
        #       - Sticky Paddle
        #       - Laser
        #       - Shield
        self.powerup_chance = 0.35

        self.barrier = params.get("barrier", None)

        InputHandler.register_listener(self)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def update(self, dt: float) -> None:
        self.paddle.update(dt)

        if self.paddle.ballStuck:
            self.paddle.sticky_timer -= dt

            if self.paddle.sticky_timer < 0:
                self.paddle.ballStuck = False

                for ball in self.balls:
                    if ball.stuck:
                        ball.unstick()
                
                
        # Check left laser collision with brickset
        laserBalls = self.paddle.laserBalls
        if laserBalls is not None:
            LLaser = laserBalls.LLaser
            if LLaser.collides(self.brickset) and LLaser.in_play:
                Lbrick = self.brickset.get_colliding_brick(LLaser.get_collision_rect())
                if Lbrick is not None:
                    Lbrick.hit()
                    self.score += Lbrick.score()
                    laserBalls.destroy(Lbrick)
                    self.brickset.update(dt)

        # Check right laser collision with brickset
        laserBalls = self.paddle.laserBalls
        if laserBalls is not None:
            RLaser = laserBalls.RLaser
            if RLaser.collides(self.brickset) and RLaser.in_play:
                Rbrick = self.brickset.get_colliding_brick(RLaser.get_collision_rect())
                if Rbrick is not None:
                    Rbrick.hit()
                    self.score += Rbrick.score()
                    laserBalls.destroy(Rbrick)
                    self.brickset.update(dt)

        if self.barrier is not None:
            self.barrier.update(dt)
            if not self.barrier.in_play:
                self.barrier = None

        for ball in self.balls:
            ball.update(dt, self.paddle.x)
            ball.solve_world_boundaries()

            # Check collision with the paddle
            if ball.collides(self.paddle):
                if not self.paddle.sticky:
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)
                else:
                    ball.stick()
                    self.paddle.stickBall()
                                    
                if not ball.stuck:
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
            
            # Check collision with the barrier
            if self.barrier is not None and ball.collides(self.barrier):
                settings.SOUNDS["paddle_hit"].stop()
                settings.SOUNDS["paddle_hit"].play()
                ball.rebound(self.barrier)
                self.barrier.hit()
                if not self.barrier.in_play:
                    self.barrier = None

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            generatePowerup = random.random()

            # Power-up selection
            if generatePowerup < self.powerup_chance:
                # taken Power-ups are not elegible to drop again
                posible_powerups = ["two"]
                if not self.paddle.ballStuck:
                    posible_powerups.append("sticky")
                if not self.paddle.loaded:
                    posible_powerups.append("laser")
                if self.barrier is None:
                    posible_powerups.append("barrier")

                selectPowerup = random.choice(posible_powerups)

                # Two more balls
                if selectPowerup == "two":
                    r = brick.get_collision_rect()
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Sticky Paddle
                elif selectPowerup == "sticky":
                    r = brick.get_collision_rect()
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("StickyPaddle").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )

                # Laser
                elif selectPowerup == "laser":
                    r = brick.get_collision_rect()
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("Laser").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )
                # Shield
                elif selectPowerup == "barrier":
                    r = brick.get_collision_rect()
                    self.powerups.append(
                        self.powerups_abstract_factory.get_factory("Shield").create(
                            r.centerx - 8, r.centery - 8
                        )
                    )

        # Check earn life
        if self.score >= self.points_to_next_live:
            settings.SOUNDS["life"].play()
            self.lives = min(3, self.lives + 1)
            self.live_factor += 0.5
            self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

        # Check growing up of the paddle
        if self.score >= self.points_to_next_grow_up:
            settings.SOUNDS["grow_up"].play()
            self.points_to_next_grow_up += (
                settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
            )
            self.paddle.inc_size()

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.in_play]

        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.laserBalls = None
                self.paddle.loaded = False
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.in_play]

        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.paddle.laserBalls = None
            self.paddle.loaded = False
            self.balls = []
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        self.brickset.render(surface)

        self.paddle.render(surface)

        if self.barrier is not None:
            self.barrier.render(surface)

        for ball in self.balls:
            ball.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0

        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0

        elif input_id == "enter" and self.paddle.ballStuck:
            for ball in self.balls:
                if ball.stuck:
                    ball.unstick()
            self.paddle.unstickBall()

        elif input_id == "move_down" and self.paddle.loaded:
            self.paddle.fire()
            self.paddle.loaded = False

        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
                barrier=self.barrier,
            )
