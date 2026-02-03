import random
import pygame

class NPCSystem:
    """
    NPCs single-player:
    - Caminan hacia estaciones (tareas no completadas) para “simular” actividad.
    - Reaccionan a sabotajes:
        * doors_locked: se quedan esperando en pasillo -> sube estrés
        * lights_out: se mueven más lento
    - Si el jugador es impostor y está cerca, sube sospecha del NPC y sospecha global.
    """

    def __init__(self, npcs):
        self.npcs = npcs
        self._targets = {}  # npc_id -> (x,y)
        self._wait_timer = {}  # npc_id -> ms

    def _pick_target_for(self, npc, tasks):
        pending = [t for t in tasks if not t.completed]
        if not pending:
            return None
        # target cercano
        pending.sort(key=lambda t: (t.x - npc.x) ** 2 + (t.y - npc.y) ** 2)
        t = pending[0]
        return (t.x, t.y)

    def update(self, dt_ms, player, tasks, doors_locked, lights_out):
        if not self.npcs:
            return {"stress_add": 0.0, "suspicion_add": 0.0, "meeting_requested": False}

        now = pygame.time.get_ticks()
        stress_add = 0.0
        suspicion_add = 0.0
        meeting_requested = False

        # velocidad base NPC
        base_speed = 0.9 if not lights_out else 0.45

        for i, npc in enumerate(self.npcs):
            # inicializar target
            if i not in self._targets or self._targets[i] is None or random.random() < 0.01:
                self._targets[i] = self._pick_target_for(npc, tasks)

            tgt = self._targets.get(i)
            if tgt:
                tx, ty = tgt
                dx, dy = (tx - npc.x), (ty - npc.y)
                dist = (dx * dx + dy * dy) ** 0.5

                # Si llega “a la estación”, se queda un rato (trabajando)
                if dist < 18:
                    # espera corta simulando trabajo
                    if i not in self._wait_timer or now > self._wait_timer[i]:
                        self._wait_timer[i] = now + random.randint(900, 1700)
                    else:
                        # mientras “trabaja”, baja un poquito el estrés (si sos diputado)
                        pass
                else:
                    # Si está esperando (trabajando), no se mueve
                    if i in self._wait_timer and now < self._wait_timer[i]:
                        pass
                    else:
                        # movimiento simple hacia target
                        step = base_speed * (dt_ms / 16.0)
                        npc.x += (dx / dist) * step
                        npc.y += (dy / dist) * step

            # si hay puertas bloqueadas, chance de “quedarse trabado” cerca del pasillo
            if doors_locked:
                # si npc está cerca del centro (donde suelen estar pasillos), sube estrés
                if 240 < npc.y < 330:
                    stress_add += 0.35 * (dt_ms / 1000.0)

            # sospecha: si jugador impostor cerca
            if getattr(player, "is_impostor", False):
                px, py = player.x, player.y
                ddx, ddy = (npc.x - px), (npc.y - py)
                pd = (ddx * ddx + ddy * ddy) ** 0.5

                if pd < 90:
                    npc.suspicion = min(100.0, npc.suspicion + 22.0 * (dt_ms / 1000.0))
                    suspicion_add += 8.0 * (dt_ms / 1000.0)
                else:
                    npc.suspicion = max(0.0, npc.suspicion - 6.0 * (dt_ms / 1000.0))

                # Si un NPC llega a sospecha alta, “pide reunión”
                if npc.suspicion >= 95:
                    meeting_requested = True

        return {"stress_add": stress_add, "suspicion_add": suspicion_add, "meeting_requested": meeting_requested}
