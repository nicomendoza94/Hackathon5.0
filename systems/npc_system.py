"""
Sistema de IA de NPCs.

Responsabilidad:
- Actualizar el comportamiento de los NPCs
- Cambiar estados (trabajo, sospecha, idle)
- Controlar NPC impostor
"""
class NPCSystem:
    def __init__(self, npcs):
        """
        Sistema que maneja todos los NPCs
        :param npcs: lista de objetos NPC
        """
        self.npcs = npcs

    def update(self, delta_time=1.0):
        """
        Actualiza todos los NPCs cada tick
        :param delta_time: tiempo transcurrido desde el último update
        """
        for npc in self.npcs:
            # Actualiza comportamiento individual
            npc.update()

            # Si el NPC es impostor, puede ejecutar un sabotaje
            if npc.is_impostor:
                sabotage_action = npc.sabotage()
                if sabotage_action:
                    self._handle_sabotage(npc, sabotage_action)

    def _handle_sabotage(self, npc, sabotage_type):
        """
        Maneja el efecto de un sabotaje
        Por ahora solo imprime la acción
        :param npc: NPC que ejecuta el sabotaje
        :param sabotage_type: tipo de sabotaje
        """
        print(f"[SABOTAGE] {npc.name} ejecuta {sabotage_type}")