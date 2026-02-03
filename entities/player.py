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
        
        # Rol del jugador (70% Ciudadano, 30% Impostor)
        self.role = "Diputado" if random.random() < 0.7 else "Impostor"
        self.is_impostor = (self.role == "Impostor")
        
        # Progreso de tareas
        self.tasks_completed = 0
        self.total_tasks = 5
        
        # Estado
        self.is_alive = True
        self.can_vote = True
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        
    def update_rect(self):
        """Actualiza el rectángulo de colisión según la posición"""
        self.rect.x = self.x - 15
        self.rect.y = self.y - 15
    
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