import pygame
from src.models import GameState


def render_frame(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    fps: float,
    parallel_mode: bool,
    total_cores: int,
    active_workers: int,
) -> None:
    """
    Capa impura de salida (I/O): dibuja el estado inmutable actual y el HUD técnico
    en la superficie de Pygame sin alterar los datos.
    """
    screen.fill((12, 14, 24))

    for ast in state.asteroids:
        color = (235, 75, 75) if ast.colliding else (140, 175, 220)
        pygame.draw.circle(screen, color, (int(ast.x), int(ast.y)), int(ast.radius))

    ship_pos = (int(state.ship.x), int(state.ship.y))
    pygame.draw.circle(screen, (70, 220, 140), ship_pos, int(state.ship.radius))
    pygame.draw.circle(screen, (200, 255, 220), ship_pos, int(state.ship.radius), 2)

    mode_label = f"PARALELO ({active_workers} workers)" if parallel_mode else "SECUENCIAL (1 núcleo)"
    mode_color = (80, 250, 150) if parallel_mode else (255, 190, 70)

    hud_lines = [
        (f"Modo: {mode_label}", mode_color),
        (f"FPS en tiempo real: {fps:.1f}", (255, 255, 255)),
        (f"Entidades activas: {len(state.asteroids):,}", (200, 220, 255)),
        (f"Núcleos lógicos detectados: {total_cores}", (180, 190, 210)),
        (f"Impactos de escudo: {state.ship.shield_hits}", (255, 130, 130)),
        ("Controles: [WASD/Flechas] Mover | [P] Secuencial/Paralelo | [1] 1k | [3] 3k | [5] 5k", (150, 160, 180)),
    ]

    for idx, (text, color) in enumerate(hud_lines):
        surface = font.render(text, True, color)
        screen.blit(surface, (16, 14 + idx * 24))

    pygame.display.flip()
