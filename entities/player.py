"""
Entidad Player (jugador).

Responsabilidades:
- Mantener el estado del jugador
- Gestionar progreso de tareas
- Gestionar score y rol
- Exponer acciones de gameplay (interactuar, resetear)
"""

class Player:
    CIUDADANO = "Ciudadano"
    IMPOSTOR = "Impostor"

    def __init__(self, name="Player"):
        self.name = name
        self.reset()

    # ----------------------------
    # Lifecycle
    # ----------------------------
    def reset(self):
        self.role = Player.CIUDADANO
        self.score = 0
        self.task_progress = 0.0
        self.current_task_idx = 0

    def set_role(self, role):
        self.role = role

    # ----------------------------
    # Tasks / Gameplay
    # ----------------------------
    def can_do_tasks(self):
        return self.role == Player.CIUDADANO

    def interact_with_task(self, tasks):
        """
        Avanza el progreso de la tarea actual.
        Devuelve True si la tarea fue completada.
        """
        if not self.can_do_tasks():
            return False

        if not tasks:
            return False

        self.task_progress += 0.25

        if self.task_progress >= 1.0:
            self.task_progress = 0.0
            self.complete_task(tasks)
            return True

        return False

    def complete_task(self, tasks):
        task = tasks[self.current_task_idx]
        self.score += task.get("value", 10)
        self.current_task_idx = (self.current_task_idx + 1) % len(tasks)

    # ----------------------------
    # Getters (para UI / Game)
    # ----------------------------
    def get_score(self):
        return self.score

    def get_task_progress(self):
        return self.task_progress

    def get_current_task_label(self, tasks):
        if not tasks or not self.can_do_tasks():
            return ""
        return tasks[self.current_task_idx].get("label", "")
