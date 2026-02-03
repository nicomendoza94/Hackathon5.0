"""
Entidad Sabotage.

Responsabilidad:
- Representar sabotajes posibles del impostor
- Indicar si están activos o no
- Proveer efectos al sistema de sabotajes
"""
import pygame


class Sabotage:
    def __init__(self, name, effect, duration_seconds, active=False):
        self.name = name
        self.effect = effect

        # ✅ duración real
        self.duration_ms = int(duration_seconds * 1000)

        self.active = active
        self.started_ms = 0

    def activate(self):
        self.active = True
        self.started_ms = pygame.time.get_ticks()

    def update(self):
        if not self.active:
            return

        now = pygame.time.get_ticks()
        if now - self.started_ms >= self.duration_ms:
            self.deactivate()

    def deactivate(self):
        self.active = False
        self.started_ms = 0
