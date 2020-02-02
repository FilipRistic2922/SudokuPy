from gui_state.gui_state import GuiState


class StateManager:
    def __init__(self, win, states={}):
        self.win = win
        self.states = states
        self.current_state = None
        self.quit = False

    def add_state(self, state: GuiState):
        self.states[state.name] = state

    def set_initial_state(self, state_name: str):
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.on_start(self.win)

    def update(self, time):
        if self.current_state:

            if self.current_state.next_state:
                new_state = self.states[self.current_state.next_state]
                new_state.data_in = self.current_state.data_out
                self.current_state.next_state = None
                self.current_state.on_end()
                self.current_state = new_state
                self.current_state.on_start(self.win)

            self.current_state.update(self.win, time)

        self.quit = self.current_state.quit

