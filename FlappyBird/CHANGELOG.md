Added GameMode.hpp for the normal and hard mode management

Added Hard class that manages the hardmode controls (sideways movement) and
world->update_hardmode() method

Added Normal class that manages the normal mode gameplay and the 
world->update() method

Added PauseState to pause the game and also go back to the title screen

PlayingState:
    Added:
        - the handle_inputs() checks input to pause the game
        - gameMode object handles the game mode

    Modified:
        - update() now checks if there is a powerUp pickup to play the sound
        - update() now has a call to gameMode->update()

TitleScreenState:
    Modified:
        - handle_inputs() now checks for input to determine the game mode
        - render, shows the game mode options

Bird:
    Added:
        - move_left() and move_right() to control sideways movement in hard mode
        - R, G and B, for sprite color manipulation

    Modified:
        - RGB sprite manipulation when picking a powerUp
        - x and y boundaries checked to avoid going outside the game screen

Log:
    modified:
        - Update method now takes an optional parameter for vertical movement

LogPair:
    Added:
        - make_logs_converge() method
        - converging_logs, to indicate the pair is dynamic
        - is_converging, to indicate if they are getting closer or apart

    Modified:
        - update, now handles dynamic logs

Added the powerUp class, to create powerUp objects in the hard mode gameplay
        
World:
    added:
        - powerUp_pickup(), checks if the bird collides with a powerUp
        - is_in_powerUp(), returns wether the game is in powerUp mode or not
        - update_hardmode(), controls the world behaviour in hardmode
        - powerUp_mode, is active when a powerUp has ben picked up
        - generate_powerup
        - powerUp_factory
        - powerUp, 
        - powerUp_spawn_timer, time passed since last powerUp
        - powerUp_duration_timer,time passed since last powerUp pickup
    Modified:
        - collides(), now checks if the game is in powerUp mode first
        - render() also renders the powerUp if not pickedUp

Makefile:
    added:
        - Inclusion of the gamemodes and powerUp class to the compiler
        - GDB debug support

Settings:
    Added:
        - HORIZONTAL_SPEED for the bird when playing in hardmode
        - LOGS_VERTICAL_SPEED for the converging logs
        - POWERUP_WIDTH
        - POWERUP_HEIGHT
        - TIME_TO_SPAWN_POWERUP
        - POWERUP_TIME_DURATION
        - powerUp_music for powerUp mode
        - Included converging logs thump and powerUp pickup sounds

    modified:
        - reduced GRAVITY by almost 40%
        - increased JUMP_TAKEOFF_SPEED
        - increased a bit the TIME_TO_SPAWN_LOGS value