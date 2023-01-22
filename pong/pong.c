/*
    ISPPJ1 2023
    Study Case: Pong

    Authors:
    Alejandro Mujica - alejandro.j.mujic4@gmail.com
    COalbert Ramirez - coabest15@gmail.com

    This file contains the definition of the functions to init a pong game,
    update it, and render it.
*/

#include <stdio.h>

#include <allegro5/allegro_primitives.h>

#include "settings.h"
#include "pong.h"

void init_pong(struct Pong* pong, struct Sounds* sounds)
{
    init_paddle(&pong->player1, PADDLE_X_OFFSET, PADDLE_Y_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT);
    init_paddle(&pong->player2, TABLE_WIDTH - PADDLE_WIDTH - PADDLE_X_OFFSET, TABLE_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT);
    init_ball(&pong->ball, TABLE_WIDTH / 2 - BALL_SIZE / 2, TABLE_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE);
    pong->state = START;
    pong->player1_score = 0;
    pong->player2_score = 0;
    pong->serving_player = 0;
    pong->winning_player = 0;
    pong->sounds = sounds;
    srand(time(NULL));
}

void handle_input_pong(struct Pong* pong, ALLEGRO_KEYBOARD_STATE* state)
{
    if (pong->state == START)
    {
        if (al_key_down(state, ALLEGRO_KEY_ENTER))
        {
            pong->state = SERVE;
            pong->serving_player = rand() % 2 + 1;
        }
    }
    else if (pong->state == SERVE)
    {
        if (al_key_down(state, ALLEGRO_KEY_ENTER))
        {
            pong->state = PLAY;

            pong->ball.vx = rand() % 60 + 160;

            if (pong->serving_player == 2)
            {
                pong->ball.vx *= -1;
            }

            pong->ball.vy = rand() % 100 - 50;
        }
    }
    else if (pong->state == PLAY)
    {
        // 
    }
    else
    {
        if (al_key_down(state, ALLEGRO_KEY_ENTER))
        {
            pong->state = SERVE;
            init_ball(&pong->ball, TABLE_WIDTH / 2 - BALL_SIZE / 2, TABLE_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE);

            pong->player1_score = 0;
            pong->player2_score = 0;

            if (pong->winning_player == 1)
            {
                pong->serving_player = 2;
            }
            else
            {
                pong->serving_player = 1;
            }
        }
    }
}

void update_pong(struct Pong* pong, double dt)
{
    if (pong->state == PLAY)
    {
        
        // Paddles AI
        int p1_AI_difficulty = 9;
        int p2_AI_difficulty = 10;
        float p1_center = pong->player1.y + (PADDLE_HEIGHT / 2);
        float p2_center = pong->player2.y + (PADDLE_HEIGHT / 2);
        float ball_center = pong->ball.y + (BALL_SIZE / 2);

        // AI for Paddle 1
        if (p1_center == ball_center || pong->ball.vx > 0)
        {
            pong->player1.vy = 0;
        }
        else
        {
            pong->player1.vy = PADDLE_SPEED * (p1_center < ball_center? 1: -1);
        }
        if (rand()%10 > p1_AI_difficulty)
        {
            pong->player1.vy *= -1;
        }

        // AI for Paddle 2
        if (pong->ball.vx < 0)
        {
            pong->player2.vy = PADDLE_SPEED * (p2_center < TABLE_HEIGHT / 2? 1: -1) / 2;
        }
        else
        {
            if (p2_center == ball_center)
            {
                    pong->player2.vy = 0;
            }
            else
            {
                pong->player2.vy = PADDLE_SPEED * (p2_center < ball_center? 1: -1);
            }
            if (rand()%10 > p2_AI_difficulty)
            {
                pong->player1.vy *= -1;
            }
        }
        
        

        update_paddle(&pong->player1, dt);
        update_paddle(&pong->player2, dt);
        update_ball(&pong->ball, dt);

        struct Hitbox ball_hitbox;
        build_ball_hitbox(pong->ball, &ball_hitbox);

        struct Hitbox player1_hitbox;
        build_paddle_hitbox(pong->player1, &player1_hitbox);

        struct Hitbox player2_hitbox;
        build_paddle_hitbox(pong->player2, &player2_hitbox);

        if (ball_hitbox.x1 > TABLE_WIDTH)
        {
            al_play_sample(pong->sounds->score, /* gain */ 1.0, /* center */ 1.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            ++pong->player1_score;
            pong->serving_player = 2;

            if (pong->player1_score == MAX_POINTS)
            {
                pong->winning_player = 1;
                pong->state = DONE;
            }
            else
            {
                pong->state = SERVE;
                init_ball(&pong->ball, TABLE_WIDTH / 2 - BALL_SIZE / 2, TABLE_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE);
            }
        }
        else if (ball_hitbox.x2 < 0)
        {
            al_play_sample(pong->sounds->score, /* gain */ 1.0, /* center */ -1.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            ++pong->player2_score;
            pong->serving_player = 1;

            if (pong->player2_score == MAX_POINTS)
            {
                pong->winning_player = 2;
                pong->state = DONE;
            }
            else
            {
                pong->state = SERVE;
                init_ball(&pong->ball, TABLE_WIDTH / 2 - BALL_SIZE / 2, TABLE_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE);
            }
        }

        if (ball_hitbox.y1 <= 0)
        {
            al_play_sample(pong->sounds->wall_hit, /* gain */ 1.0, /* center */ 0.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            pong->ball.y = 0;
            pong->ball.vy *= -1;
        }
        else if (ball_hitbox.y2 >= TABLE_HEIGHT)
        {
            al_play_sample(pong->sounds->wall_hit, /* gain */ 1.0, /* center */ 0.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            pong->ball.y = TABLE_HEIGHT - pong->ball.height;
            pong->ball.vy *= -1;
        }
        
        if (collides(ball_hitbox, player1_hitbox))
        {
            al_play_sample(pong->sounds->paddle_hit, /* gain */ 1.0, /* center */ -1.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            pong->ball.x = player1_hitbox.x2;
            pong->ball.vx *= -1.05;

            if (pong->ball.vy < 0)
            {
                pong->ball.vy = -(rand() % 150 + 10);
            }
            else
            {
                pong->ball.vy = rand() % 150 + 10;
            }
        }
        else if (collides(ball_hitbox, player2_hitbox))
        {
            al_play_sample(pong->sounds->paddle_hit, /* gain */ 1.0, /* center */ 1.0, /* speed */ 1.0, ALLEGRO_PLAYMODE_ONCE, NULL);
            pong->ball.x = player2_hitbox.x1 - pong->ball.width;
            pong->ball.vx *= -1.05;

            if (pong->ball.vy < 0)
            {
                pong->ball.vy = -(rand() % 150 + 10);
            }
            else
            {
                pong->ball.vy = rand() % 150 + 10;
            }
        }
    }
}

void render_pong(struct Pong pong)
{
    al_draw_filled_rectangle(
        TABLE_WIDTH / 2 - MID_LINE_WIDTH / 2, 0,
        TABLE_WIDTH / 2 + MID_LINE_WIDTH / 2, TABLE_HEIGHT,
        al_map_rgb(127, 64, 127)
    );
    
    for (int i = 0; i < pong.player1_score; ++i)
    {
        al_draw_filled_circle(
            TABLE_WIDTH / 2 - 10 - 8*i, 10, 4, al_map_rgb(127, 64 + i*32, 127)
        );
    }

    for (int i = 0; i < pong.player2_score; ++i)
    {
        al_draw_filled_circle(
            TABLE_WIDTH / 2 + 10 + 8*i, 10, 4, al_map_rgb(127, 64 + i*32, 127)
        );
    }

    render_paddle(pong.player1);
    render_paddle(pong.player2);
    render_ball(pong.ball);

}

