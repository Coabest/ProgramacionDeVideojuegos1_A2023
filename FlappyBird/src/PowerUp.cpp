/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class PowerUp.
*/
#include <iostream>
#include <Settings.hpp>
#include <src/PowerUp.hpp>

PowerUp::PowerUp(float _x, float _y) noexcept
    : x{_x}, y{_y}, sprite{Settings::textures["PowerUp"]}
{
    set_reachable(true);
}

sf::FloatRect PowerUp::get_collision_rect() const noexcept
{
    return sf::FloatRect{x, y, Settings::POWERUP_WIDTH, Settings::POWERUP_HEIGHT};
}

bool PowerUp::collides(const sf::FloatRect& rect) noexcept
{
    if (get_collision_rect().intersects(rect))
    {
        set_reachable(false);
        return true;
    }
    return false;
}

void PowerUp::update(float dt) noexcept
{
    if (reachable)
    {
        R = 127 + (R + 2) % 128;
        G = 127 + (G + 4) % 128;
        B = 127 + (B + 8) % 128;
        R = (R + 2) % 255;
        G = (G + 4) % 255;
        B = (B + 8) % 255;
        sprite.setColor(sf::Color(R, G, B));
    }
    else{
        sprite.setColor(sf::Color::White);
    }
    x += -Settings::MAIN_SCROLL_SPEED * dt;

    sprite.setPosition(x, y);
}

void PowerUp::render(sf::RenderTarget& target) const noexcept
{
    if (reachable)
        target.draw(sprite);
}

bool PowerUp::is_out_of_game() noexcept
{
    if ( x < -Settings::POWERUP_WIDTH )
    {
        set_reachable(false);
        return true;
    }
    return false;
}

void PowerUp::set_reachable(bool _reachable) noexcept
{
    reachable = _reachable;
}

bool PowerUp::is_reachable() noexcept
{
    return reachable;
}

void PowerUp::reset(float _x, float _y) noexcept
{
    x = _x;
    y = _y;
    reachable = true;
}