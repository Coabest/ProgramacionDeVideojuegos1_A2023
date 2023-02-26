#pragma once

#include <SFML/Graphics.hpp>

class PowerUp
{
public:
    PowerUp(float _x, float _y) noexcept;

    sf::FloatRect get_collision_rect() const noexcept;

    bool collides(const sf::FloatRect& rect) noexcept;

    void update(float dt) noexcept;

    void render(sf::RenderTarget& target) const noexcept;

    bool is_out_of_game() noexcept;

    void set_reachable(bool _is_reachable) noexcept;

    bool is_reachable() noexcept;

    void reset(float _x, float _y) noexcept;

private:
    int R, G, B;
    float x;
    float y;
    bool reachable;
    sf::Sprite sprite;
};