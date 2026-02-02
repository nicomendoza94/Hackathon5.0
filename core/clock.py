"""
Control del tiempo del juego.

Responsabilidad:
- Manejar el clock de pygame
- Controlar FPS
- Proveer delta time si es necesario

No debe contener lógica del juego.
"""
import pygame

class Clock():
    def __init__(self, fps):
        self.clock = pygame.time.Clock()
        self.fps = fps
    
    def tick(self):
        return self.clock.tick(self.fps)