import random
import pygame
from entities.sabotage import Sabotage

class SabotageSystem:
    def __init__(self):
        self.sabotages = [
            Sabotage("Luces apagadas", "lights", 10),
            Sabotage("Puertas bloqueadas", "doors", 8),
            Sabotage("Comunicaciones caídas", "comms", 12),
        ]

        # Más seguido:
        self.cooldown = 6000        # ms entre intentos fuertes
        self.last_sabotage_time = 0
        self.trigger_chance = 0.06  # 6% por tick cuando está disponible

        # Mensajes para UI (se ven en pantalla)
        self.ui_messages = []  # list[(text, expires_ms)]

    def _push_ui(self, text, seconds=3.0):
        expires = pygame.time.get_ticks() + int(seconds * 1000)
        self.ui_messages.append((text, expires))

    def get_ui_messages(self):
        now = pygame.time.get_ticks()
        self.ui_messages = [(t, exp) for (t, exp) in self.ui_messages if exp > now]
        return [t for (t, exp) in self.ui_messages]

    def update(self, player, npcs, tasks):
        # Solo el impostor humano dispara sabotajes (Among Us style)
        if not player.is_impostor:
            # Igual mantenemos update de timers por si quedó algo activo
            for s in self.sabotages:
                s.update()
            return

        now = pygame.time.get_ticks()

        # Actualizar sabotajes activos
        for sabotage in self.sabotages:
            sabotage.update()

        # Intentar activar sabotaje
        can_try = (now - self.last_sabotage_time >= self.cooldown) and (not any(s.active for s in self.sabotages))
        if can_try and random.random() < self.trigger_chance:
            self.activate_random_sabotage()
            self.last_sabotage_time = now

        # Evento cómico más seguido
        if random.random() < 0.02:
            self.random_fun_event()

    def random_fun_event(self):
        events = [
            "Un celular suena en plena sesión 📱",
            "Se cae el termo y alguien grita '¡NDERA!' 🧉",
            "El micrófono hace acople y todos miran al técnico 🎤",
            "Aparece una bandeja de empanadas de la nada 🥟",
            "Se arma discusión por el aire acondicionado ❄️",
        ]
        self._push_ui(random.choice(events), seconds=3.0)

    def activate_random_sabotage(self):
        available = [s for s in self.sabotages if not s.active]
        if not available:
            return
        sabotage = random.choice(available)
        sabotage.activate()
        self._push_ui(f"Sabotaje activado: {sabotage.name} ⚠️", seconds=3.5)
