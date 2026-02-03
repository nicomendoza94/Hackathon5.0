import pygame
from ui.icons import IconManager

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.icons = IconManager()
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_stats = pygame.font.SysFont("Verdana", 16, bold=True)
        self.RES_OBJETIVO = (1280, 720) # Resolución de tu config.py [cite: 142-143]
        
        try:
            # Escalamos tu fondo de 3008x1408 para que no se vea "tan cerca"
            img_original = pygame.image.load("assets/images/Fondo_hud.png").convert_alpha()
            self.fondo_hud = pygame.transform.smoothscale(img_original, self.RES_OBJETIVO)
        except pygame.error:
            self.fondo_hud = pygame.Surface(self.RES_OBJETIVO)
            self.fondo_hud.fill((30, 30, 35))

    def _draw_text_with_shadow(self, text, font, color, pos):
        """Dibuja texto con sombra para que sea legible sobre el fondo del Congreso."""
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
        label = font.render(text, True, color)
        self.screen.blit(label, pos)

    def _draw_premium_bar(self, x, y, w, h, progress, color_main):
        """Barra de progreso con diseño metálico y brillo."""
        pygame.draw.rect(self.screen, (200, 200, 200), (x-3, y-3, w+6, h+6), border_radius=8)
        pygame.draw.rect(self.screen, (40, 40, 45), (x, y, w, h), border_radius=5)
        if progress > 0:
            fill_w = int(w * max(0, min(progress, 1)))
            pygame.draw.rect(self.screen, color_main, (x, y, fill_w, h), border_radius=5)
            brillo = pygame.Surface((fill_w, h // 2), pygame.SRCALPHA)
            brillo.fill((255, 255, 255, 60))
            self.screen.blit(brillo, (x, y))

    def draw(self, player_role, task_progress, timer_seconds, score):
        # 1. Dibujar Fondo Escalado
        self.screen.blit(self.fondo_hud, (0, 0))

        # 2. Conteo de Tiempo y Puntos (Panel Superior)
        mins, secs = divmod(timer_seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        overlay = pygame.Surface((320, 40), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Fondo oscuro transparente
        self.screen.blit(overlay, (20, 15))
        self._draw_text_with_shadow(f"TIEMPO: {time_str} | PUNTOS: {score}", 
        self.font_stats, (255, 215, 0), (35, 25))

        # 3. Pantalla según el Rol del Jugador [cite: 7-11]
        if player_role == "Impostor":
            self._draw_impostor_ui()
        else:
            self._draw_ciudadano_ui(task_progress)

    def _draw_ciudadano_ui(self, progress):
        """Interfaz para el Diputado Ciudadano."""
        pygame.draw.rect(self.screen, (0, 200, 255), (20, 70, 15, 40), border_radius=4)
        self._draw_text_with_shadow("DIPUTADO CIUDADANO", self.font_main, (0, 255, 255), (45, 75))
        
        # Icono de Tarea: Presupuesto [cite: 44]
        icon = self.icons.get("presupuesto")
        self.screen.blit(icon, (20, 122))
        self._draw_text_with_shadow("PROGRESO DEL PRESUPUESTO:", self.font_stats, (200, 255, 200), (60, 130))
        self._draw_premium_bar(20, 165, 300, 25, progress, (50, 205, 50))

    def _draw_impostor_ui(self):
        """Interfaz para el Impostor."""
        pygame.draw.rect(self.screen, (220, 20, 60), (20, 70, 15, 40), border_radius=4)
        self._draw_text_with_shadow("IMPOSTOR", self.font_main, (255, 50, 50), (45, 75))
        self._draw_text_with_shadow("SABOTAJES DISPONIBLES:", self.font_stats, (255, 200, 200), (20, 130))
        
        # Sabotajes con iconos: Luz y Cumbia [cite: 56-57]
        sabotajes = [("luz", " [F1] CORTAR LUZ"), ("cumbia", " [F2] PONER CUMBIA")]
        for i, (icon_key, label) in enumerate(sabotajes):
            y_pos = 160 + (i * 45)
            pygame.draw.rect(self.screen, (60, 0, 0, 150), (20, y_pos, 280, 40), border_radius=5)
            icon = self.icons.get(icon_key)
            self.screen.blit(icon, (30, y_pos + 4))
            self._draw_text_with_shadow(label, self.font_stats, (230, 230, 230), (70, y_pos + 8))