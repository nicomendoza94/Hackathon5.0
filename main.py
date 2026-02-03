# main.py
import pygame
from core.game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Instanciamos el juego
    game = Game(screen)
    game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        # Cargamos fuentes para el estilo del Congreso
        self.font_titulo = pygame.font.SysFont("Verdana", 42, bold=True)
        self.font_opciones = pygame.font.SysFont("Arial", 22, bold=True)
        
        # Resolución objetivo
        self.RES_OBJETIVO = (1280, 720)
        
        # Intentamos cargar un fondo para el menú
        try:
            img = pygame.image.load("assets/images/Fondo.hud.png").convert_alpha()
            self.fondo = pygame.transform.smoothscale(img, self.RES_OBJETIVO)
        except:
            self.fondo = pygame.Surface(self.RES_OBJETIVO)
            self.fondo.fill((20, 30, 20))

    def draw(self):
        """Dibuja la pantalla principal del menú."""
        # 1. Dibujar fondo con un filtro oscuro para que resalte el texto
        self.screen.blit(self.fondo, (0, 0))
        overlay = pygame.Surface(self.RES_OBJETIVO, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        self.screen.blit(overlay, (0, 0))

        # 2. Título con sombra (Estilo "El Impostor en el Congreso")
        texto_titulo = "EL IMPOSTOR EN EL CONGRESO"
        sombra = self.font_titulo.render(texto_titulo, True, (0, 0, 0))
        titulo = self.font_titulo.render(texto_titulo, True, (255, 255, 0))
        
        rect_titulo = titulo.get_rect(center=(self.screen.get_width()//2, 200))
        self.screen.blit(sombra, (rect_titulo.x + 4, rect_titulo.y + 4))
        self.screen.blit(titulo, rect_titulo)

        # 3. Instrucciones de navegación para el test
        instrucciones = [
            "Presiona '2' para INICIAR SESIÓN",
            "Presiona 'ESC' para SALIR"
        ]
        
        for i, linea in enumerate(instrucciones):
            txt = self.font_opciones.render(linea, True, (255, 255, 255))
            rect = txt.get_rect(center=(self.screen.get_width()//2, 400 + (i * 40)))
            self.screen.blit(txt, rect)