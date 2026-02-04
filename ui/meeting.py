import os
import pygame

class Meeting:
    """
    Meeting single-player (sin votos):
    - 1) Restablecer orden: limpia sabotajes activos + baja estrés, pero cuesta tiempo.
    - ESC) Volver al juego
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Verdana", 36, bold=True)
        self.font_body = pygame.font.SysFont("Verdana", 22, bold=True)

        # Fondo reunión
        self.bg = None
        path_bg = "assets/images/run_jeremy.png"
        if os.path.exists(path_bg):
            try:
                img = pygame.image.load(path_bg).convert()
                self.bg = pygame.transform.smoothscale(img, (screen.get_width(), screen.get_height()))
            except:
                self.bg = None

    def draw(self, stress, suspicion, timer_seconds, info_lines):
        w, h = self.screen.get_width(), self.screen.get_height()

        # Fondo (imagen o fallback)
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((10, 10, 15))

        # Filtro oscuro para que el texto se lea
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # Tiempo restante
        mins, secs = divmod(int(timer_seconds), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        time_txt = self.font_body.render(f"TIEMPO RESTANTE: {time_str}", True, (255, 215, 0))
        self.screen.blit(time_txt, (w//2 - time_txt.get_width()//2, 30))

        title = self.font_title.render("SESIÓN EXTRAORDINARIA", True, (255, 255, 0))
        self.screen.blit(title, (w//2 - title.get_width()//2, 90))

        s = self.font_body.render(f"Estrés del Congreso: {int(stress)}/100", True, (255, 160, 160))
        self.screen.blit(s, (w//2 - s.get_width()//2, 170))

        sp = self.font_body.render(f"Sospecha global: {int(suspicion)}/100", True, (255, 200, 200))
        self.screen.blit(sp, (w//2 - sp.get_width()//2, 210))

        y = 280
        for line in info_lines:
            t = self.font_body.render(line, True, (255, 255, 255))
            self.screen.blit(t, (w//2 - t.get_width()//2, y))
            y += 32

        opt1 = self.font_body.render(
            "1) Restablecer orden (limpia sabotajes, -25 estrés, cuesta 30s)",
            True,
            (200, 255, 200)
        )
        self.screen.blit(opt1, (w//2 - opt1.get_width()//2, 400))

        opt2 = self.font_body.render("ESC) Volver", True, (200, 200, 255))
        self.screen.blit(opt2, (w//2 - opt2.get_width()//2, 450))
