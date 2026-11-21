import math
import random
from src.models import Asteroid, Ship, GameState


def create_initial_state(num_asteroids: int, width: int = 1280, height: int = 720) -> GameState:
    """Genera un estado inicial inmutable con una semilla determinista."""
    rng = random.Random(42)
    asteroids = tuple(
        Asteroid(
            id=i,
            x=rng.uniform(0, width),
            y=rng.uniform(0, height),
            vx=rng.uniform(-120.0, 120.0),
            vy=rng.uniform(-120.0, 120.0),
            radius=rng.uniform(2.5, 5.5),
            mass=rng.uniform(1.0, 4.0),
        )
        for i in range(num_asteroids)
    )
    ship = Ship(x=width / 2.0, y=height / 2.0, vx=0.0, vy=0.0, radius=14.0)
    return GameState(asteroids=asteroids, ship=ship, width=width, height=height, frame=0)


def update_single_asteroid(
    asteroid: Asteroid,
    ship: Ship,
    reference_sample: tuple[Asteroid, ...],
    dt: float,
    width: int,
    height: int,
) -> Asteroid:
    """
    Función pura: calcula la nueva posición, perturbación orbital y colisiones
    de un solo asteroide sin mutar el original.
    """
    dx_ship = ship.x - asteroid.x
    dy_ship = ship.y - asteroid.y
    dist_ship_sq = dx_ship * dx_ship + dy_ship * dy_ship + 100.0
    inv_dist = 1.0 / math.sqrt(dist_ship_sq)

    ax = dx_ship * inv_dist * 18.0
    ay = dy_ship * inv_dist * 18.0

    new_vx = (asteroid.vx + ax * dt) * 0.999
    new_vy = (asteroid.vy + ay * dt) * 0.999
    new_x = (asteroid.x + new_vx * dt) % width
    new_y = (asteroid.y + new_vy * dt) % height

    hit_ship = (new_x - ship.x) ** 2 + (new_y - ship.y) ** 2 <= (asteroid.radius + ship.radius) ** 2

    hit_neighbor = any(
        other.id != asteroid.id
        and (new_x - other.x) ** 2 + (new_y - other.y) ** 2 <= (asteroid.radius + other.radius) ** 2
        for other in reference_sample
    )

    return Asteroid(
        id=asteroid.id,
        x=new_x,
        y=new_y,
        vx=new_vx,
        vy=new_vy,
        radius=asteroid.radius,
        mass=asteroid.mass,
        colliding=(hit_ship or hit_neighbor),
    )


def update_asteroid_chunk(
    chunk: tuple[Asteroid, ...],
    ship: Ship,
    reference_sample: tuple[Asteroid, ...],
    dt: float,
    width: int,
    height: int,
) -> tuple[Asteroid, ...]:
    """
    Transformación pura de un segmento de asteroides.
    Función ejecutada por cada proceso worker en paralelo.
    """
    return tuple(
        update_single_asteroid(ast, ship, reference_sample, dt, width, height)
        for ast in chunk
    )


def update_ship(
    ship: Ship,
    move_dir: tuple[float, float],
    asteroids: tuple[Asteroid, ...],
    dt: float,
    width: int,
    height: int,
) -> Ship:
    """Calcula de forma pura la nueva posición de la nave y conteo de impactos."""
    speed = 320.0
    dx, dy = move_dir
    norm = math.hypot(dx, dy)
    vx = (dx / norm * speed) if norm > 0 else 0.0
    vy = (dy / norm * speed) if norm > 0 else 0.0

    new_x = max(ship.radius, min(width - ship.radius, ship.x + vx * dt))
    new_y = max(ship.radius, min(height - ship.radius, ship.y + vy * dt))

    new_hits = sum(
        1
        for ast in asteroids
        if (ast.x - new_x) ** 2 + (ast.y - new_y) ** 2 <= (ast.radius + ship.radius) ** 2
    )

    return Ship(
        x=new_x,
        y=new_y,
        vx=vx,
        vy=vy,
        radius=ship.radius,
        shield_hits=ship.shield_hits + new_hits,
    )
