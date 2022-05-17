from typing import Callable, Dict, Tuple
from cell import Cell


class Grid:

    def __init__(self, dimensions: int, initial_state: int) -> None:
        self.dimensions = dimensions
        self.initial_state = initial_state
        self.cells: Dict[(dimensions * int), Cell] = {}

    # If cell already exists in that location, replaces it (because dictionary)
    def add_cell_at(self, cell: Cell, location: Tuple[int]) -> None:
        assert len(location) == self.dimensions, "Invalid dimensions for specified location"

        if cell.state == None: cell.state = self.initial_state
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

    # TODO: To be implemented with proper GUI
    # FIXME: Can't handle negative indices
    def visualize(self) -> None:
        # if self.dimensions > 2: print("Sorry, dimensions not supported"); return
        size_per_dimension = []
        for locations_per_dimension in list(zip(*self.cells.keys())):
            size_per_dimension.append(max(locations_per_dimension) + 1)

        matrix = self.__matrix_populator(size_per_dimension)
        for cell_location in self.cells:
            self.__matrix_set_cell_at(matrix, cell_location, self.cells[cell_location].state)
        return matrix

    def __matrix_populator(self, size_per_dimension, current_dimension=0, matrix: list = None):
        if matrix is None: matrix = []  # Need to use "sentinel value" for default value assignment
        while len(matrix) < size_per_dimension[current_dimension]:
            #
            # If you reach the deepeset dimension...
            if current_dimension == self.dimensions - 1:
                matrix.extend([' ' for _ in range(size_per_dimension[current_dimension])])
            #
            # Otherwise, you're in a shallower dimension, you need to go deeper!
            else:
                matrix.append(self.__matrix_populator(size_per_dimension, current_dimension + 1))

        return matrix

    def __matrix_set_cell_at(self, matrix, location, value):
        # reference copy of matrix
        matrix_cell = matrix
        # navigate to penultimate depth
        for index in location[:-1]: matrix_cell = matrix_cell[index]
        # update with ultimate depth index
        matrix_cell[location[-1]] = value

    def __get_previous_locations(self, location: Tuple[int]):
        locations = []
        for i in range(self.dimensions):
            locations.append((*location[:i], location[i] - 1, *location[i + 1:]))

        return locations

    def __get_next_locations(self, location: Tuple[int]):
        locations = []
        for i in range(self.dimensions):
            locations.append((*location[:i], location[i] + 1, *location[i + 1:]))

        return locations

    def get_next_gen(self, rule) -> 'Grid':
        next_gen_grid = Grid(self.dimensions, self.initial_state)

        location_groups_to_check = []
        # for the location of each cell manually inserted (regardless of its state)
        for cell_location in self.cells.keys():
            # for its neighboring locations and itself (regardless of whether we inserted them or not)
            for location in [
                *self.__get_previous_locations(cell_location),
                cell_location,
                *self.__get_next_locations(cell_location),
            ]:
                # take ALL their neighbors into consideration
                location_groups_to_check.append([
                    *self.__get_previous_locations(location),
                    location,
                    *self.__get_next_locations(location),
                ])

        # If you try to access a location that doesn't exist, use initial_state value
        for location_group in location_groups_to_check:

            rule_digit = 0
            for location in location_group:
                rule_digit <<= 1
                try: rule_digit += self.cells[location].state
                except: rule_digit += self.initial_state

            next_gen_cell = Cell(int(rule[len(rule) - rule_digit - 1]))
            # supposedly we will only ever have odd-length location groups
            next_gen_cell_location = location_group[(len(location_group) - 1) // 2]
            next_gen_grid.add_cell_at(next_gen_cell, next_gen_cell_location)
        
        return next_gen_grid
