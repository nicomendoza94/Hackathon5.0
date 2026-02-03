"""
Gestor de estados del juego.

Responsabilidad:
- Definir los estados (MENU, PLAYING, MEETING, GAME_OVER, WIN)
- Controlar transiciones entre estados
- Evitar lógica de juego dentro de los estados

Actúa como una máquina de estados simple.
"""
class StateManager():
    MENU = "MENU"
    PLAYING = "PLAYING"
    MEETING = "MEETING"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"

    def __init__(self):
        self.state = StateManager.MENU

    def set_state(self, new_state):
        self.state = new_state