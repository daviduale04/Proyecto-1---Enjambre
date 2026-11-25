# Proyecto 1: Simulador de Enjambre de Asteroides (Programación Funcional y Paralelismo)

Simulador 2D interactivo en Python que demuestra optimización medible mediante paralelismo real (`multiprocessing`) respetando principios de inmutabilidad y funciones puras.

## Integrantes y Contribuciones
- **David Guale** (`feature/core-physics`): Estructuras de datos inmutables (`src/models.py`), física pura y detección de colisiones (`src/physics.py`), y pruebas unitarias (`tests/test_physics.py`).
- **Derek Baque** (`feature/parallel-engine`): Partición equilibrada de tuplas y tareas de workers (`src/parallel.py`), y motor de simulación secuencial/paralelo con `multiprocessing.Pool` (`src/engine.py`).
- **Leonardo Valdivieso** (`feature/pygame-renderer`): Renderizado 2D y panel HUD de métricas en Pygame (`src/renderer.py`), y bucle principal con controles de estrés (`src/main.py`).

## Instalación y Ejecución
1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecutar el simulador:**
   ```bash
   python -m src.main
   ```
3. **Ejecutar pruebas unitarias:**
   ```bash
   python -m pytest
   ```

## Controles en Tiempo Real
- **`W / A / S / D` o `Flechas`:** Mover la nave.
- **`P`:** Alternar entre **Modo Paralelo (`N` núcleos)** y **Modo Secuencial (`1` núcleo)**.
- **`1` / `3` / `5`:** Reiniciar con **1,000**, **3,000** o **5,000** asteroides.
