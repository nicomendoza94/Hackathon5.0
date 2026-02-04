"""
Sistema de movimiento y colisiones.

Responsabilidad:
- Mover player y NPCs
- Detectar colisiones con paredes y obstáculos
- Aplicar límites del mapa
"""
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class MovementSystem:
    """Maneja el movimiento de entidades y colisiones"""
    
    def __init__(self):
        # Límites del mapa (con margen)
        self.min_x = 50
        self.max_x = SCREEN_WIDTH - 50
        self.min_y = 100
        self.max_y = SCREEN_HEIGHT - 100
    
    def update(self, player, npcs):
        """
        Actualiza posiciones del jugador y NPCs.
        
        Args:
            player: Objeto Player
            npcs: Lista de NPCs (puede estar vacía)
        """
        # Mover jugador
        self._move_player(player)
        
        # Mover NPCs (si existen)
        if npcs and isinstance(npcs, list):
            for npc in npcs:
                self._move_npc(npc)
    
    def _move_player(self, player):
        """Mueve al jugador y aplica límites"""
        # Aplicar velocidad
        player.x += player.velocity_x
        player.y += player.velocity_y
        
        # Aplicar límites del mapa
        player.x = max(self.min_x, min(player.x, self.max_x))
        player.y = max(self.min_y, min(player.y, self.max_y))
        
        # Actualizar rectángulo de colisión
        player.update_rect()
    
    def _move_npc(self, npc):
        """Mueve un NPC (si tiene lógica de movimiento)"""
        # Los NPCs se mueven según su lógica interna
        # (ya implementada en entities/npc.py)
        
        # Aplicar límites también a NPCs
        if hasattr(npc, 'x') and hasattr(npc, 'y'):
            npc.x = max(self.min_x, min(npc.x, self.max_x))
            npc.y = max(self.min_y, min(npc.y, self.max_y))