"""
Sistema de entrada del jugador.

Responsabilidad:
- Leer teclado y mouse
- Traducir input en acciones del jugador
- No debe modificar directamente el estado del juego
"""
import pygame

class InputSystem:
    """Maneja la entrada del teclado para mover al jugador"""
    
    def __init__(self):
        self.keys = {}
    
    def update(self, player):
        """
        Lee el teclado y actualiza la velocidad del jugador.
        
        Args:
            player: Objeto Player
        """
        # Obtener estado de todas las teclas
        keys = pygame.key.get_pressed()
        
        # Resetear velocidad
        player.velocity_x = 0
        player.velocity_y = 0
        
        # WASD para movimiento
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.velocity_y = -player.speed
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.velocity_y = player.speed
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.velocity_x = -player.speed
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.velocity_x = player.speed
        
        # Normalizar velocidad diagonal (para que no vaya más rápido)
        if player.velocity_x != 0 and player.velocity_y != 0:
            # Reducir velocidad en diagonal
            player.velocity_x *= 0.7071  # 1/sqrt(2)
            player.velocity_y *= 0.7071