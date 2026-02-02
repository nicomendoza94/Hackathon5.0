import pygame

class Task:
    """
    Representa una tarea que el jugador debe completar.
    Cada tarea tiene un minijuego asociado.
    """
    
    def __init__(self, name, x, y, task_type, difficulty=1):
        """
        Args:
            name: Nombre de la tarea 
            x, y: Posición en el mapa donde está la tarea
            task_type: Tipo de minijuego
            difficulty: Nivel de dificultad
        """
        self.name = name
        self.x = x
        self.y = y
        self.task_type = task_type
        self.difficulty = difficulty
        self.completed = False
        self.active = False  # Si el jugador está haciendo la tarea ahora
        
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60) # Área de interacción
        
    def is_near_player(self, player_x, player_y, distance=50):
        """
        Verifica si el jugador está cerca de la tarea.
        
        Args:
            player_x, player_y: Posición del jugador
            distance: Distancia máxima para interactuar
            
        Returns:
            True si el jugador puede interactuar con la tarea
        """
        dx = self.x - player_x
        dy = self.y - player_y
        dist = (dx**2 + dy**2)**0.5  # Teorema de Pitágoras
        return dist < distance
    
    def start(self):
        """Inicia la tarea (abre el minijuego)"""
        self.active = True
        
    def complete(self):
        """Marca la tarea como completada"""
        self.completed = True
        self.active = False
        
    def cancel(self):
        """Cancela la tarea actual"""
        self.active = False