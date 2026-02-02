"""
Punto de entrada del juego.

Responsabilidad:
- Inicializar pygame
- Crear la ventana principal
- Instanciar el objeto Game
- Ejecutar el loop principal

Este archivo NO debe contener lógica del juego.
"""
import pygame 
from core.game import Game 
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE 
def main(): 
    pygame.init() 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE) 
    game = Game(screen) 
    game.run() 
    pygame.quit() 
if __name__ == "__main__": 
    main() 
