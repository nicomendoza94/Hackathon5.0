import pygame
import os

class Meeting:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Verdana", 36, bold=True)
        self.font_name = pygame.font.SysFont("Verdana", 20, bold=True)
        self.RES_OBJETIVO = (1280, 720) # Resolución oficial del proyecto 
        
        # --- CARGA DEL FONDO DEL MEETING ---
        try:
            # Puedes usar una imagen llamada Fondo.meeting.png
            path_fondo = "assets/images/run_jeremy.png"
            img_original = pygame.image.load(path_fondo).convert_alpha()
            self.fondo = pygame.transform.smoothscale(img_original, self.RES_OBJETIVO)
        except pygame.error:
            # Fondo de respaldo (Gris oscuro tipo oficina)
            self.fondo = pygame.Surface(self.RES_OBJETIVO)
            self.fondo.fill((45, 45, 50))

    def draw(self, npcs_list, selected_index):
        """Dibuja la pantalla de votación con la lista de NPCs[cite: 211]."""
        # 1. Dibujar el fondo del Congreso
        self.screen.blit(self.fondo, (0, 0))
        
        # 2. Título de la reunión
        shadow = self.font_title.render("¡SESIÓN EXTRAORDINARIA!", True, (0, 0, 0))
        title = self.font_title.render("¡SESIÓN EXTRAORDINARIA!", True, (255, 255, 0))
        self.screen.blit(shadow, (self.screen.get_width()//2 - 248, 42))
        self.screen.blit(title, (self.screen.get_width()//2 - 250, 40))

        # 3. Dibujar la cuadrícula de NPCs para votar [cite: 212]
        # Organizamos a los diputados en dos columnas
        start_x, start_y = 150, 150
        for i, npc in enumerate(npcs_list):
            col = i % 2
            row = i // 2
            x = start_x + (col * 500)
            y = start_y + (row * 80)
            
            # Color de selección: Amarillo si el mouse está encima
            box_color = (255, 255, 0) if i == selected_index else (200, 200, 200)
            
            # Fondo de la tarjeta del diputado
            pygame.draw.rect(self.screen, (0, 0, 0, 150), (x, y, 400, 60), border_radius=10)
            pygame.draw.rect(self.screen, box_color, (x, y, 400, 60), 3, border_radius=10)
            
            # Nombre del NPC (Extraído de npcs.json) [cite: 125]
            nombre_txt = self.font_name.render(f"Diputado: {npc['name']}", True, (255, 255, 255))
            self.screen.blit(nombre_txt, (x + 20, y + 15))