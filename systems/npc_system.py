"""
Sistema de IA de NPCs.

Responsabilidad:
- Actualizar el comportamiento de los NPCs
- Cambiar estados (trabajo, sospecha, idle)
- Controlar NPC impostor
"""
class NPCSystem: 
    def update(self, npcs): 
        for npc in npcs: 
            npc.update() 