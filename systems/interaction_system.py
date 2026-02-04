"""
Sistema de interacciones.

Responsabilidad:
- Detectar interacción jugador ↔ tareas
- Detectar interacción jugador ↔ NPCs
- Lanzar eventos de tareas o reuniones
"""
import pygame

class InteractionSystem:
    """Maneja las interacciones del jugador con el mundo"""
    
    def __init__(self):
        self.interaction_distance = 50  # Distancia para interactuar
    
    def check_task_interaction(self, player, tasks):
        """
        Verifica si el jugador puede interactuar con alguna tarea.
        
        Args:
            player: Objeto Player
            tasks: Lista de tareas
            
        Returns:
            Task si hay una cercana, None si no
        """
        if not tasks or not isinstance(tasks, list):
            return None
        
        for task in tasks:
            if not task.completed:
                # Verificar distancia
                if task.is_near_player(player.x, player.y, self.interaction_distance):
                    return task
        
        return None
    
    def check_npc_interaction(self, player, npcs):
        """
        Verifica si el jugador está cerca de algún NPC.
        
        Args:
            player: Objeto Player
            npcs: Lista de NPCs
            
        Returns:
            NPC si hay uno cercano, None si no
        """
        if not npcs or not isinstance(npcs, list):
            return None
        
        for npc in npcs:
            # Calcular distancia
            dx = npc.x - player.x
            dy = npc.y - player.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.interaction_distance:
                return npc
        
        return None