from typing import TypeVar
from src.models import Asteroid, Ship
from src.physics import update_asteroid_chunk

T = TypeVar("T")


def partition_tuple(items: tuple[T, ...], num_chunks: int) -> tuple[tuple[T, ...], ...]:
    """
    Divide una tupla inmutable en N sub-tuplas equilibradas sin mutar la original.
    Estrategia de partición: bloques contiguos (chunking) con distribución de residuo.
    """
    total = len(items)
    if num_chunks <= 1 or total == 0:
        return (items,) if total > 0 else ()

    actual_chunks = min(num_chunks, total)
    base_size, remainder = divmod(total, actual_chunks)

    chunks: list[tuple[T, ...]] = []
    start = 0
    for i in range(actual_chunks):
        end = start + base_size + (1 if i < remainder else 0)
        chunks.append(items[start:end])
        start = end

    return tuple(chunks)


def process_worker_task(
    task: tuple[tuple[Asteroid, ...], Ship, tuple[Asteroid, ...], float, int, int]
) -> tuple[Asteroid, ...]:
    """
    Desempaqueta los argumentos inmutables enviados por pool.map
    y ejecuta la transformación pura en el proceso hijo.
    """
    chunk, ship, reference_sample, dt, width, height = task
    return update_asteroid_chunk(chunk, ship, reference_sample, dt, width, height)