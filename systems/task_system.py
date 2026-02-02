import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE

class TaskSystem:
    """
    Sistema que maneja todas las tareas y minijuegos del juego.
    """
    
    def __init__(self):
        self.current_task = None
        self.minigame_active = False
        
        # Fuentes para los minijuegos
        self.font_small = pygame.font.SysFont("Arial", 20)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_large = pygame.font.SysFont("Arial", 48)
        
        # Variables para cada minijuego
        self._init_minigames()

    def _init_minigames(self):
        
        """Inicializa las variables de cada minijuego"""
        
        # Minijuego 1: Firmar presupuesto
        self.sign_progress = 0
        self.sign_target = 100
        
        # Minijuego 2: Revisar informe
        self.review_text = self._generate_random_text()
        self.review_found = False
        self.review_clicks = 0
        
        # Minijuego 3: Ajustar micrófono
        self.mic_position = 50
        self.mic_target = random.randint(40, 60)
        self.mic_speed = 2
        
        # Minijuego 4: Repartir empanadas
        self.empanadas_orders = self._generate_orders()
        self.empanadas_completed = 0
        self.empanadas_time = 10
        self.empanadas_start_time = 0
        
        # Minijuego 5: Evitar que se duerma
        self.sleep_energy = 100
        self.sleep_clicks = 0
        self.sleep_duration = 8
        self.sleep_start_time = 0
        
    def update(self, player, tasks):
        """
        Actualiza el sistema de tareas cada frame.
        
        Args:
            player: Objeto del jugador
            tasks: Lista de todas las tareas del nivel
        """
        if not self.minigame_active:
            # Buscar tareas cercanas al jugador
            for task in tasks:
                if not task.completed and task.is_near_player(player.x, player.y):
                    # Aquí se podría mostrar un indicador visual
                    pass
        
    def try_start_task(self, player, tasks):
        """
        Intenta iniciar una tarea si el jugador está cerca y presiona la tecla.
        
        Args:
            player: Objeto del jugador
            tasks: Lista de tareas
            
        Returns:
            True si se inició una tarea
        """
        for task in tasks:
            if not task.completed and task.is_near_player(player.x, player.y):
                self.start_minigame(task)
                return True
        return False
    
    def start_minigame(self, task):
        """Inicia el minijuego de una tarea"""
        self.current_task = task
        self.minigame_active = True
        task.start()
        
        # Reiniciar variables según el tipo de tarea
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
            self.sleep_energy = 100
            self.sleep_clicks = 0
            self.sleep_start_time = pygame.time.get_ticks()
    
    def handle_minigame_event(self, event):
        """
        Maneja eventos (clicks, teclas) dentro de un minijuego.
        
        Args:
            event: Evento de pygame
            
        Returns:
            True si el minijuego se completó
        """
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
        """Actualiza la lógica del minijuego activo"""
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
        """
        Dibuja el minijuego activo en pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.minigame_active or not self.current_task:
            return
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))
        
        # Dibujar según el tipo de tarea
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
        
        # Botón para cancelar (ESC)
        cancel_text = self.font_small.render("Presiona ESC para cancelar", True, WHITE)
        screen.blit(cancel_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30))
    
    def complete_minigame(self):
        """Completa el minijuego actual"""
        if self.current_task:
            self.current_task.complete()
        self.minigame_active = False
        self.current_task = None
    
    def cancel_minigame(self):
        """Cancela el minijuego actual"""
        if self.current_task:
            self.current_task.cancel()
        self.minigame_active = False
        self.current_task = None
    
    # ========== MINIJUEGO 1: FIRMAR PRESUPUESTO ==========
    
    def _handle_sign_event(self, event):
        """Maneja eventos del minijuego de firmar"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sign_progress += random.randint(5, 15)
            if self.sign_progress >= self.sign_target:
                self.complete_minigame()
                return True
        return False
    
    def _draw_sign_minigame(self, screen):
        """Dibuja el minijuego de firmar presupuesto"""
        title = self.font_large.render("Firmar Presupuesto", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 200, 100))
        
        instruction = self.font_medium.render("¡Clickeá rápido para firmar!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 200, 180))
        
        # Barra de progreso
        bar_width = 400
        bar_height = 50
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300
        
        # Fondo de la barra
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Progreso
        progress_width = int((self.sign_progress / self.sign_target) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, bar_height))
        
        # Porcentaje
        percentage = int((self.sign_progress / self.sign_target) * 100)
        percent_text = self.font_medium.render(f"{percentage}%", True, WHITE)
        screen.blit(percent_text, (SCREEN_WIDTH//2 - 30, bar_y + 10))
    
    # ========== MINIJUEGO 2: REVISAR INFORME ==========
    
    def _generate_random_text(self):
        """Genera texto aleatorio con la palabra 'ERROR' escondida"""
        words = ["presupuesto", "diputado", "sesión", "votación", "proyecto", 
                 "comisión", "informe", "congreso", "senado", "ERROR"]
        text = []
        for _ in range(50):
            text.append(random.choice(words))
        # Asegurar que ERROR esté al menos una vez
        if "ERROR" not in text:
            text[random.randint(0, len(text)-1)] = "ERROR"
        return text
    
    def _handle_review_event(self, event):
        """Maneja eventos del minijuego de revisar"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Verificar si clickeó en alguna palabra
            start_x, start_y = 100, 150
            x, y = start_x, start_y
            
            for i, word in enumerate(self.review_text):
                word_surf = self.font_small.render(word, True, WHITE)
                word_rect = word_surf.get_rect(topleft=(x, y))
                
                if word_rect.collidepoint(mouse_x, mouse_y):
                    self.review_clicks += 1
                    if word == "ERROR":
                        self.review_found = True
                        self.complete_minigame()
                        return True
                
                x += word_surf.get_width() + 10
                if x > SCREEN_WIDTH - 150:
                    x = start_x
                    y += 30
        
        return False
    
    def _draw_review_minigame(self, screen):
        """Dibuja el minijuego de revisar informe"""
        title = self.font_large.render("Revisar Informe", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 180, 50))
        
        instruction = self.font_small.render("¡Encontrá la palabra 'ERROR' en el texto!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 200, 100))
        
        # Dibujar texto
        start_x, start_y = 100, 150
        x, y = start_x, start_y
        
        for word in self.review_text:
            color = RED if word == "ERROR" else WHITE
            word_surf = self.font_small.render(word, True, color)
            screen.blit(word_surf, (x, y))
            
            x += word_surf.get_width() + 10
            if x > SCREEN_WIDTH - 150:
                x = start_x
                y += 30
        
        # Contador de clicks
        clicks_text = self.font_small.render(f"Clicks: {self.review_clicks}", True, WHITE)
        screen.blit(clicks_text, (SCREEN_WIDTH - 150, 100))
    
    # ========== MINIJUEGO 3: AJUSTAR MICRÓFONO ==========
    
    def _update_mic(self):
        """Actualiza el minijuego del micrófono"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.mic_position = max(0, self.mic_position - self.mic_speed)
        if keys[pygame.K_RIGHT]:
            self.mic_position = min(100, self.mic_position + self.mic_speed)
        
        return False
    
    def _handle_mic_event(self, event):
        """Maneja eventos del minijuego del micrófono"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Verificar si está en la zona correcta
            if abs(self.mic_position - self.mic_target) < 5:
                self.complete_minigame()
                return True
        return False
    
    def _draw_mic_minigame(self, screen):
        """Dibuja el minijuego del micrófono"""
        title = self.font_large.render("Ajustar Micrófono", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 220, 100))
        
        instruction = self.font_medium.render("Usá ← → para ajustar, ESPACIO para confirmar", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 350, 180))
        
        # Barra de ajuste
        bar_width = 500
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300
        
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, 20), 2)
        
        # Zona objetivo (verde)
        target_x = bar_x + int((self.mic_target / 100) * bar_width)
        pygame.draw.rect(screen, GREEN, (target_x - 15, bar_y - 5, 30, 30))
        
        # Posición actual (azul)
        current_x = bar_x + int((self.mic_position / 100) * bar_width)
        pygame.draw.circle(screen, BLUE, (current_x, bar_y + 10), 15)
    
    # ========== MINIJUEGO 4: REPARTIR EMPANADAS ==========
    
    def _generate_orders(self):
        """Genera pedidos aleatorios de empanadas"""
        types = ["carne", "pollo", "queso", "humita"]
        return [random.choice(types) for _ in range(5)]
    
    def _update_empanadas(self):
        """Actualiza el minijuego de empanadas"""
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.empanadas_start_time) / 1000
        
        if elapsed >= self.empanadas_time:
            # Se acabó el tiempo
            if self.empanadas_completed >= len(self.empanadas_orders):
                self.complete_minigame()
                return True
            else:
                self.cancel_minigame()
                return False
        
        return False
    
    def _handle_empanadas_event(self, event):
        """Maneja eventos del minijuego de empanadas"""
        if event.type == pygame.KEYDOWN:
            if self.empanadas_completed < len(self.empanadas_orders):
                target = self.empanadas_orders[self.empanadas_completed]
                
                key_map = {
                    pygame.K_1: "carne",
                    pygame.K_2: "pollo",
                    pygame.K_3: "queso",
                    pygame.K_4: "humita"
                }
                
                if event.key in key_map:
                    if key_map[event.key] == target:
                        self.empanadas_completed += 1
                        if self.empanadas_completed >= len(self.empanadas_orders):
                            self.complete_minigame()
                            return True
        
        return False
    
    def _draw_empanadas_minigame(self, screen):
        """Dibuja el minijuego de repartir empanadas"""
        title = self.font_large.render("Repartir Empanadas", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 220, 50))
        
        instruction = self.font_small.render("Presioná 1:Carne 2:Pollo 3:Queso 4:Humita", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 250, 120))
        
        # Tiempo restante
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.empanadas_start_time) / 1000
        remaining = max(0, self.empanadas_time - elapsed)
        time_text = self.font_medium.render(f"Tiempo: {remaining:.1f}s", True, WHITE if remaining > 3 else RED)
        screen.blit(time_text, (SCREEN_WIDTH//2 - 100, 180))
        
        # Pedidos
        y = 250
        for i, order in enumerate(self.empanadas_orders):
            color = GREEN if i < self.empanadas_completed else WHITE
            order_text = self.font_medium.render(f"{i+1}. {order.capitalize()}", True, color)
            screen.blit(order_text, (SCREEN_WIDTH//2 - 100, y))
            y += 40
    
    # ========== MINIJUEGO 5: EVITAR QUE SE DUERMA ==========
    
    def _update_sleep(self):
        """Actualiza el minijuego de mantener despierto"""
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.sleep_start_time) / 1000
        
        # La energía baja con el tiempo
        self.sleep_energy = 100 - (elapsed / self.sleep_duration) * 100
        
        if self.sleep_energy <= 0:
            self.cancel_minigame()
            return False
        
        if elapsed >= self.sleep_duration and self.sleep_energy > 20:
            self.complete_minigame()
            return True
        
        return False
    
    def _handle_sleep_event(self, event):
        """Maneja eventos del minijuego de mantener despierto"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sleep_clicks += 1
            self.sleep_energy = min(100, self.sleep_energy + 10)
        return False
    
    def _draw_sleep_minigame(self, screen):
        """Dibuja el minijuego de mantener despierto"""
        title = self.font_large.render("¡No te durmás!", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - 180, 100))
        
        instruction = self.font_medium.render("¡Clickeá para mantener al diputado despierto!", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - 350, 180))
        
        # Barra de energía
        bar_width = 400
        bar_height = 50
        bar_x = SCREEN_WIDTH//2 - bar_width//2
        bar_y = 300
        
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Energía
        energy_width = int((self.sleep_energy / 100) * bar_width)
        color = GREEN if self.sleep_energy > 50 else RED
        pygame.draw.rect(screen, color, (bar_x, bar_y, energy_width, bar_height))
        
        # Porcentaje
        energy_text = self.font_medium.render(f"{int(self.sleep_energy)}%", True, WHITE)
        screen.blit(energy_text, (SCREEN_WIDTH//2 - 30, bar_y + 10))
        
        # Clicks
        clicks_text = self.font_small.render(f"Clicks: {self.sleep_clicks}", True, WHITE)
        screen.blit(clicks_text, (SCREEN_WIDTH//2 - 50, bar_y + 80))