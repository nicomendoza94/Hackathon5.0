"""
Entidad NPC (diputados controlados por IA).

Responsabilidad:
- Representar NPCs ciudadanos o impostores
- Mantener su estado interno (trabajando, caminando, sospechoso)
- Ejecutar comportamientos simples controlados por sistemas
"""
import random 
 
class NPC: 
    #Definimos los posibles estados del NPC
    STATES = ("WORKING", "WALKING", "SUSPICIOUS")

    def __init__(self, name, x, y): 
        self.name = name 
        self.x = x 
        self.y = y 
        self.state = "WALKING" 
        self.is_impostor = random.random() < 0.1 
        self.suspicion = 0.0 
 
    def update(self): 
        """
        Actualiza el NPC en cada tick
        """
        # Elegimos qué comportamiento ejecutar según el estado actual
        if self.state == "WORKING":
            self._work_behavior()
        elif self.state == "WALKING":
            self._walk_behavior()
        elif self.state == "SUSPICIOUS":
            self._suspicious_behavior()

        # Comprobamos si debemos cambiar de estado según la sospecha
        self._check_state_transition()

    def _work_behavior(self):
        """
        Comportamiento cuando el NPC está trabajando
        """
        # Pequeña probabilidad de empezar a caminar
        if random.random() < 0.01:
            self.state = "WALKING"

        # Si es impostor, puede aumentar la sospecha de manera aleatoria
        if self.is_impostor and random.random() < 0.005:
            self.suspicion += 10  # aumenta nivel de sospecha

    def _walk_behavior(self):
        """
        Movimiento aleatorio del NPC
        """
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])

        # Probabilidad de volver a trabajar
        if random.random() < 0.2:
            self.state = "WORKING"

    def _suspicious_behavior(self):
        """
        Comportamiento cuando el NPC está en estado sospechoso
        """
        # Mientras está sospechoso, la sospecha sigue aumentando
        self.suspicion += 2

    def _check_state_transition(self):
        """
        Cambia el estado según el nivel de sospecha
        """
        if self.suspicion >= 50:
            self.state = "SUSPICIOUS"
        elif self.suspicion < 20 and self.state == "SUSPICIOUS":
            self.state = "WORKING"

    def sabotage(self):
        """
        Si el NPC es impostor, puede realizar un sabotaje aleatorio
        :return: acción de sabotaje o None si no hay sabotaje
        """
        if not self.is_impostor:
            return None

        actions = [
            "disable_task",            # ejemplo: deshabilitar una tarea
            "trigger_event",           # ejemplo: activar un evento
            "increase_global_suspicion" # ejemplo: aumentar sospecha general
        ]
        return random.choice(actions)
