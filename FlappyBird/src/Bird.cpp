/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class Bird.
*/
#include <iostream>
#include <Settings.hpp>
#include <src/Bird.hpp>

Bird::Bird(float _x, float _y, float w, float h) noexcept
    : x{_x}, y{_y}, width{w}, height{h}, vy{0.f}, vx{0.0f}, R{255}, G{255}, B{255}, sprite{Settings::textures["bird"]}
{
    sprite.setPosition(x, y);
}

sf::FloatRect Bird::get_collision_rect() const noexcept
{
    return sf::FloatRect{x, y, width, height};
}

int Bird::get_score() noexcept
{
    return score;
}

void Bird::up_score() noexcept
{
    ++score;
}

void Bird::jump() noexcept
{
    if (!jumping)
    {
        jumping = true;
    }
}

void Bird::move_left() noexcept
{
    vx = -Settings::HORIZONTAL_SPEED;
}

void Bird::move_right() noexcept
{
    vx = Settings::HORIZONTAL_SPEED;
}

void Bird::update(float dt, bool powerUp_mode)
{
    if (powerUp_mode)
    {
        R = (R + 2) % 255;
        G = (G + R + 4) % 255;
        B = (B + R + G + 8) % 255;
        sprite.setColor(sf::Color(R, G, B));
    }
    else{
        sprite.setColor(sf::Color::White);
    }
    

    vx /= (1.0f + 1.f/60.f);
    vy += Settings::GRAVITY * dt;

    if (jumping)
    {
        Settings::sounds["jump"].play();
        vy = -Settings::JUMP_TAKEOFF_SPEED;
        jumping = false;
    }
    x = std::max(0.f, x + vx * dt);
    y = std::max(0.f, y + vy * dt);

    sprite.setPosition(x, y);
}

void Bird::render(sf::RenderTarget& target) const noexcept
{
    target.draw(sprite);
}