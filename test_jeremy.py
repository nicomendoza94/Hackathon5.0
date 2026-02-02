import pygame
import sys
from ui.menu import Menu
from ui.hud import HUD
from ui.meeting import Meeting

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Test Jeremy - Hackathon 5.0")
    clock = pygame.time.Clock()

    # Instancias
    menu_ui = Menu(screen)
    hud_ui = HUD(screen)
    meeting_ui = Meeting(screen)

    # Estado y Datos
    estado = "MENU" 
    rol = "Ciudadano"
    progreso = 0.5
    tiempo = 300
    puntos = 150
    npcs = [{"name": "Diputado A"}, {"name": "Diputado B"}, {"name": "Diputado C"}]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: estado = "MENU"
                if event.key == pygame.K_2: estado = "PLAYING"
                if event.key == pygame.K_3: estado = "MEETING"
                if event.key == pygame.K_r:
                    rol = "Impostor" if rol == "Ciudadano" else "Ciudadano"

        screen.fill((0, 0, 0))
        
        if estado == "MENU":
            menu_ui.draw()
        elif estado == "PLAYING":
            hud_ui.draw(rol, progreso, tiempo, puntos)
        elif estado == "MEETING":
            meeting_ui.draw(npcs, 0)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()