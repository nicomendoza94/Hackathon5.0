class StateManager:
    MENU = "MENU"
    PLAYING = "PLAYING"
    MEETING = "MEETING"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"

    def __init__(self):
        self.state = StateManager.MENU

    def set_state(self, new_state):
        self.state = new_state