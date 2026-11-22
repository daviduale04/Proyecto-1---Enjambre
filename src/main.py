import time
from multiprocessing import Pool, freeze_support
import pygame
from src.physics import create_initial_state
from src.engine import get_system_cores, step_simulation
from src.renderer import render_frame


def run_simulator() -> None:
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Proyecto 1 - Simulador Funcional de Asteroides (Secuencial vs Paralelo)")
    font = pygame.font.SysFont("consolas", 18)

    total_cores = get_system_cores()
    active_workers = total_cores
    parallel_mode = True
    entity_count = 1000

    state = create_initial_state(entity_count, width, height)
    running = True
    last_time = time.perf_counter()
    smooth_fps = 60.0

    # El Pool se crea UNA sola vez fuera del bucle para evitar overhead de creación de procesos
    with Pool(processes=active_workers) as pool:
        while running:
            now = time.perf_counter()
            dt = min(now - last_time, 0.05)  # Limitar dt para estabilidad física
            last_time = now
            instant_fps = (1.0 / dt) if dt > 0 else 0.0
            smooth_fps = smooth_fps * 0.9 + instant_fps * 0.1

            # 1. Lectura de eventos (Entrada impura)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        parallel_mode = not parallel_mode
                    elif event.key == pygame.K_1:
                        entity_count = 1000
                        state = create_initial_state(entity_count, width, height)
                    elif event.key == pygame.K_3:
                        entity_count = 3000
                        state = create_initial_state(entity_count, width, height)
                    elif event.key == pygame.K_5:
                        entity_count = 5000
                        state = create_initial_state(entity_count, width, height)

            keys = pygame.key.get_pressed()
            dx = float(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - float(keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = float(keys[pygame.K_DOWN] or keys[pygame.K_s]) - float(keys[pygame.K_UP] or keys[pygame.K_w])

            # 2. Paso de simulación PURO (devuelve un nuevo GameState congelado)
            state = step_simulation(
                state=state,
                move_dir=(dx, dy),
                dt=dt if dt > 0 else 0.016,
                parallel=parallel_mode,
                pool=pool,
                num_workers=active_workers,
            )

            # 3. Renderizado IMPURO del estado inmutable
            render_frame(
                screen=screen,
                font=font,
                state=state,
                fps=smooth_fps,
                parallel_mode=parallel_mode,
                total_cores=total_cores,
                active_workers=active_workers,
            )

    pygame.quit()


if __name__ == "__main__":
    freeze_support()
    run_simulator()