"""
Entidad Player (jugador).

Responsabilidad:
- Representar al jugador humano
- Guardar su rol (Ciudadano o Impostor)
- Posición, movimiento y estado
- Progreso de tareas
"""
import random
import pygame


class Player:
    """Representa al jugador humano"""

    def __init__(self):
        # Posición inicial (centro del mapa)
        self.x = 600
        self.y = 400

        # Movimiento
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0

        # Rol del jugador (70% Diputado, 30% Impostor)
        self.role = "Diputado" if random.random() < 0.7 else "Impostor"
        self.is_impostor = (self.role == "Impostor")

        # Progreso de tareas
        self.tasks_completed = 0
        self.total_tasks = 5

        # Estado
        self.is_alive = True
        self.can_vote = True

        # ✅ HITBOX REAL (centrado)
        # Si hacés el sprite más grande pero el rect no está centrado, “se siente igual”.
        self.width = 56
        self.height = 56
        self.rect = pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def update_rect(self):
        """Actualiza el rectángulo de colisión según la posición (centrado)"""
        self.rect.topleft = (
            int(self.x - self.width // 2),
            int(self.y - self.height // 2)
        )

    def get_task_progress(self):
        """Retorna el progreso de tareas como porcentaje (0.0 a 1.0)"""
        if self.total_tasks == 0:
            return 0.0
        return self.tasks_completed / self.total_tasks

    def complete_task(self):
        """Marca una tarea como completada"""
        if self.tasks_completed < self.total_tasks:
            self.tasks_completed += 1

    def reset_position(self, x, y):
        """Cambia la posición del jugador"""
        self.x = x
        self.y = y
        self.update_rect()
