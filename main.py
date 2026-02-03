"""
Punto de entrada del juego.

Responsabilidad:
- Inicializar pygame
- Crear la ventana principal
- Instanciar el objeto Game
- Ejecutar el loop principal

Este archivo NO debe contener lógica del juego.
"""
import pygame 
import json
from core.game import Game 
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE 
from entities.npc import NPC

def main(): 
    pygame.init() 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE) 
    game = Game(screen) 
    game.run() 
    pygame.quit() 
if __name__ == "__main__": 
    main() 

# ====================================
def load_npcs(path="data/npcs.json"):
 
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        NPC(
            npc_id=n["id"],
            name=n["name"],
            x=n["x"],
            y=n["y"],
            is_impostor=n["is_impostor"]
        )
        for n in data
    ]