# Proyecto 1: Simulador de Enjambre de Asteroides (Programación Funcional y Paralelismo)

Simulador 2D interactivo en Python que demuestra optimización medible mediante paralelismo real (`multiprocessing`) respetando principios de inmutabilidad y funciones puras.

## Integrantes y Contribuciones
- **David Guale** (`feature/core-physics`): Diseño de estructuras de datos inmutables (`Asteroid`, `Ship`, `GameState`) en `src/models.py`, funciones puras de física y detección de colisiones en `src/physics.py`, y pruebas unitarias de pureza e inmutabilidad en `tests/test_physics.py`.
- **Derek Baque** (`feature/parallel-engine`): Estrategia de partición equilibrada de tuplas (`partition_tuple`) y tareas de workers en `src/parallel.py`, además del motor de simulación secuencial/paralelo con `multiprocessing.Pool` en `src/engine.py`.
- **Leonardo Valdivieso** (`feature/pygame-renderer`): Renderizado 2D del estado congelado y panel HUD de métricas en `src/renderer.py`, junto al Game Loop principal y controles de estrés (1k, 3k y 5k entidades) en `src/main.py`.

---

## Requisitos e Instalación

### 1. Descarga y Gestión del Repositorio (Comandos Git)
- **Clonar el repositorio por primera vez y entrar a la raíz del proyecto:**
  ```bash
  git clone [https://github.com/daviduale04/Proyecto-1---Enjambre.git](https://github.com/daviduale04/Proyecto-1---Enjambre.git)
  cd Proyecto-1---Enjambre
  ```
- **Descargar los últimos cambios subidos a `main`:**
  ```bash
  git checkout main
  git pull origin main
  ```
- **Crear una rama nueva para trabajar sin alterar `main`:**
  ```bash
  git checkout -b feature/nombre-rama
  ```
- **Sincronizar una rama de trabajo con lo último de `main`:**
  ```bash
  git fetch origin
  git merge origin/main
  ```
- **Sobrescribir copia local para dejarla idéntica al remoto (en caso de conflictos):**
  ```bash
  git fetch origin
  git checkout main
  git reset --hard origin/main
  git clean -fd
  ```

### 2. Comandos de Ejecución
- **Instalar dependencias (`pygame` y `pytest`):**
  ```bash
  pip install -r requirements.txt
  ```
- **Ejecutar el simulador:**
  ```bash
  python -m src.main
  ```
- **Ejecutar pruebas unitarias:**
  ```bash
  python -m pytest
  ```

---

## Controles en Tiempo Real
- **`W / A / S / D` o `Flechas`:** Mover la nave evasora.
- **`P`:** Alternar en vivo entre **Modo Paralelo (`N` núcleos)** y **Modo Secuencial (`1` núcleo)**.
- **`1` / `3` / `5`:** Reiniciar simulación con **1,000**, **3,000** o **5,000** asteroides.
