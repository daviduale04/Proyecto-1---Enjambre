import pytest
from src.physics import create_initial_state, update_asteroid_chunk, update_ship


def test_immutability_and_purity():
    state = create_initial_state(50)
    original_snapshot = state.asteroids

    updated_chunk = update_asteroid_chunk(
        chunk=state.asteroids,
        ship=state.ship,
        reference_sample=state.asteroids[:10],
        dt=0.016,
        width=state.width,
        height=state.height,
    )

    assert state.asteroids == original_snapshot
    assert updated_chunk != original_snapshot

    with pytest.raises(AttributeError):
        state.asteroids[0].x = 999.0  # type: ignore


def test_ship_movement_purity():
    state = create_initial_state(10)
    new_ship = update_ship(state.ship, (1.0, 0.0), state.asteroids, 0.1, state.width, state.height)

    assert state.ship.x == 640.0
    assert new_ship.x == pytest.approx(672.0)
