
class CellState():
    def __init__(self, value) -> None:
        self.value = value


class Cell:

    def __init__(self, state: CellState) -> None:
        assert isinstance(state, CellState),\
            "Cell states must be of base class type CellState"
        self.state = state

    def copy(self) -> 'Cell':
        new_cell = Cell(self.state)
        return new_cell
