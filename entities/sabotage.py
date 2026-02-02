"""
Entidad Sabotage.

Responsabilidad:
- Representar sabotajes posibles del impostor
- Indicar si están activos o no
- Proveer efectos al sistema de sabotajes
"""
class Sabotage:
    def __init__(self, name, effect, duration, active=False):
        self.name = name              # Nombre del sabotaje
        self.effect = effect          # Qué afecta (luces, puertas, etc.)
        self.duration = duration      # Cuánto dura
        self.active = active          # Está activo o no
        self.timer = 0                # Contador interno

    def activate(self):
        self.active = True
        self.timer = self.duration

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.deactivate()

    def deactivate(self):
        self.active = False
        self.timer = 0