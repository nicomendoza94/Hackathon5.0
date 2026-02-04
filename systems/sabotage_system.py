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

        # Timers fijos (lo que pediste)
        self.fun_interval_ms = 5000       # eventos graciosos cada 5s
        self.sabotage_interval_ms = 15000 # sabotajes cada 15s

        self.next_fun_ms = pygame.time.get_ticks() + self.fun_interval_ms
        self.next_sabotage_ms = pygame.time.get_ticks() + self.sabotage_interval_ms
        
        self.manual_cooldown_ms = 15000   # 15s entre sabotajes manuales
        self.last_manual_time = 0

        # Mensajes para UI
        self.ui_messages = []  # list[(text, expires_ms)]

        # Preferencia: puertas más que el resto
        # (si querés todavía más, subí el peso de "doors")
        self.weights = {
            "doors": 0.60,
            "lights": 0.25,
            "comms": 0.15,
        }

    def _push_ui(self, text, seconds=4.0):
        expires = pygame.time.get_ticks() + int(seconds * 1000)
        self.ui_messages.append((text, expires))

    def get_ui_messages(self):
        now = pygame.time.get_ticks()
        self.ui_messages = [(t, exp) for (t, exp) in self.ui_messages if exp > now]
        return [t for (t, exp) in self.ui_messages]

    def update(self, player, npcs, tasks):
        now = pygame.time.get_ticks()

        # Siempre actualizar timers de sabotajes activos
        for s in self.sabotages:
            s.update()

        # ¿Quién puede disparar sabotajes?
        # - Si el jugador ES impostor => él dispara
        # - Si el jugador NO es impostor => un NPC impostor dispara
        impostor_exists = False
        if player and getattr(player, "is_impostor", False):
            impostor_exists = True
        else:
            if npcs:
                impostor_exists = any(getattr(n, "is_impostor", False) for n in npcs)

        # Eventos graciosos fijos cada 5s (siempre)
        if now >= self.next_fun_ms:
            self.random_fun_event()
            self.next_fun_ms = now + self.fun_interval_ms

        # Sabotajes cada 15s (solo si existe impostor y no hay uno activo)
        if impostor_exists and now >= self.next_sabotage_ms:
            if not any(s.active for s in self.sabotages):
                self.activate_weighted_sabotage()
            self.next_sabotage_ms = now + self.sabotage_interval_ms

    def random_fun_event(self):
        events = [
            "Un celular suena en plena sesión 📱",
            "Se cae el termo y alguien grita '¡NDERA!' 🧉",
            "El micrófono hace acople y todos miran al técnico 🎤",
            "Aparece una bandeja de empanadas de la nada 🥟",
            "Se arma discusión por el aire acondicionado ❄️",
        ]
        self._push_ui(random.choice(events), seconds=5.0)

    def activate_weighted_sabotage(self):
        available = [s for s in self.sabotages if not s.active]
        if not available:
            return

        # elegir por peso (doors más probable)
        effects = [s.effect for s in available]
        weights = [self.weights.get(eff, 0.1) for eff in effects]

        chosen_effect = random.choices(effects, weights=weights, k=1)[0]
        chosen = next(s for s in available if s.effect == chosen_effect)

        chosen.activate()
        self._push_ui(f"Sabotaje activado: {chosen.name} ⚠️", seconds=6.0)

    def _activate(self, effect):
        # No permitir si ya hay un sabotaje activo
        if any(s.active for s in self.sabotages):
            self._push_ui("Ya hay un sabotaje activo ⛔", seconds=2.2)
            return False

        now = pygame.time.get_ticks()

        # Cooldown manual
        if now - self.last_manual_time < self.manual_cooldown_ms:
            remaining = int((self.manual_cooldown_ms - (now - self.last_manual_time)) / 1000)
            self._push_ui(f"Sabotaje en cooldown: {remaining}s ⏳", seconds=2.2)
            return False

        # Activar sabotaje
        for s in self.sabotages:
            if s.effect == effect:
                s.activate()
                self.last_manual_time = now
                self._push_ui(f"Sabotaje activado: {s.name} ⚠️", seconds=3.5)
                return True

        return False

            
    def manual_trigger(self, key):
        if key == pygame.K_1:
            self._activate("lights")

        elif key == pygame.K_2:
            self._activate("doors")

        elif key == pygame.K_3:
            self._activate("comms")



