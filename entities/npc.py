"""
Entidad NPC (diputados controlados por IA).

Responsabilidad:
- Representar NPCs ciudadanos o impostores
- Mantener su estado interno (trabajando, caminando, sospechoso)
- Ejecutar comportamientos simples controlados por sistemas
"""
import random 
 
class NPC: 
    def __init__(self, name, x, y): 
        self.name = name 
        self.x = x 
        self.y = y 
        self.state = "WALKING" 
        self.is_impostor = random.random() < 0.1 
 
    def update(self): 
        # IA simple 
        pass 
