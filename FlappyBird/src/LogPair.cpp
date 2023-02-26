/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class LogPair.
*/
#include <iostream>
#include <Settings.hpp>
#include <src/LogPair.hpp>

LogPair::LogPair(float _x, float _y) noexcept
    : x{_x}, y{_y},
      top{x, y + Settings::LOG_HEIGHT, true},
      bottom{x, y + Settings::LOGS_GAP + Settings::LOG_HEIGHT, false},
      converging_logs{false}
{

}

bool LogPair::collides(const sf::FloatRect& rect) const noexcept
{
    return top.get_collision_rect().intersects(rect) || bottom.get_collision_rect().intersects(rect);
}

void LogPair::update(float dt) noexcept
{
    x += -Settings::MAIN_SCROLL_SPEED * dt;
    
    if (converging_logs)
    {
        float dy = Settings::LOGS_VERTICAL_SPEED * dt;
        if (is_converging)
        {
            top.update(x, dy);
            bottom.update(x, -dy);
        }
        else
        {
            top.update(x, -dy);
            bottom.update(x, dy);
        }
        if ( bottom.get_collision_rect().top - Settings::LOGS_GAP + 1.f >=
            top.get_collision_rect().top + Settings::LOG_HEIGHT)
        {
            is_converging = true;
        }
        if ( top.get_collision_rect().top + Settings::LOG_HEIGHT + 1.f >=
             bottom.get_collision_rect().top)
        {
            Settings::sounds["thump"].play();
            is_converging = false;
        }
    }
    else
    {
        top.update(x);
        bottom.update(x);
    }
}

void LogPair::render(sf::RenderTarget& target) const noexcept
{
    top.render(target);
    bottom.render(target);
}

bool LogPair::is_out_of_game() const noexcept
{
    return x < -Settings::LOG_WIDTH;
}

bool LogPair::update_scored(const sf::FloatRect& rect) noexcept
{
    if (scored)
    {
        return false;
    }

    if (rect.left > x + Settings::LOG_WIDTH)
    {
        scored = true;
        return true;
    }

    return false;
}

void LogPair::reset(float _x, float _y) noexcept
{
    x = _x;
    y = _y;
    scored = false;
}

void LogPair::make_logs_converge() noexcept
{
    converging_logs = true;
}