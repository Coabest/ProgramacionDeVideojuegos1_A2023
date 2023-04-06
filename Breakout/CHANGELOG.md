    Created a class for each new powerup
        Added:
            - StickyPaddle.py
            - Laser.py
            - Shield.py

    Ball.py
        - Added:
            - stuck, to know if the ball is glued to the paddle or not
            - stick(), sets the Y position just above the paddle and horizontal speed to 0
            - unstick(), gives a new random horizontal speed to the ball as if serving

        - Modified:
            - update(), now checks if the ball is glued to update vertical position

    PlayState.py
        - Added:
            - sticky, allows the next ball to hit the paddle to stick to it
            - ballStuck, checks wether a ball is already glued to the paddle

        - Modified:
            - update()
                - ball-paddle collision checks if paddle is sticky
                - TwoMoreBall powerup chance changed to 4%
                - Added StickyPaddle powerup with 4% chance

            - on_input()
                - horizontal arrows now also move glued balls
                - pressing 'enter' when balls are glued, serves them