class Cell:
    
    def __init__(self, state=None) -> None:
        self.state = state

    def copy(self) -> 'Cell':
        new_cell = Cell(self.state)
        return new_cell