import pygame
import os

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_titulo = pygame.font.SysFont("Verdana", 42, bold=True)
        self.font_opciones = pygame.font.SysFont("Arial", 22, bold=True)
        self.RES_OBJETIVO = (1280, 720)
        
        # Intentamos cargar tu imagen específica
        path_menu = "assets/images/Fondo_menu_Jeremy.png"
        print(f"Buscando imagen en: {os.path.abspath(path_menu)}")
        
        try:
            img = pygame.image.load(path_menu).convert_alpha()
            self.fondo = pygame.transform.smoothscale(img, self.RES_OBJETIVO)
            print("¡Imagen de fondo del menú cargada correctamente!")
        except:
            print(f"ADVERTENCIA: No se encontró {path_menu}. Usando fondo de respaldo.")
            self.fondo = pygame.Surface(self.RES_OBJETIVO)
            self.fondo.fill((20, 30, 20))

    def draw(self): # NOTA: Ya no recibe 'screen' aquí
        """Dibuja el menú principal."""
        self.screen.blit(self.fondo, (0, 0))
        
        # Filtro oscuro para resaltar texto
        overlay = pygame.Surface(self.RES_OBJETIVO, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120)) 
        self.screen.blit(overlay, (0, 0))

        # Título
        titulo_txt = ""
        titulo = self.font_titulo.render(titulo_txt, True, (255, 255, 0))
        rect_titulo = titulo.get_rect(center=(self.screen.get_width()//2, 200))
        self.screen.blit(titulo, rect_titulo)

        # Instrucción
        inst = self.font_opciones.render("Presiona '2' para iniciar la sesión", True, (255, 255, 255))
        self.screen.blit(inst, inst.get_rect(center=(self.screen.get_width()//2, 450)))