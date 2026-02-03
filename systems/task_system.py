import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE

class TaskSystem:
    def __init__(self):
        self.current_task = None
        self.minigame_active = False

        self.font_small = pygame.font.SysFont("Arial", 20)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_large = pygame.font.SysFont("Arial", 48)

        self._init_minigames()

    def _init_minigames(self):
        self.sign_progress = 0
        self.sign_target = 100

        self.review_text = self._generate_random_text()
        self.review_found = False
        self.review_clicks = 0

        self.mic_position = 50
        self.mic_target = random.randint(0, 100)
        self.mic_speed = 2

        self.empanadas_orders = self._generate_orders()
        self.empanadas_completed = 0
        self.empanadas_time = 10
        self.empanadas_start_time = 0

        # SLEEP
        self.sleep_energy = 100.0
        self.sleep_clicks = 0
        self.sleep_duration = 8
        self.sleep_start_time = 0

    def update(self, player, tasks):
        # (por ahora no hace nada visual)
        pass

    def try_start_task(self, player, tasks):
        for task in tasks:
            if not task.completed and task.is_near_player(player.x, player.y):
                self.start_minigame(task)
                return True
        return False

    def start_minigame(self, task):
        self.current_task = task
        self.minigame_active = True
        task.start()

        if task.task_type == "sign":
            self.sign_progress = 0

        elif task.task_type == "review":
            self.review_text = self._generate_random_text()
            self.review_found = False
            self.review_clicks = 0

        elif task.task_type == "mic":
            self.mic_position = 50
            self.mic_target = random.randint(40, 60)

        elif task.task_type == "empanadas":
            self.empanadas_orders = self._generate_orders()
            self.empanadas_completed = 0
            self.empanadas_start_time = pygame.time.get_ticks()

        elif task.task_type == "sleep":
            self.sleep_energy = 100.0
            self.sleep_clicks = 0
            self.sleep_start_time = pygame.time.get_ticks()

    def handle_minigame_event(self, event):
        if not self.minigame_active or not self.current_task:
            return False

        task_type = self.current_task.task_type

        if task_type == "sign":
            return self._handle_sign_event(event)
        elif task_type == "review":
            return self._handle_review_event(event)
        elif task_type == "mic":
            return self._handle_mic_event(event)
        elif task_type == "empanadas":
            return self._handle_empanadas_event(event)
        elif task_type == "sleep":
            return self._handle_sleep_event(event)

        return False

    def update_minigame(self):
        if not self.minigame_active or not self.current_task:
            return False

        task_type = self.current_task.task_type

        if task_type == "mic":
            return self._update_mic()
        elif task_type == "empanadas":
            return self._update_empanadas()
        elif task_type == "sleep":
            return self._update_sleep()

        return False

    def draw_minigame(self, screen):
        if not self.minigame_active or not self.current_task:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))

        task_type = self.current_task.task_type

        if task_type == "sign":
            self._draw_sign_minigame(screen)
        elif task_type == "review":
            self._draw_review_minigame(screen)
        elif task_type == "mic":
            self._draw_mic_minigame(screen)
        elif task_type == "empanadas":
            self._draw_empanadas_minigame(screen)
        elif task_type == "sleep":
            self._draw_sleep_minigame(screen)

        cancel_text = self.font_small.render("Presiona ESC para cancelar", True, WHITE)
        screen.blit(cancel_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30))

    def complete_minigame(self):
        if self.current_task:
            self.current_task.complete()
        self.minigame_active = False
        self.current_task = None

    def cancel_minigame(self):
        if self.current_task:
            self.current_task.cancel()
        self.minigame_active = False
        self.current_task = None

    # ========= SIGN =========
    def _handle_sign_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sign_progress += random.randint(5, 15)
            if self.sign_progress >= self.sign_target:
                self.complete_minigame()
                return True
        return False

    def _draw_sign_minigame(self, screen):
        title = self.font_large.render("Firmar Presupuesto", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 200, 100))

        instruction = self.font_medium.render("¡Clickeá rápido para firmar!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 250, 180))

        bar_width = 400
        bar_height = 50
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300

        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        progress_width = int((self.sign_progress / self.sign_target) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, bar_height))

        percentage = int((self.sign_progress / self.sign_target) * 100)
        percent_text = self.font_medium.render(f"{percentage}%", True, WHITE)
        screen.blit(percent_text, (SCREEN_WIDTH//2 - 30, bar_y + 10))

    # ========= REVIEW =========
    def _generate_random_text(self):
        words = ["presupuesto", "diputado", "sesión", "votación", "proyecto",
                 "comisión", "informe", "congreso", "senado", "error"]
        text = [random.choice(words) for _ in range(50)]
        if "error" not in text:
            text[random.randint(0, len(text)-1)] = "error"
        return text

    def _handle_review_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            start_x, start_y = 100, 150
            x, y = start_x, start_y

            for word in self.review_text:
                word_surf = self.font_small.render(word, True, WHITE)
                word_rect = word_surf.get_rect(topleft=(x, y))

                if word_rect.collidepoint(mouse_x, mouse_y):
                    self.review_clicks += 1
                    if word == "error":
                        self.review_found = True
                        self.complete_minigame()
                        return True

                x += word_surf.get_width() + 10
                if x > SCREEN_WIDTH - 150:
                    x = start_x
                    y += 30

        return False

    def _draw_review_minigame(self, screen):
        title = self.font_large.render("Revisar Informe", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 180, 50))

        instruction = self.font_small.render("¡Encontrá la palabra 'error' en el texto!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 200, 100))

        start_x, start_y = 100, 150
        x, y = start_x, start_y

        for word in self.review_text:
            color = WHITE
            word_surf = self.font_small.render(word, True, color)
            screen.blit(word_surf, (x, y))

            x += word_surf.get_width() + 10
            if x > SCREEN_WIDTH - 150:
                x = start_x
                y += 30

        clicks_text = self.font_small.render(f"Clicks: {self.review_clicks}", True, WHITE)
        screen.blit(clicks_text, (SCREEN_WIDTH - 150, 100))

    # ========= MIC =========
    def _update_mic(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mic_position = max(0, self.mic_position - self.mic_speed)
        if keys[pygame.K_RIGHT]:
            self.mic_position = min(100, self.mic_position + self.mic_speed)
        return False

    def _handle_mic_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if abs(self.mic_position - self.mic_target) < 5:
                self.complete_minigame()
                return True
        return False

    def _draw_mic_minigame(self, screen):
        title = self.font_large.render("Ajustar Micrófono", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 220, 100))

        instruction = self.font_medium.render("Usá ← →, ESPACIO confirma", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 260, 180))

        bar_width = 500
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300

        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, 20), 2)

        target_x = bar_x + int((self.mic_target / 100) * bar_width)
        pygame.draw.rect(screen, GREEN, (target_x - 15, bar_y - 5, 30, 30))

        current_x = bar_x + int((self.mic_position / 100) * bar_width)
        pygame.draw.circle(screen, BLUE, (current_x, bar_y + 10), 15)

    # ========= EMPANADAS =========
    def _generate_orders(self):
        types = ["carne", "pollo", "jamon y queso", "choclo"]
        return [random.choice(types) for _ in range(5)]

    def _update_empanadas(self):
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.empanadas_start_time) / 1000

        if elapsed >= self.empanadas_time:
            if self.empanadas_completed >= len(self.empanadas_orders):
                self.complete_minigame()
                return True
            else:
                self.cancel_minigame()
                return False

        return False

    def _handle_empanadas_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.empanadas_completed < len(self.empanadas_orders):
                target = self.empanadas_orders[self.empanadas_completed]

                key_map = {
                    pygame.K_1: "carne",
                    pygame.K_2: "pollo",
                    pygame.K_3: "jamon y queso",
                    pygame.K_4: "choclo"
                }

                if event.key in key_map and key_map[event.key] == target:
                    self.empanadas_completed += 1
                    if self.empanadas_completed >= len(self.empanadas_orders):
                        self.complete_minigame()
                        return True

        return False

    def _draw_empanadas_minigame(self, screen):
        title = self.font_large.render("Repartir Empanadas", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 220, 50))

        instruction = self.font_small.render("1:Carne 2:Pollo 3:Jamon y Queso 4:Choclo", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 190, 120))

        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.empanadas_start_time) / 1000
        remaining = max(0, self.empanadas_time - elapsed)

        time_text = self.font_medium.render(f"Tiempo: {remaining:.1f}s", True, WHITE if remaining > 3 else RED)
        screen.blit(time_text, (SCREEN_WIDTH//2 - 100, 180))

        y = 250
        for i, order in enumerate(self.empanadas_orders):
            color = GREEN if i < self.empanadas_completed else WHITE
            order_text = self.font_medium.render(f"{i+1}. {order.capitalize()}", True, color)
            screen.blit(order_text, (SCREEN_WIDTH//2 - 100, y))
            y += 40

    # ========= SLEEP (FIX REAL) =========
    def _update_sleep(self):
        # La energía ya NO se resetea cada frame.
        # Se drena gradualmente, y los clicks la suben.
        self.sleep_energy -= 0.6  # ajustá: más alto = más difícil

        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.sleep_start_time) / 1000

        if self.sleep_energy <= 0:
            self.sleep_energy = 0
            self.cancel_minigame()
            return False

        # si aguantó el tiempo, gana
        if elapsed >= self.sleep_duration:
            self.complete_minigame()
            return True

        return False

    def _handle_sleep_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sleep_clicks += 1
            self.sleep_energy = min(100, self.sleep_energy + 10)
        return False

    def _draw_sleep_minigame(self, screen):
        title = self.font_large.render("¡No te durmás!", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 180, 100))

        instruction = self.font_medium.render("¡Clickeá para mantener despierto!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 290, 180))

        bar_width = 400
        bar_height = 50
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300

        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        energy_width = int((self.sleep_energy / 100) * bar_width)
        color = GREEN if self.sleep_energy > 50 else RED
        pygame.draw.rect(screen, color, (bar_x, bar_y, energy_width, bar_height))

        energy_text = self.font_medium.render(f"{int(self.sleep_energy)}%", True, WHITE)
        screen.blit(energy_text, (SCREEN_WIDTH//2 - 30, bar_y + 10))

        clicks_text = self.font_small.render(f"Clicks: {self.sleep_clicks}", True, WHITE)
        screen.blit(clicks_text, (SCREEN_WIDTH//2 - 50, bar_y + 80))
