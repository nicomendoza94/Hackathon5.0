"""
Gestión de íconos UI.

Responsabilidad:
- Cargar y mostrar íconos de estados
- Indicadores visuales (sospecha, tareas, etc.)
"""
import pygame
import os

class IconManager:
    def __init__(self):
        self.icons = {}
        # Lista completa con tus 5 tareas y 5 sabotajes
        self.icon_names = [
            # Tareas del Ciudadano
            "presupuesto", "empanada", "microfono", "aire", "firmar", 
            # Sabotajes del Impostor
            "luz", "cumbia", "huelga", "voto", "planillero"
        ]
        self.load_icons()

    def load_icons(self):
        """Carga y escala los iconos a 32x32 píxeles."""
        for name in self.icon_names:
            path = f"assets/images/icons/{name}.png"
            
            if os.path.exists(path):
                # Si la imagen existe, la cargamos y escalamos suavemente
                img = pygame.image.load(path).convert_alpha()
                self.icons[name] = pygame.transform.smoothscale(img, (32, 32))
            else:
                # Si falta el archivo, creamos un placeholder de color
                surf = pygame.Surface((32, 32))
                
                # Diferenciamos colores: Celeste para tareas, Rojo para sabotajes
                if name in ["presupuesto", "empanada", "microfono", "aire", "firmar"]:
                    color = (0, 200, 255) # Celeste Ciudadano
                else:
                    color = (220, 20, 60) # Rojo Impostor
                
                surf.fill(color)
                # Dibujamos un pequeño borde para que se vea más profesional
                pygame.draw.rect(surf, (255, 255, 255), (0, 0, 32, 32), 1)
                self.icons[name] = surf

    def get(self, name):
        """Obtiene el icono solicitado o uno por defecto si no existe."""
        return self.icons.get(name, self.icons.get("presupuesto"))