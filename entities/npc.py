"""
Entidad NPC (diputados controlados por IA).

Responsabilidad:
- Representar NPCs ciudadanos o impostores
- Mantener su estado interno
- Ejecutar comportamientos simples
"""
import random
import pygame

class NPC:
    STATES = ("WORKING", "WALKING", "SUSPICIOUS")

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

        self.state = "WALKING"
        self.is_impostor = random.random() < 0.1
        self.suspicion = 0.0

        # Anti-spam de sabotajes
        self.sabotage_cooldown_ms = 4000
        self.last_sabotage_ms = 0

    def update(self):
        if self.state == "WORKING":
            self._work_behavior()
        elif self.state == "WALKING":
            self._walk_behavior()
        elif self.state == "SUSPICIOUS":
            self._suspicious_behavior()

        self._check_state_transition()

    def _work_behavior(self):
        if random.random() < 0.01:
            self.state = "WALKING"

        if self.is_impostor and random.random() < 0.005:
            self.suspicion += 5

    def _walk_behavior(self):
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])

        if random.random() < 0.2:
            self.state = "WORKING"

    def _suspicious_behavior(self):
        self.suspicion += 2

    def _check_state_transition(self):
        if self.suspicion >= 50:
            self.state = "SUSPICIOUS"
        elif self.suspicion < 20 and self.state == "SUSPICIOUS":
            self.state = "WORKING"

    def sabotage(self):
        """
        Ejecuta un sabotaje con cooldown y probabilidad
        """
        if not self.is_impostor:
            return None

        now = pygame.time.get_ticks()

        # cooldown
        if now - self.last_sabotage_ms < self.sabotage_cooldown_ms:
            return None

        # probabilidad
        if random.random() > 0.15:
            return None

        self.last_sabotage_ms = now

        actions = [
            "disable_task",
            "trigger_event",
            "increase_global_suspicion"
        ]
        return random.choice(actions)
