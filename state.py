import copy
class state:
    def __init__(self,ID):
        self.ID = ID
        self.next_state = {}
        self.is_end = False

    def add_transition(self, st, symbol):
        if symbol not in self.next_state:
            self.next_state[symbol] = []
        self.next_state[symbol].append(st)

    def get_transition(self,key):
        if key not in self.next_state:
            return []
        return self.next_state[key]