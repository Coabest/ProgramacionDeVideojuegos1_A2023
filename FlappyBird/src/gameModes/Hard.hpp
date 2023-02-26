#pragma once

#include <memory>
#include <src/gameModes/GameMode.hpp>

class Hard: public GameMode
{
public:
    Hard(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) noexcept;

    void handle_inputs(const sf::Event& event) noexcept override;

    void update(float dt, bool powerUp_mode) noexcept override;
};