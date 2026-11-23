from dataclasses import dataclass


@dataclass(frozen=True)
class Asteroid:
    id: int
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    mass: float
    colliding: bool = False


@dataclass(frozen=True)
class Ship:
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    shield_hits: int = 0


@dataclass(frozen=True)
class GameState:
    asteroids: tuple[Asteroid, ...]
    ship: Ship
    width: int
    height: int
    frame: int
