/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class PlayingBaseState.
*/
#include <iostream>
#include <Settings.hpp>
#include <src/text_utilities.hpp>
#include <src/states/StateMachine.hpp>
#include <src/states/PlayingState.hpp>
#include <src/gameModes/GameMode.hpp>

PlayingState::PlayingState(StateMachine* sm) noexcept
    : BaseState{sm}, gameMode{nullptr}
{

}

void PlayingState::enter(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) noexcept
{
    std::cout << "Entered playing state with gameMode: " << (state_machine->is_hardmode()? "Hard ": "Normal ") << state_machine->is_hardmode() << " \n";        
    world = _world;
    world->reset(true);
    
    if (_bird == nullptr)
    {
        bird = std::make_shared<Bird>(
            Settings::VIRTUAL_WIDTH / 2 - Settings::BIRD_WIDTH / 2, Settings::VIRTUAL_HEIGHT / 2 - Settings::BIRD_HEIGHT / 2,
            Settings::BIRD_WIDTH, Settings::BIRD_HEIGHT
        );
    }
    else
    {
        bird = _bird;
    }

    if (gameMode == nullptr)
    {
        bool mode = state_machine->is_hardmode();
        if (mode)
        {
            // gameMode = std::make_shared<Hard>(bird, world);
        }
        else
        {
            std::cout << "creating normal gameMode\n";
            gameMode = std::make_shared<Normal>(world, bird);
            std::cout << "created normal gameMode\n";
        }
        

    }
}

void PlayingState::handle_inputs(const sf::Event& event) noexcept
{
    // if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left)
    // {
    //     bird->jump();
    // }

    gameMode->handle_inputs(event);

    if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Right)
    {
        std::cout << "Game paused\n";
        state_machine->change_state("pause", world, bird);
    }
}

void PlayingState::update(float dt) noexcept
{
    gameMode->update(dt);

    if (world->collides(bird->get_collision_rect()))
    {
        Settings::sounds["explosion"].play();
        Settings::sounds["hurt"].play();
        state_machine->change_state("count_down");
        return;
    }
    
    if (world->update_scored(bird->get_collision_rect()))
    {
        bird->up_score();
        Settings::sounds["score"].play();
    }
}

void PlayingState::render(sf::RenderTarget& target) const noexcept
{
    world->render(target);
    bird->render(target);
    render_text(target, 20, 10, "Score: " + std::to_string(bird->get_score()), Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color::White);
}