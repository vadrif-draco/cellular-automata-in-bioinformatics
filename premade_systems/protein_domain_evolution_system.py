from typing import Dict
from grid import Grid
from cell import Cell, CellState
import random

ALLOWED_DIMENSIONALITIES = [1]
INITIAL_CELL_STATE = CellState("Φ") # XXX: y no use?

F2B = {
    'X': {
        'X': 0.1,
        'Y': 0.6,
        'Z': 0.4
    },
    'Y': {
        'X': 0.6,
        'Y': 0.3,
        'Z': 0.7
    },
    'Z': {
        'X': 0.2,
        'Y': 0.1,
        'Z': 0.3
    }
}

B2F = {
    'X': {
        'X': 0.1,
        'Y': 0.3,
        'Z': 0.2
    },
    'Y': {
        'X': 0.6,
        'Y': 0.3,
        'Z': 0.1
    },
    'Z': {
        'X': 0.4,
        'Y': 0.7,
        'Z': 0.3
    }
}

def tf(*tfargs) -> Grid:

    prev_gen_grid: Grid = tfargs[0]
    f2b: Dict[str, Dict[str, float]] = tfargs[1][0]
    b2f: Dict[str, Dict[str, float]] = tfargs[1][1]

    next_gen_grid: Grid = prev_gen_grid.copy()

    left = min(prev_gen_grid.cells.keys(), key=lambda key : key[0])
    right = max(prev_gen_grid.cells.keys(), key=lambda key : key[0])

    # TODO: If we reach start, stop
    if left[0] > 0:
        prev_gen_left_cell = prev_gen_grid.cells[left]
        next_gen_left_cell = __roulette_select_cell(f2b[prev_gen_left_cell.state.value])
        next_gen_grid.add_cell_at(next_gen_left_cell, ((left[0] - 1),))

    # TODO: If we reach end, stop
    if right[0] < prev_gen_grid.dimensions[0] - 1:
        prev_gen_right_cell = prev_gen_grid.cells[right]
        next_gen_right_cell = __roulette_select_cell(b2f[prev_gen_right_cell.state.value])
        next_gen_grid.add_cell_at(next_gen_right_cell, ((right[0] + 1),))

    return next_gen_grid


def __roulette_select_cell(rule_population_matrix: Dict[str, float]) -> Cell:
    population_fitness = sum(rule_population_matrix.values())
    probabilities = [domain_fitness/population_fitness for domain_fitness in rule_population_matrix.values()]
    
    roulette_selection = random.choices(list(rule_population_matrix.keys()), weights=probabilities)

    return Cell(CellState(roulette_selection[0]))