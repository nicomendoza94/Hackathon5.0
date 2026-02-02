"""
Sistema de sabotajes.

Responsabilidad:
- Activar sabotajes del impostor
- Aplicar efectos negativos al juego
- Incrementar dificultad
"""

import random
from entities.sabotage import Sabotage

class SabotageSystem:
    def __init__(self):
        self.sabotages = [
            Sabotage("Luces apagadas", "lights", 10),
            Sabotage("Puertas bloqueadas", "doors", 8),
            Sabotage("Comunicaciones caídas", "comms", 12),
        ]

    def update(self, player, npcs, tasks):
        # Solo el impostor puede activar sabotajes
        if not player.is_impostor:
            return

        # Actualizar sabotajes activos
        for sabotage in self.sabotages:
            sabotage.update()

        # Activar uno nuevo si no hay activos
        if not any(s.active for s in self.sabotages):
            if random.random() < 0.01:  # probabilidad baja
                self.activate_random_sabotage()

        # Evento cómico aleatorio
        if random.random() < 0.005:
            self.random_fun_event()

        # Eventos comicos Aleatorios ###
    def random_fun_event(self):
        events = [
            " Un perro corre por la sala del congreso",
            " El micrófono empieza a chillar",
            " Un diputado derrama su café",
            " Suena un celular en plena sesión",]

        print(random.choice(events))

    def activate_random_sabotage(self):
        available = [s for s in self.sabotages if not s.active]
        if not available:
            return

        sabotage = random.choice(available)
        sabotage.activate()
        print(f"Sabotaje activado: {sabotage.name}")
