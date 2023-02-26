/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the declaration of the class Bird.
*/

#pragma once

#include <SFML/Graphics.hpp>

class Bird
{
public:
    Bird(float _x, float _y, float w, float h) noexcept;

    Bird(const Bird&) = delete;

    Bird& operator = (Bird) = delete;

    sf::FloatRect get_collision_rect() const noexcept;

    int get_score() noexcept;

    void up_score() noexcept;

    void jump() noexcept;

    void move_left() noexcept;

    void move_right() noexcept;

    void update(float dt, bool powerUp_mode);

    void render(sf::RenderTarget& target) const noexcept;

private:
    int R, G, B;
    float x;
    float y;
    float width;
    float height;
    float vx;
    float vy;
    int score{0};
    sf::Sprite sprite;
    bool jumping{false};
};
