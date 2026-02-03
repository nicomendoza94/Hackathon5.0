import pygame
import os

class IconManager:
    def __init__(self):
        self.icons = {}
        # Lista de iconos extraídos de tus tareas y sabotajes
        self.icon_names = ["presupuesto", "empanada", "microfono", "luz", "cumbia", "aire"]
        self.load_icons()

    def load_icons(self):
        """Carga y escala los iconos a 32x32 píxeles."""
        for name in self.icon_names:
            path = f"assets/images/icons/{name}.png"
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.icons[name] = pygame.transform.smoothscale(img, (32, 32))
            else:
                # Si falta el archivo, crea un cuadro de color (Placeholder)
                surf = pygame.Surface((32, 32))
                color = (0, 255, 255) if name in ["presupuesto", "empanada"] else (255, 50, 50)
                surf.fill(color)
                self.icons[name] = surf

    def get(self, name):
        return self.icons.get(name, self.icons.get("presupuesto"))