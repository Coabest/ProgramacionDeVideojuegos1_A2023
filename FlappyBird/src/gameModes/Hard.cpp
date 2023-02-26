#include <iostream>
#include <src/gameModes/Hard.hpp>

Hard::Hard(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) noexcept
    :  GameMode(_world, _bird)
{

}

void Hard::handle_inputs(const sf::Event& event) noexcept
{
    if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Space ||
        event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left)
    {
        bird->jump();
    }
    if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::A ||
        event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Left)
    {
        bird->move_left();
    }
    else if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::D ||
             event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Right)
    {
        bird->move_right();
    }
}

void Hard::update(float dt, bool powerUp_mode) noexcept
{
    bird->update(dt, powerUp_mode);
    world->update_hardmode(dt);
}