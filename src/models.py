from typing import NamedTuple


class Asteroid(NamedTuple):
    id: int
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    mass: float
    colliding: bool = False


class Ship(NamedTuple):
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    shield_hits: int = 0


class GameState(NamedTuple):
    asteroids: tuple[Asteroid, ...]
    ship: Ship
    width: int
    height: int
    frame: int
