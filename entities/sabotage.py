"""
Entidad Sabotage.

Responsabilidad:
- Representar sabotajes posibles del impostor
- Indicar si están activos o no
- Proveer efectos al sistema de sabotajes
"""
class Sabotage:
 def __init__(self, name, x, y, active=False):
    self.name = name
    self.x = x
    self.y = y
    self.active = active