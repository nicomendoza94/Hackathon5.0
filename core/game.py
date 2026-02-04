# core/game.py
import os
import random
import pygame

from core.state_manager import StateManager
from core.clock import Clock
from ui.menu import Menu
from ui.hud import HUD
from ui.meeting import Meeting

from entities.player import Player
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem
from systems.npc_system import NPCSystem
from systems.task_system import TaskSystem
from systems.sabotage_system import SabotageSystem

from data import load_npcs, load_tasks


def _safe_load_image(path, size=None, alpha=True):
    if not os.path.exists(path):
        return None
    try:
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except pygame.error:
        return None


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state_manager = StateManager()
        self.clock = Clock(60)

        # UI
        self.menu = Menu(screen)
        self.hud = HUD(screen)
        self.meeting = Meeting(screen)

        # Sistemas
        self.input_system = InputSystem()
        self.movement_system = MovementSystem()
        self.interaction_system = InteractionSystem()
        self.npc_system = NPCSystem([])
        self.task_system = TaskSystem()
        self.sabotage_system = SabotageSystem()

        # Entidades
        self.player = Player()
        self.npcs = load_npcs()
        self.tasks = load_tasks()
        self.npc_system.npcs = self.npcs

        self.player.total_tasks = len(self.tasks)

        self.timer_seconds = 300.0
        self.score = 0

        self.stress = 0.0
        self.suspicion = 0.0

        self.lights_out = False
        self.doors_locked = False

        # ----------------------------
        # MAPA OPEN/CLOSED
        # ----------------------------
        w, h = self.screen.get_width(), self.screen.get_height()

        self.map_open = _safe_load_image("assets/images/map_open.png", size=(w, h), alpha=False)
        self.map_closed = _safe_load_image("assets/images/map_closed.png", size=(w, h), alpha=False)

        if self.map_open is None:
            print("⚠️ map_open.png no encontrada o inválida. Revisá formato/ubicación.")
            self.map_open = pygame.Surface((w, h))
            self.map_open.fill((40, 40, 45))

        if self.map_closed is None:
            print("⚠️ map_closed.png no encontrada o inválida. Usando map_open como reemplazo.")
            self.map_closed = self.map_open.copy()

        self.bg = self.map_open

        # Sprites
        # ✅ si querés aún más grande, subí a (80,80) o (96,96)
        # self.player_sprite = _safe_load_image("assets/images/player.png", size=(80, 80), alpha=True)
        self.player_sprite = _safe_load_image("assets/images/personaje_solo.png", size=(80, 80), alpha=True)
        # self.npc_sprite = _safe_load_image("assets/images/npc.png", size=(80, 80), alpha=True)
        # self.npc_sprite = _safe_load_image("assets/images/npc_1.png", size=(80, 80), alpha=True)
        self.npc_sprite = {
            "npc_1":_safe_load_image("assets/images/npc_1.png", size=(80, 80), alpha=True)
            ,"npc_2":_safe_load_image("assets/images/npc_2.png", size=(80, 80), alpha=True)
            ,"npc_3":_safe_load_image("assets/images/npc_3.png", size=(80, 80), alpha=True)
            ,"npc_4":_safe_load_image("assets/images/npc_4.png", size=(80, 80), alpha=True)
            ,"npc_5":_safe_load_image("assets/images/npc_5.png", size=(80, 80), alpha=True)
        }

        self.font_hint = pygame.font.SysFont("Verdana", 20, bold=True)

        # ============================================================
        # WALLS + DOORS
        # ============================================================
        wall_y, wall_h = 308, 22

        left_gap_x = 90
        gap_w = 160
        right_gap_x = 1030

        self.walls = [
            pygame.Rect(0, wall_y, left_gap_x, wall_h),
            pygame.Rect(left_gap_x + gap_w, wall_y, right_gap_x - (left_gap_x + gap_w), wall_h),
            pygame.Rect(right_gap_x + gap_w, wall_y, 1280 - (right_gap_x + gap_w), wall_h),

            pygame.Rect(0, 0, 1280, 8),
            pygame.Rect(0, 712, 1280, 8),
            pygame.Rect(0, 0, 8, 720),
            pygame.Rect(1272, 0, 8, 720),
        ]

        pad_y = 6
        self.door_blocks = [
            pygame.Rect(left_gap_x, wall_y - pad_y, gap_w, wall_h + pad_y * 2),
            pygame.Rect(right_gap_x, wall_y - pad_y, gap_w, wall_h + pad_y * 2),
        ]

        self.safe_spawns = [
            (640, 560),
            (160, 140),
            (1120, 140),
            (160, 640),
            (1120, 640),
        ]

        self._assign_random_impostor()
        self._spawn_player_safely()

        self.debug_colliders = False

    def _assign_random_impostor(self):
        self.player.is_impostor = False
        self.player.role = "Diputado"
        for npc in self.npcs:
            npc.is_impostor = False

        pick = random.choice(["player"] + list(range(len(self.npcs))))
        if pick == "player":
            self.player.is_impostor = True
            self.player.role = "Impostor"
        else:
            self.npcs[pick].is_impostor = True
            self.player.is_impostor = False
            self.player.role = "Diputado"

    def _collides_world(self, rect):
        for w in self.walls:
            if rect.colliderect(w):
                return True
        if self.doors_locked:
            for d in self.door_blocks:
                if rect.colliderect(d):
                    return True
        return False

    def _spawn_player_safely(self):
        for x, y in self.safe_spawns:
            self.player.x, self.player.y = x, y
            self.player.update_rect()
            if not self._collides_world(self.player.rect):
                return
        self.player.x, self.player.y = 640, 360
        self.player.update_rect()

    def _reset_match(self, skip_role_roll=False):
        self.timer_seconds = 300.0
        self.score = 0
        self.stress = 0.0
        self.suspicion = 0.0

        for t in self.tasks:
            t.completed = False
            t.active = False

        self.player.total_tasks = len(self.tasks)
        self.player.tasks_completed = 0

        for npc in self.npcs:
            npc.suspicion = 0.0

        # 👇 CLAVE: solo asigna roles si NO venís del menú
        if not skip_role_roll:
            self._assign_random_impostor()

        self._spawn_player_safely()

        self.doors_locked = False
        self.bg = self.map_open


    # ✅ pantalla final
    def _draw_end_screen(self, win):
        self.screen.fill((10, 10, 15))
        font_big = pygame.font.SysFont("Verdana", 56, bold=True)
        font_small = pygame.font.SysFont("Verdana", 28, bold=True)

        title = "GANASTE 🎉" if win else "PERDISTE 💀"
        subtitle = "Presioná ESPACIO para volver al menú"

        t = font_big.render(title, True, (0, 220, 0) if win else (220, 60, 60))
        s = font_small.render(subtitle, True, (200, 200, 200))

        self.screen.blit(t, (640 - t.get_width() // 2, 260))
        self.screen.blit(s, (640 - s.get_width() // 2, 340))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick()

            for event in pygame.event.get():
                # Cerrar ventana
                if event.type == pygame.QUIT:
                    running = False

                # ✅ ESC: volver al menú desde cualquier pantalla (PRIORIDAD GLOBAL)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state_manager.set_state(StateManager.MENU)
                    continue  # importante: no seguir procesando este evento

                # Manejo por estado
                if self.state_manager.state == StateManager.MENU:
                    self._handle_menu_events(event)

                elif self.state_manager.state == StateManager.PLAYING:
                    self._handle_playing_events(event)

                elif self.state_manager.state == StateManager.MEETING:
                    self._handle_meeting_events(event)

                elif self.state_manager.state in (StateManager.WIN, StateManager.GAME_OVER):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.state_manager.set_state(StateManager.MENU)

            # Dibujo según estado
            if self.state_manager.state == StateManager.MENU:
                self.menu.draw()

            elif self.state_manager.state == StateManager.PLAYING:
                self._update_playing(dt)
                self._draw_playing()

            elif self.state_manager.state == StateManager.MEETING:
                info = [
                    "Reunión de emergencia (single player).",
                    "No hay voto: gestionás el caos.",
                ]
                self.meeting.draw(self.stress, self.suspicion, self.timer_seconds, info)

            elif self.state_manager.state == StateManager.WIN:
                self._draw_end_screen(True)

            elif self.state_manager.state == StateManager.GAME_OVER:
                self._draw_end_screen(False)

            pygame.display.flip()

        pygame.quit()



    def _handle_menu_events(self, event):
        if event.type != pygame.KEYDOWN:
            return

        # Elegir rol en menú
        if event.key == pygame.K_1:
            self.menu.selected_role = "Diputado"
            return

        if event.key == pygame.K_2:
            self.menu.selected_role = "Impostor"
            return

        # Iniciar partida
        if event.key == pygame.K_SPACE:
            # aplicar rol elegido (si no eligió, default Diputado)
            chosen = self.menu.selected_role or "Diputado"
            self.player.role = chosen
            self.player.is_impostor = (chosen == "Impostor")

            # si arrancás como Diputado, elegimos un NPC impostor
            if not self.player.is_impostor and self.npcs:
                for npc in self.npcs:
                    npc.is_impostor = False
                random.choice(self.npcs).is_impostor = True

            self._reset_match(skip_role_roll=True)
            self.state_manager.set_state(StateManager.PLAYING)



    def _handle_playing_events(self, event):
        # Eventos del minijuego
        if self.task_system.minigame_active:
            completed = self.task_system.handle_minigame_event(event)
            if completed:
                self.player.complete_task()
                self.score += 100
                self.stress = max(0.0, self.stress - 10.0)

        if event.type == pygame.KEYDOWN:

            # ==========================
            # SABOTAJES MANUALES (IMPOSTOR)
            # ==========================
            if self.player.is_impostor:
                self.sabotage_system.manual_trigger(event.key)

            # ==========================
            # INTERACCIÓN CON TAREAS
            # ==========================
            if event.key == pygame.K_e and not self.task_system.minigame_active:

                # 🚫 IMPOSTOR NO HACE TAREAS
                if self.player.is_impostor:
                    if hasattr(self.sabotage_system, "_push_ui"):
                        self.sabotage_system._push_ui(
                            "Sos IMPOSTOR: no hacés tareas. Saboteá (1/2/3).",
                            seconds=3.8
                        )
                    return  # 👈 CLAVE: corta acá

                # 📵 COMMS CAÍDAS (solo diputado)
                if getattr(self, "comms_down", False):
                    if hasattr(self.sabotage_system, "_push_ui"):
                        self.sabotage_system._push_ui(
                            "COMMS CAÍDAS: no podés iniciar tareas ahora 📵",
                            seconds=4.5
                        )
                else:
                    self.task_system.try_start_task(self.player, self.tasks)


            # ==========================
            # CANCELAR MINIJUEGO
            # ==========================
            if event.key == pygame.K_ESCAPE and self.task_system.minigame_active:
                self.task_system.cancel_minigame()

            # ==========================
            # REUNIÓN
            # ==========================
            if event.key == pygame.K_m and not self.task_system.minigame_active:
                self.state_manager.set_state(StateManager.MEETING)

            # ==========================
            # DEBUG
            # ==========================
            if event.key == pygame.K_F3:
                self.debug_colliders = not self.debug_colliders


    def _handle_meeting_events(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_1:
            for s in self.sabotage_system.sabotages:
                s.deactivate()

            self.stress = max(0.0, self.stress - 25.0)
            self.timer_seconds = max(0.0, self.timer_seconds - 30.0)
            self.state_manager.set_state(StateManager.PLAYING)
            return

        if event.key == pygame.K_ESCAPE:
            self.state_manager.set_state(StateManager.PLAYING)

    def _update_playing(self, dt):
        self.timer_seconds -= dt / 1000.0
        if self.timer_seconds <= 0:
            self.timer_seconds = 0

            if (not self.player.is_impostor) and self.player.tasks_completed >= self.player.total_tasks:
                self.state_manager.set_state(StateManager.WIN)
            else:
                if self.player.is_impostor and self.player.tasks_completed < self.player.total_tasks:
                    self.state_manager.set_state(StateManager.WIN)
                else:
                    self.state_manager.set_state(StateManager.GAME_OVER)
            return

        self.sabotage_system.update(self.player, self.npcs, self.tasks)

        self.lights_out = any(s.active and s.effect == "lights" for s in self.sabotage_system.sabotages)
        self.doors_locked = any(s.active and s.effect == "doors" for s in self.sabotage_system.sabotages)
        self.comms_down = any(s.active and s.effect == "comms" for s in self.sabotage_system.sabotages)
        
        # --- SOSPECHA TAMBIÉN PARA DIPUTADO (gestión single player) ---
        dt_s = dt / 1000.0

        if not self.player.is_impostor:
            # Si hay caos (sabotajes), sube sospecha global un poco
            if self.doors_locked:
                self.suspicion += 0.35 * dt_s
            if self.lights_out:
                self.suspicion += 0.25 * dt_s
            if getattr(self, "comms_down", False):
                self.suspicion += 0.55 * dt_s

        self.bg = self.map_closed if self.doors_locked else self.map_open

        active_count = sum(1 for s in self.sabotage_system.sabotages if s.active)
        self.stress += (active_count * 1.6) * (dt / 1000.0)
        if self.doors_locked:
            self.stress += 0.9 * (dt / 1000.0)
        if self.lights_out:
            self.stress += 0.6 * (dt / 1000.0)

        npc_effects = self.npc_system.update(
            dt, self.player, self.tasks,
            self.doors_locked, self.lights_out,
            walls=self.walls,
            door_blocks=self.door_blocks
)


        self.stress += npc_effects.get("stress_add", 0.0)
        self.suspicion += npc_effects.get("suspicion_add", 0.0)

        if self.player.is_impostor and npc_effects.get("meeting_requested", False):
            # reunión automática (no pantalla)
            self.stress = min(100.0, self.stress + 8.0)

            if hasattr(self.sabotage_system, "_push_ui"):
                self.sabotage_system._push_ui(
                    "Reunión automática: te miran raro 👀 (+estrés)",
                    seconds=4.5
                )



        if not self.player.is_impostor:
            self.suspicion = max(0.0, self.suspicion - 2.5 * (dt / 1000.0))

        else:
            self.suspicion = max(0.0, self.suspicion - 3.0 * (dt / 1000.0))

        self.stress = max(0.0, min(100.0, self.stress))
        self.suspicion = max(0.0, min(100.0, self.suspicion))

        if self.stress >= 100.0:
            self.state_manager.set_state(StateManager.WIN if self.player.is_impostor else StateManager.GAME_OVER)
            return

        if self.suspicion >= 100.0:
            self.state_manager.set_state(StateManager.GAME_OVER if self.player.is_impostor else StateManager.WIN)
            return

        if not self.task_system.minigame_active:
            prev_x, prev_y = self.player.x, self.player.y
            prev_rect = self.player.rect.copy()

            self.input_system.update(self.player)
            self.movement_system.update(self.player, self.npcs)

            if self._collides_world(self.player.rect):
                self.player.x, self.player.y = prev_x, prev_y
                self.player.rect = prev_rect

        completed_from_update = self.task_system.update_minigame()
        if completed_from_update:
            self.player.complete_task()
            self.score += 100
            self.stress = max(0.0, self.stress - 10.0)

        self.task_system.update(self.player, self.tasks)

        # -----------------------------
        # CONDICIONES WIN/LOSE IMPOSTOR
        # -----------------------------
        if self.player.is_impostor:
            # si los NPC completaron todas las tareas -> vos perdés
            if all(t.completed for t in self.tasks):
                self.state_manager.set_state(StateManager.GAME_OVER)
                return

        # WIN diputado por tareas (solo el jugador)
        if (not self.player.is_impostor) and self.player.tasks_completed >= self.player.total_tasks:
            self.state_manager.set_state(StateManager.WIN)
            return


    def _draw_playing(self):
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((40, 40, 45))

        # NPCs
        for i in range(len(self.npcs)):
            cur = self.npcs[i]
            if self.npc_sprite[f"npc_{i+1}"]:
                sw = self.npc_sprite[f"npc_{i+1}"].get_width()
                sh = self.npc_sprite[f"npc_{i+1}"].get_height()
                self.screen.blit(self.npc_sprite[f"npc_{i+1}"], (int(cur.x - sw // 2), int(cur.y - sh // 2)))

            else:
                pygame.draw.circle(self.screen, (0, 140, 255), (int(cur.x), int(cur.y)), 16)

            bar_w, bar_h = 40, 6
            x = int(cur.x) - bar_w // 2
            y = int(cur.y) - 30
            pygame.draw.rect(self.screen, (30, 30, 30), (x, y, bar_w, bar_h))
            fill = int(bar_w * (max(0.0, min(100.0, getattr(cur, "suspicion", 0.0))) / 100.0))
            pygame.draw.rect(self.screen, (255, 80, 80), (x, y, fill, bar_h))

        # ✅ Player (centrado siempre, no hardcode)
        if self.player_sprite:
            sw = self.player_sprite.get_width()
            sh = self.player_sprite.get_height()
            self.screen.blit(self.player_sprite, (int(self.player.x - sw // 2), int(self.player.y - sh // 2)))
        else:
            pygame.draw.circle(self.screen, (0, 255, 0), (int(self.player.x), int(self.player.y)), 18)

        # Hint
        near_task = self.interaction_system.check_task_interaction(self.player, self.tasks)
        if near_task and not self.task_system.minigame_active and not near_task.completed:
            hint = self.font_hint.render("Presioná E para hacer tarea", True, (255, 255, 255))
            shadow = self.font_hint.render("Presioná E para hacer tarea", True, (0, 0, 0))
            hx = int(self.player.x) - hint.get_width() // 2
            hy = int(self.player.y) - 70
            self.screen.blit(shadow, (hx + 2, hy + 2))
            self.screen.blit(hint, (hx, hy))

        # HUD
        pending = [t for t in self.tasks if not t.completed]

        if getattr(self, "comms_down", False):
            hud_task = "COMMS CAÍDAS: SIN INFORMACIÓN DE TAREAS"
            task_progress = 0.0
        else:
            current_task = self.task_system.current_task.name if self.task_system.current_task else "Buscar estación"
            hud_task = f"{current_task} | Pendientes: {len(pending)}/{len(self.tasks)}"
            task_progress = self.player.get_task_progress()

        self.hud.draw(
            player_role=("Impostor" if self.player.is_impostor else "Diputado"),
            task_progress=task_progress,
            timer_seconds=self.timer_seconds,
            score=self.score,
            current_task_name=hud_task,
            stress=self.stress,
            suspicion=self.suspicion,
        )


        # ✅ MENSAJES tipo BANNER (arriba centrado)
        msgs = self.sabotage_system.get_ui_messages() if hasattr(self.sabotage_system, "get_ui_messages") else []
        if msgs:
            font_msg = pygame.font.SysFont("Verdana", 22, bold=True)
            y = 90
            for msg in msgs[-2:]:
                surf = font_msg.render(msg, True, (255, 255, 255))
                shadow = font_msg.render(msg, True, (0, 0, 0))
                x = self.screen.get_width() // 2 - surf.get_width() // 2
                self.screen.blit(shadow, (x + 2, y + 2))
                self.screen.blit(surf, (x, y))
                y += 34

        # Luces apagadas
        if self.lights_out:
            dark = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            dark.fill((0, 0, 0, 170))
            self.screen.blit(dark, (0, 0))

            font = pygame.font.SysFont("Verdana", 26, bold=True)
            msg = font.render("SABOTAJE: LUCES APAGADAS", True, (255, 90, 90))
            self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 140))

        # DEBUG colisiones (F3)
        if self.debug_colliders:
            for r in self.walls:
                pygame.draw.rect(self.screen, (255, 0, 0), r, 1)

            if self.doors_locked:
                for r in self.door_blocks:
                    pygame.draw.rect(self.screen, (0, 255, 0), r, 2)
            else:
                for r in self.door_blocks:
                    pygame.draw.rect(self.screen, (0, 180, 0), r, 1)

        # Minijuego
        if self.task_system.minigame_active:
            self.task_system.draw_minigame(self.screen)
