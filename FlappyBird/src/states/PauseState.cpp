/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Coalbert Ramirez
    coabest15@gmail.com

    This file contains the definition of the class PauseState.
*/

#include <Settings.hpp>
#include <src/text_utilities.hpp>
#include <src/states/StateMachine.hpp>
#include <src/states/PauseState.hpp>

PauseState::PauseState(StateMachine* sm) noexcept
    : BaseState{sm}
{

}

void PauseState::enter(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) noexcept
{
    world = _world;
    bird = _bird;    
}

void PauseState::handle_inputs(const sf::Event& event) noexcept
{
    if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Right)
    {
        state_machine->change_state("playing", world, bird);
    }
    if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left)
    {
        Settings::powerUp_music.stop();
        Settings::music.play();
        state_machine->change_state("title");
    }
}

void PauseState::render(sf::RenderTarget& target) const noexcept
{
    world->render(target);
    bird->render(target);
    render_text(target, 20, 10, "Score: " + std::to_string(bird->get_score()), Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color(255, 127, 0));
    render_text(target, Settings::VIRTUAL_WIDTH / 2, Settings::VIRTUAL_HEIGHT * 3 / 7, "Rightclick to unpause", Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color(255, 127, 0), true);
    render_text(target, Settings::VIRTUAL_WIDTH / 2, Settings::VIRTUAL_HEIGHT * 4 / 7, "Leftclick for title screen", Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color(255, 127, 0), true);
}