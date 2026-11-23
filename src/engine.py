import os
from multiprocessing.pool import Pool
from src.models import Asteroid, GameState
from src.physics import update_asteroid_chunk, update_ship
from src.parallel import partition_tuple, process_worker_task


def get_system_cores() -> int:
    """Detecta los núcleos lógicos disponibles en la CPU."""
    return os.cpu_count() or 2


def step_simulation(
    state: GameState,
    move_dir: tuple[float, float],
    dt: float,
    parallel: bool,
    pool: Pool | None,
    num_workers: int,
) -> GameState:
    """
    Ejecuta un frame completo de forma pura:
    1. Segmentación de entidades.
    2. Procesamiento Secuencial (1 núcleo) o Mapeo Paralelo (N workers).
    3. Sincronización y consolidación en un nuevo GameState inmutable.
    """
    reference_sample: tuple[Asteroid, ...] = state.asteroids[:60]

    if parallel and pool is not None and num_workers > 1:
        chunks = partition_tuple(state.asteroids, num_workers)
        tasks = tuple(
            (chunk, state.ship, reference_sample, dt, state.width, state.height)
            for chunk in chunks
        )
        processed_chunks = pool.map(process_worker_task, tasks)
        new_asteroids = tuple(ast for chunk in processed_chunks for ast in chunk)
    else:
        new_asteroids = update_asteroid_chunk(
            chunk=state.asteroids,
            ship=state.ship,
            reference_sample=reference_sample,
            dt=dt,
            width=state.width,
            height=state.height,
        )

    new_ship = update_ship(
        ship=state.ship,
        move_dir=move_dir,
        asteroids=new_asteroids,
        dt=dt,
        width=state.width,
        height=state.height,
    )

    return GameState(
        asteroids=new_asteroids,
        ship=new_ship,
        width=state.width,
        height=state.height,
        frame=state.frame + 1,
    )
