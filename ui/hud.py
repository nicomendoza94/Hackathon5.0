import pygame

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_stats = pygame.font.SysFont("Verdana", 16, bold=True)
        self.font_tarea = pygame.font.SysFont("Arial", 18, bold=True)
        self.RES_OBJETIVO = (1280, 720)
        
        try:
            img_original = pygame.image.load("assets/images/Fondo_hud.png").convert_alpha()
            self.fondo_hud = pygame.transform.smoothscale(img_original, self.RES_OBJETIVO)
        except:
            self.fondo_hud = pygame.Surface(self.RES_OBJETIVO)
            self.fondo_hud.fill((30, 30, 35))

    def _draw_text_with_shadow(self, text, font, color, pos):
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
        label = font.render(text, True, color)
        self.screen.blit(label, pos)

    def draw(self, player_role, task_progress, timer_seconds, score, current_task_name="", sabotajes_list=[]):
        # 1. Dibujar Fondo
        self.screen.blit(self.fondo_hud, (0, 0))

        # 2. Panel Superior (Tiempo y Puntos)
        mins, secs = divmod(timer_seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        self._draw_text_with_shadow(f"TIEMPO: {time_str} | PUNTOS: {score}", 
                                    self.font_stats, (255, 215, 0), (35, 25))

        # 3. Interfaz según el Rol
        if player_role == "Impostor":
            # Pasamos la lista de sabotajes aquí
            self._draw_impostor_ui(sabotajes_list)
        else:
            self._draw_ciudadano_ui(task_progress, current_task_name)

    def _draw_ciudadano_ui(self, progress, task_name):
        pygame.draw.rect(self.screen, (0, 200, 255), (20, 70, 15, 40), border_radius=4)
        self._draw_text_with_shadow("DIPUTADO CIUDADANO", self.font_main, (0, 255, 255), (45, 75))
        self._draw_text_with_shadow(f"TAREA: {task_name}", self.font_tarea, (255, 255, 255), (20, 130))
        
        # Barra de progreso
        pygame.draw.rect(self.screen, (40, 40, 45), (20, 165, 300, 20), border_radius=5)
        fill_w = int(300 * progress)
        pygame.draw.rect(self.screen, (50, 205, 50), (20, 165, fill_w, 20), border_radius=5)

    def _draw_impostor_ui(self, sabotajes):
        """Dibuja la lista de sabotajes disponibles para el Impostor."""
        # Título en Rojo
        pygame.draw.rect(self.screen, (220, 20, 60), (20, 70, 15, 40), border_radius=4)
        self._draw_text_with_shadow("IMPOSTOR", self.font_main, (255, 50, 50), (45, 75))
        
        self._draw_text_with_shadow("SABOTAJES DISPONIBLES:", self.font_stats, (255, 200, 200), (20, 130))
        
        # Dibujar cada sabotaje del JSON como texto
        for i, sabo in enumerate(sabotajes):
            y_pos = 165 + (i * 35)
            # Dibujamos el nombre que viene de 'label' en tu JSON
            texto = f"- {sabo['label']}"
            self._draw_text_with_shadow(texto, self.font_tarea, (230, 230, 230), (30, y_pos))