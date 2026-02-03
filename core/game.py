"""
Clase principal Game.

Responsabilidad:
- Orquestar todo el juego
- Inicializar sistemas y entidades
- Ejecutar el loop principal
- Delegar lógica según el estado actual del juego

Este archivo conecta todos los sistemas.
"""
import pygame
import sys
import json
import os
import random

from core.state_manager import StateManager
from entities.player import Player
from ui.menu import Menu
from ui.hud import HUD
from ui.meeting import Meeting

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TIME, TITLE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # Core
        self.state_manager = StateManager()
        self.running = True

        # UI
        self.menu = Menu(self.screen)
        self.hud = HUD(self.screen)
        self.meeting = Meeting(self.screen)

        # Entities
        self.player = Player(name="Player")

        # Data
        self.npcs_base = self.load_json("data/npcs.json")
        tasks_data = self.load_json("data/tasks.json")
        self.tasks = tasks_data.get("tasks", [])
        self.sabotages = tasks_data.get("sabotages", [])

        # Runtime
        self.reset_game_data()

    # ----------------------------
    # Utility / Data
    # ----------------------------
    def load_json(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_score(self, victory):
        path = "data/scores.json"
        data = self.load_json(path)

        if not data or not isinstance(data, dict):
            data = {"high_scores": [], "total_games_played": 0}

        entry = {
            "player": self.player.name,
            "points": self.player.get_score(),
            "date": "2026-02-03",
            "role": self.player.role,
            "victory": victory,
            "level_reached": 1
        }

        data["high_scores"].append(entry)
        data["total_games_played"] += 1
        data["high_scores"] = sorted(
            data["high_scores"],
            key=lambda x: x["points"],
            reverse=True
        )[:10]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # ----------------------------
    # Game lifecycle
    # ----------------------------
    def reset_game_data(self):
        self.timer = GAME_TIME
        self.npcs = []
        self.selected_npc_idx = 0
        self.player.reset()

    def start_game(self):
        self.reset_game_data()
        self.assign_roles()
        self.state_manager.set_state(StateManager.PLAYING)

    def end_game(self, victory):
        self.save_score(victory)
        self.state_manager.set_state(
            StateManager.WIN if victory else StateManager.GAME_OVER
        )

    def assign_roles(self):
        self.npcs = [dict(npc) for npc in self.npcs_base]
        for npc in self.npcs:
            npc["is_impostor"] = False

        if random.randint(1, 100) <= 30:
            self.player.set_role(Player.IMPOSTOR)
        else:
            self.player.set_role(Player.CIUDADANO)
            if self.npcs:
                random.choice(self.npcs)["is_impostor"] = True

    # ----------------------------
    # Main Loop
    # ----------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    # ----------------------------
    # Event handling
    # ----------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            state = self.state_manager.state

            if state == StateManager.MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_game()

            elif state == StateManager.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state_manager.set_state(StateManager.MENU)
                    elif event.key == pygame.K_e:
                        self.player.interact_with_task(self.tasks)

            elif state == StateManager.MEETING:
                self.meeting.handle_event(event)

            elif state in (StateManager.GAME_OVER, StateManager.WIN):
                if event.type == pygame.KEYDOWN:
                    self.state_manager.set_state(StateManager.MENU)

    # ----------------------------
    # Update logic
    # ----------------------------
    def update(self, dt):
        state = self.state_manager.state

        if state == StateManager.PLAYING:
            self.update_playing(dt)

        elif state == StateManager.MEETING:
            self.update_meeting()

    def update_playing(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.end_game(victory=False)
            return

        # Trigger de reunión (ejemplo simple)
        if int(self.timer) % 60 == 0 and int(self.timer) != GAME_TIME:
            self.state_manager.set_state(StateManager.MEETING)

    def update_meeting(self):
        if self.meeting.vote_done:
            voted_npc = self.npcs[self.meeting.selected_npc_idx]
            self.end_game(victory=voted_npc.get("is_impostor", False))

    # ----------------------------
    # Rendering
    # ----------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        state = self.state_manager.state

        if state == StateManager.MENU:
            self.menu.draw()

        elif state == StateManager.PLAYING:
            self.hud.draw(
                self.player.role,
                self.player.get_task_progress(),
                int(self.timer),
                self.player.get_score(),
                self.player.get_current_task_label(self.tasks),
                self.sabotages
            )

        elif state == StateManager.MEETING:
            self.meeting.draw(self.npcs, self.selected_npc_idx)

        elif state == StateManager.GAME_OVER:
            self.menu.draw_game_over()

        elif state == StateManager.WIN:
            self.menu.draw_win()

        pygame.display.flip()
