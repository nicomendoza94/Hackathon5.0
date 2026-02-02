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
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state_manager = StateManager()
        self.clock = Clock(60)
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.meeting = Meeting(self)
        # Sistemas
        self.input_system = InputSystem()
        self.movement_system = MovementSystem()
        self.interaction_system = InteractionSystem()
        self.npc_system = NPCSystem()
        self.task_system = TaskSystem()
        self.sabotage_system = SabotageSystem()
        # Entidades
        self.player = Player()
        self.npcs = load_npcs()
        self.tasks = load_tasks()
        def run(self):
            running = True
            while running:
                dt = self.clock.tick()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if self.state_manager.state == StateManager.MENU:
                    self.menu.update()
                    self.menu.draw(self.screen)
                elif self.state_manager.state == StateManager.PLAYING:
                    self.input_system.update(self.player)
                    self.movement_system.update(self.player, self.npcs)
                    self.npc_system.update(self.npcs)
                    self.task_system.update(self.player, self.tasks)
                    self.sabotage_system.update(self.player, self.npcs,  self.tasks)
                    self.screen.fill((0, 0, 0))
                    self.hud.draw(self.screen)
                    pygame.display.flip()
                elif self.state_manager.state == StateManager.MEETING:
                    self.meeting.update()
                    self.meeting.draw(self.screen)
                elif self.state_manager.state in (StateManager.GAME_OVER, StateManager.WIN):
                    self.menu.update()
                    self.menu.draw(self.screen)
            pygame.quit()

