"""
Punto de entrada del juego.

Responsabilidad:
- Inicializar pygame
- Crear la ventana principal
- Instanciar el objeto Game
- Ejecutar el loop principal

Este archivo NO debe contener lógica del juego.
"""

import json
from entities.npc import NPC

def load_npcs(path="data/npcs.json"):
    """
    Carga NPCs desde un archivo JSON
    :param path: ruta al JSON
    :return: lista de objetos NPC
    """
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