    Created a class for each new powerup
        Added:
            - StickyPaddle.py
            - Laser.py
            - Shield.py

    Created "LaserBall" class
    Created "LaserBalls" class which works as a container for the laserBall pair

    Ball.py
        - Added:
            - stuck, to know if the ball is glued to the paddle or not
            - stick(), glues the ball on top of the paddle where the collided
            - unstick(), simulates ball serve

        - Modified:
            - update()
                - now checks if the ball is glued to update vertical position
                - tracks the ball-paddle horizontal relative distance

    Paddle.py
        - Added:
            - sticky, allows the next ball to hit the paddle to stick to it
            - ballStuck, checks wether a ball is already glued to the paddle
            - laserBalls, works a container for the two lasers
            - loaded, checks if the lasers are ready to be fired
            - addLasers(), creates a laserBalls object
            - fire(), begins the movement of the lasers

        - Modified:
            - update()
                - now also handles the lasers behaviour when loaded and fired

    PlayState.py
        - Added:
            - powerup_chance, probability to drop Power-up when breaking a brick

        - Modified:
            - update()
                - Added Laser-Brick collision behaviour
                - Added Ball-Paddle collision checking for stickyPaddle behavior
                - ~~TwoMoreBall powerup chance changed to 4%~~
                - ~~Added StickyPaddle powerup with 4% chance~~
                - **powerup_chance** evenly divided between available Power-ups
                    - taken Power-ups have 0% drop probability until used
                

            - on_input()
                - Horizontal arrows now also move glued balls
                - Pressing 'enter' when balls are glued, serves them
                - Pressing 'down-arrow' when lasers are loaded, fires them

    settings.py
        - Added:
            - lasers frames
            - shields frames

    frames.py
        - Added:
            - generate_laser_frames()
            - generate_shield_frames()