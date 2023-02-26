/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class World.
*/

#include <ctime>
#include <iostream>
#include <Settings.hpp>
#include <src/World.hpp>
using namespace std;

World::World(bool _generate_logs) noexcept
    : generate_logs{_generate_logs},
      background{Settings::textures["background"]},
      ground{Settings::textures["ground"]},
      logs{},
      
      rng{std::default_random_engine{}()}
{
    srand(time(0));
    ground.setPosition(0, Settings::VIRTUAL_HEIGHT - Settings::GROUND_HEIGHT);
    std::uniform_int_distribution<int> dist(0, 80);
    last_log_y = -Settings::LOG_HEIGHT + dist(rng) + 20;
    powerUp_mode = false;
}

void World::reset(bool _generate_logs) noexcept
{
    generate_logs = _generate_logs;
    generate_powerup = true;
    powerUp_mode = false;
    Settings::music.setLoop(true);
    Settings::music.play();
}

bool World::collides(const sf::FloatRect& rect) const noexcept
{
    if (rect.top + rect.height >= Settings::VIRTUAL_HEIGHT)
    {
        Settings::powerUp_music.stop();
        return true;
    }
    if (!powerUp_mode)
    {
        
        for (auto log_pair: logs)
        {
            if (log_pair->collides(rect))
            {
                return true;
            }
        }
    }
    return false;
}

bool World::powerUp_pickup(const sf::FloatRect& rect) noexcept
{
    for (auto power_up: powerUp)
    {
        if (!is_in_powerUp() && power_up->collides(rect))
        {
            powerUp_mode = true;
            Settings::music.setLoop(true);
            Settings::music.stop();
            Settings::powerUp_music.play();
            return true;
        }
    }

    return false;
}

bool World::is_in_powerUp()
{
    return powerUp_mode;
}

bool World::update_scored(const sf::FloatRect& rect) noexcept
{
    for (auto log_pair: logs)
    {
        if (log_pair->update_scored(rect))
        {
            return true;
        }
    }

    return false;
}

void World::update(float dt) noexcept
{
    if (generate_logs)
    {
        logs_spawn_timer += dt;

        if (logs_spawn_timer >= Settings::TIME_TO_SPAWN_LOGS)
        {
            logs_spawn_timer = 0.f;

            std::uniform_int_distribution<int> dist{-40, 40};
            float y = std::max(-Settings::LOG_HEIGHT + 10,
                        std::min(last_log_y + dist(rng),
                                  Settings::VIRTUAL_HEIGHT + 90 - Settings::LOG_HEIGHT));

            last_log_y = y;

            logs.push_back(log_factory.create(Settings::VIRTUAL_WIDTH, y));

        }
    }

    background_x += -Settings::BACK_SCROLL_SPEED * dt;

    if (background_x <= -Settings::BACKGROUND_LOOPING_POINT)
    {
        background_x = 0;
    }

    background.setPosition(background_x, 0);

    ground_x += -Settings::MAIN_SCROLL_SPEED * dt;

    if (ground_x <= -Settings::VIRTUAL_WIDTH)
    {
        ground_x = 0;
    }

    ground.setPosition(ground_x, Settings::VIRTUAL_HEIGHT - Settings::GROUND_HEIGHT);

    for (auto it = logs.begin(); it != logs.end(); )
    {
        if ((*it)->is_out_of_game())
        {
            auto log_pair = *it;
            log_factory.remove(log_pair);
            it = logs.erase(it);
            
        }
        else
        {
            (*it)->update(dt);
            ++it;
        }
    }
}

void World::update_hardmode(float dt) noexcept
{

    if (generate_logs)
    {
        
        logs_spawn_timer += dt;

        if (logs_spawn_timer >= Settings::TIME_TO_SPAWN_LOGS)
        {
            logs_spawn_timer = 0.f;

            std::uniform_int_distribution<int> dist{-80, 80};
            float y = std::max(-Settings::LOG_HEIGHT + 10, 
                                std::min(last_log_y + dist(rng), 
                                          Settings::VIRTUAL_HEIGHT + 90 - Settings::LOG_HEIGHT));

            last_log_y = y;

            logs.push_back(log_factory.create(Settings::VIRTUAL_WIDTH, y));

            if (rand()%3 == 0)
            {
                logs.back()->make_logs_converge();
            }
        }
    }

    if (generate_powerup)
    {
        powerUp_spawn_timer += dt;
        if (powerUp_spawn_timer >= Settings::TIME_TO_SPAWN_POWERUP)
        {
            powerUp_spawn_timer = 0.f;
            
            int range = Settings::POWERUP_HEIGHT * 4;
            float y = Settings::VIRTUAL_HEIGHT / 2
                        - Settings::POWERUP_HEIGHT * 2
                        + rand()%range;

            powerUp.push_back(powerUp_factory.create(Settings::VIRTUAL_WIDTH, y));
            for (auto power_up: powerUp)
            {
                power_up->set_reachable(true);
            }
        }
    }

    if (powerUp_mode)
    {   
        for (auto power_up: powerUp)
        {
            power_up->set_reachable(false);
        }
        powerUp_duration_timer += dt;
        if (powerUp_duration_timer >= Settings::POWERUP_TIME_DURATION)
        {
            powerUp_duration_timer = 0.f;
            powerUp_mode = false;
            Settings::powerUp_music.setLoop(true);
            Settings::powerUp_music.stop();
            Settings::music.play();
        }
    }

    background_x += -Settings::BACK_SCROLL_SPEED * 1.2f * dt;

    if (background_x <= -Settings::BACKGROUND_LOOPING_POINT)
    {
        background_x = 0;
    }

    background.setPosition(background_x, 0);

    ground_x += -Settings::MAIN_SCROLL_SPEED * 1.2f * dt;

    if (ground_x <= -Settings::VIRTUAL_WIDTH)
    {
        ground_x = 0;
    }

    ground.setPosition(ground_x, Settings::VIRTUAL_HEIGHT - Settings::GROUND_HEIGHT);

    for (auto it = logs.begin(); it != logs.end(); )
    {
        if ((*it)->is_out_of_game())
        {
            auto log_pair = *it;
            log_factory.remove(log_pair);
            it = logs.erase(it);
        }
        else
        {
            (*it)->update(dt);
            ++it;
        }
    }
    for (auto it = powerUp.begin(); it != powerUp.end(); )
    {
        if ((*it)->is_out_of_game())
        {
            auto power_up = *it;
            powerUp_factory.remove(power_up);
            it = powerUp.erase(it);
        }
        else
        {
            (*it)->update(dt);
            ++it;
        }
    }
}

void World::render(sf::RenderTarget& target) const noexcept
{   
    target.draw(background);

    for (const auto& power_up: powerUp)
    {
        if (power_up->is_reachable())
            power_up->render(target);
    }

    for (const auto& log_pair: logs)
    {
        log_pair->render(target);
    }

    target.draw(ground);
}