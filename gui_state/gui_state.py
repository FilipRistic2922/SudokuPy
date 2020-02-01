
class GuiState:
    def __init__(self, name,  state_manager):
        self.name = name
        self.data_in = {}
        self.data_out = {}
        self.state_manager = state_manager
        self.next_state = None
        self.quit = False
        self.state_manager.add_state(self)

    def change_state(self, new_state: str, data: map):
        self.next_state = new_state
        self.data_out = data

    def on_start(self, win):
        pass

    def on_end(self):
        pass

    def update(self, win, time_delta):
        pass
