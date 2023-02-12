#include <iostream>
#include <src/gameModes/Normal.hpp>

Normal::Normal(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) noexcept
    :  GameMode(_world, _bird)
{

}

void Normal::handle_inputs(const sf::Event& event) noexcept
{
    if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left)
    {
        std::cout << "Jump detected!\n";
        bird->jump();
    }
}

void Normal::update(float dt) noexcept
{
    bird->update(dt);
    world->update(dt);
}