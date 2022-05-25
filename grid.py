from typing import Callable, Tuple
from cell import Cell, CellState


class Grid:

    def __init__(self, dimensions: Tuple[int, ...]) -> None:
        self.dimensions = dimensions
        self.cells: dict[Tuple[int, ...], Cell] = {}

    # If cell already exists in that location, replaces it (because dictionary)
    def add_cell_at(self, cell: Cell, location: Tuple[int]) -> None:
        assert len(location) == len(self.dimensions),\
            "Invalid dimensions for specified location"

        for i, zipped in enumerate(list(zip(location, self.dimensions))):
            l, d = zipped
            assert l >= 0 and l < d,\
                f"Location '{l}' of axis '{i}' is out of axis bounds ('0...{d}')"

        self.cells[location] = cell

    def get_cell_location(self, cell_to_locate: Cell):
        for location, cell in self.cells.items():
            if cell == cell_to_locate:
                return location

    def remove_cell_at(self, location) -> None:
        try: del self.cells[location]
        except KeyError: print("There are no cells in the specified location"); return

    def remove_cells_matching(self, query: Callable[[Cell], bool]) -> None:
        locations_to_remove_cells_at = []
        for cell_location in self.cells.keys():
            if query(self.cells[cell_location]):
                locations_to_remove_cells_at.append(cell_location)

        for location in locations_to_remove_cells_at:
            self.remove_cell_at(location)

    def remove_cells_like(self, cell_to_remove: Cell) -> None:
        self.remove_cells_matching(lambda cell: cell == cell_to_remove)

    def swap_cells(self, cell1: Cell, cell2: Cell) -> None:
        # Relies on the fact that add_cell_at replaces existing cells
        # If you ever remove this property of add_cell_at, you'll need to re-write this function
        self.add_cell_at(cell1, self.get_cell_location(cell2))
        self.add_cell_at(cell2, self.get_cell_location(cell1))

    def copy(self) -> 'Grid':
        grid_copy: Grid = Grid(dimensions=self.dimensions)
        for cell in self.cells.items():
            grid_copy.cells[cell[0]] = cell[1].copy()

        return grid_copy

    # TODO: To be implemented with proper GUI
    # TODO: Visualize based on number of dimensions, 1D, 2D, 3D, and any further could be CLIed or something
    # FIXME: Can't handle negative indices
    def visualize(self) -> None:
        # if self.dimensions > 2: print("Sorry, dimensions not supported"); return
        matrix = self.__matrix_populator()
        for cell_location in self.cells:
            self.__matrix_set_cell_at(matrix, cell_location, self.cells[cell_location].state.value)
        
        if len(self.dimensions) == 1:
            print(*matrix)
        
        if len(self.dimensions) == 2:
            for a in matrix:
                print(*a)
        
        if len(self.dimensions) == 3:
            for a in matrix:
                print(end=" | ")
                for b in a: print(*b, end=' | ')
                print()
        

    def __matrix_populator(self, current_dimension=0, matrix: list = None):
        if matrix is None: matrix = []  # Need to use "sentinel value" for default value assignment
        while len(matrix) < self.dimensions[current_dimension]:
            #
            # If you reach the deepeset dimension...
            if current_dimension == len(self.dimensions) - 1:
                matrix.extend([' ' for _ in range(self.dimensions[current_dimension])])
            #
            # Otherwise, you're in a shallower dimension, you need to go deeper!
            else:
                matrix.append(self.__matrix_populator(current_dimension + 1))

        return matrix

    def __matrix_set_cell_at(self, matrix, location, value):
        # reference copy of matrix
        matrix_cell = matrix
        # navigate to penultimate depth
        for index in location[:-1]: matrix_cell = matrix_cell[index]
        # update with ultimate depth index
        matrix_cell[location[-1]] = value
