"""
Entidad Task.

Responsabilidad:
- Representar una tarea del Congreso
- Mantener su estado (pendiente / completada)
- Proveer información para minijuegos

La lógica del minijuego NO va aquí.
"""

import pygame

class Task:
    """
    Representa una tarea que el jugador debe completar.
    Cada tarea tiene un minijuego asociado.
    """
    def __init__(self, name, x, y, task_type, difficulty=1):
        self.name = name
        self.x = x
        self.y = y
        self.task_type = task_type
        self.difficulty = difficulty

        self.completed = False
        self.active = False

        # Área de interacción
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)

    def is_near_player(self, player_x, player_y, distance=50):
        dx = self.x - player_x
        dy = self.y - player_y
        dist = (dx**2 + dy**2) ** 0.5
        return dist < distance

    def start(self):
        self.active = True

    def complete(self):
        self.completed = True
        self.active = False

    def cancel(self):
        self.active = False
