import pygame

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont("Verdana", 20, bold=True)
        self.font_small = pygame.font.SysFont("Verdana", 16, bold=True)

    def _bar(self, x, y, w, h, value_0_100, label, fg):
        pygame.draw.rect(self.screen, (25, 25, 25), (x, y, w, h), border_radius=6)
        fill = int(w * max(0, min(100, value_0_100)) / 100)
        pygame.draw.rect(self.screen, fg, (x, y, fill, h), border_radius=6)
        pygame.draw.rect(self.screen, (220, 220, 220), (x, y, w, h), 2, border_radius=6)
        t = self.font_small.render(f"{label}: {int(value_0_100)}/100", True, (255, 255, 255))
        self.screen.blit(t, (x, y - 18))

    def draw(self, player_role, task_progress, timer_seconds, score, current_task_name,
             stress, suspicion):
        # Panel superior simple
        mins, secs = divmod(int(timer_seconds), 60)
        time_str = f"{mins:02d}:{secs:02d}"

        line1 = self.font_main.render(f"TIEMPO: {time_str}   PUNTOS: {score}", True, (255, 215, 0))
        self.screen.blit(line1, (20, 16))

        line2 = self.font_main.render(f"ROL: {player_role}", True, (200, 255, 255))
        self.screen.blit(line2, (20, 44))

        # Tareas
        line3 = self.font_small.render(f"TAREA: {current_task_name}", True, (255, 255, 255))
        self.screen.blit(line3, (20, 74))

        # Progreso tareas (barra)
        px, py = 20, 102
        w, h = 260, 16
        pygame.draw.rect(self.screen, (25, 25, 25), (px, py, w, h), border_radius=6)
        pygame.draw.rect(self.screen, (50, 205, 50), (px, py, int(w * task_progress), h), border_radius=6)
        pygame.draw.rect(self.screen, (220, 220, 220), (px, py, w, h), 2, border_radius=6)
        ptxt = self.font_small.render(f"Tareas: {int(task_progress*100)}%", True, (255, 255, 255))
        self.screen.blit(ptxt, (px, py + 20))

        # Barras nuevas
        self._bar(320, 20, 240, 16, stress, "Estrés", (255, 90, 90))
        self._bar(320, 62, 240, 16, suspicion, "Sospecha", (255, 160, 100))
