import random
import pygame

class NPCSystem:
    """
    NPCs single-player:

    - Si el JUGADOR es IMPOSTOR:
        * Los NPCs avanzan tareas automáticamente (sin minijuegos).
        * Progresan a un ritmo "prudencial" para ganar o perder con el timer.
        * No se amontonan: reservan estaciones.
        * No atraviesan paredes ni puertas cerradas.

    - Si el JUGADOR es DIPUTADO:
        * Los NPCs solo simulan actividad (caminar/esperar), NO completan tareas.
    """

    def __init__(self, npcs):
        self.npcs = npcs

        # npc_id -> Task (reservada)
        self._reserved_task = {}

        # npc_id -> (task, finish_ms)
        self._working = {}

        # Ajustes de balance (prudencial)
        self.max_workers = 2                 # cuantos NPC trabajan a la vez (clave)
        self.work_time_ms_range = (35000, 50000)  # 35s..50s por tarea (con 2 workers, 5 tareas => ~90-140s + caminata)

        # Movimiento
        self.npc_size = 36   # hitbox cuadrada del NPC
        self.base_speed = 0.9

    # ---------- helpers ----------
    def _npc_rect(self, x, y):
        half = self.npc_size // 2
        return pygame.Rect(int(x - half), int(y - half), self.npc_size, self.npc_size)

    def _collides(self, rect, walls, door_blocks, doors_locked):
        for w in walls:
            if rect.colliderect(w):
                return True
        if doors_locked:
            for d in door_blocks:
                if rect.colliderect(d):
                    return True
        return False

    def _pick_task_for(self, npc, tasks):
        pending = [t for t in tasks if not t.completed]
        if not pending:
            return None

        # evitar amontonarse: preferir no reservadas
        free = [t for t in pending if t not in self._reserved_task.values()]
        pool = free if free else pending

        pool.sort(key=lambda t: (t.x - npc.x) ** 2 + (t.y - npc.y) ** 2)
        return pool[0]

    def update(self, dt_ms, player, tasks, doors_locked, lights_out, walls=None, door_blocks=None):
        if not self.npcs:
            return {"stress_add": 0.0, "suspicion_add": 0.0, "meeting_requested": False}

        if walls is None:
            walls = []
        if door_blocks is None:
            door_blocks = []

        now = pygame.time.get_ticks()

        stress_add = 0.0
        suspicion_add = 0.0
        meeting_requested = False

        impostor_mode = bool(getattr(player, "is_impostor", False))

        # velocidad por luces
        speed = self.base_speed if not lights_out else self.base_speed * 0.5

        # contar "workers" activos
        active_workers = len(self._working)

        for i, npc in enumerate(self.npcs):
            # ==========================
            # 1) MOVIMIENTO / TARGET
            # ==========================
            # Si jugador es impostor: solo algunos NPC trabajan a la vez
            can_work = impostor_mode and (i in self._working or active_workers < self.max_workers)

            # Si está trabajando, no caminar
            if i in self._working:
                task, finish_ms = self._working[i]
                if now >= finish_ms:
                    # Completa la tarea al terminar
                    if not task.completed:
                        task.complete()

                    # liberar reserva y working
                    self._working.pop(i, None)
                    self._reserved_task.pop(i, None)
                    active_workers = len(self._working)
                else:
                    # quieto mientras trabaja
                    pass

            # Si no está trabajando, decide target
            if i not in self._working:
                # DIPUTADO: NPC solo “simula”
                if not impostor_mode:
                    # caminata simple random controlada
                    if random.random() < 0.08:
                        dx = random.choice([-1, 0, 1])
                        dy = random.choice([-1, 0, 1])
                        nx = npc.x + dx * 2
                        ny = npc.y + dy * 2
                        nrect = self._npc_rect(nx, ny)
                        if not self._collides(nrect, walls, door_blocks, doors_locked):
                            npc.x, npc.y = nx, ny

                # IMPOSTOR: NPC hace tareas (limitado por max_workers)
                else:
                    if can_work:
                        # asegurar reserva
                        if i not in self._reserved_task or self._reserved_task[i] is None or self._reserved_task[i].completed:
                            t = self._pick_task_for(npc, tasks)
                            if t is not None:
                                self._reserved_task[i] = t

                        t = self._reserved_task.get(i)
                        if t is not None and not t.completed:
                            tx, ty = t.x, t.y
                            dx = tx - npc.x
                            dy = ty - npc.y
                            dist = (dx * dx + dy * dy) ** 0.5

                            # moverse hacia la tarea
                            if dist > 16:
                                step = speed * (dt_ms / 16.0)
                                nx = npc.x + (dx / dist) * step
                                ny = npc.y + (dy / dist) * step

                                nrect = self._npc_rect(nx, ny)
                                if not self._collides(nrect, walls, door_blocks, doors_locked):
                                    npc.x, npc.y = nx, ny
                                else:
                                    # si choca, re-pick en otro tick
                                    if random.random() < 0.15:
                                        self._reserved_task.pop(i, None)

                            else:
                                # llegó: empieza “trabajo” con tiempo prudencial
                                if active_workers < self.max_workers:
                                    work_ms = random.randint(self.work_time_ms_range[0], self.work_time_ms_range[1])
                                    self._working[i] = (t, now + work_ms)
                                    active_workers = len(self._working)

            # ==========================
            # 2) EFECTOS en STRESS/SOSPECHA
            # ==========================
            if doors_locked:
                # si npc está cerca del pasillo central, sube stress
                if 240 < npc.y < 340:
                    stress_add += 0.35 * (dt_ms / 1000.0)

            # sospecha: si jugador impostor cerca (sirve si querés “tensión”)
            if impostor_mode:
                px, py = player.x, player.y
                ddx, ddy = (npc.x - px), (npc.y - py)
                pd = (ddx * ddx + ddy * ddy) ** 0.5
                if pd < 90:
                    npc.suspicion = min(100.0, npc.suspicion + 22.0 * (dt_ms / 1000.0))
                    suspicion_add += 6.0 * (dt_ms / 1000.0)
                    if npc.suspicion >= 95:
                        meeting_requested = True
                else:
                    npc.suspicion = max(0.0, npc.suspicion - 6.0 * (dt_ms / 1000.0))

        return {"stress_add": stress_add, "suspicion_add": suspicion_add, "meeting_requested": meeting_requested}
