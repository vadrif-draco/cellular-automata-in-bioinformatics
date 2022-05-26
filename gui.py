import PySimpleGUI as sg
from cell import Cell, CellState
from grid import Grid
from system import System, SystemRule
from premade_systems import elementary_wolfram_system as ews


NO_OF_GENS = 48
SQUARE_SIZE = 400 // NO_OF_GENS
# SQUARE_SIZE = 10
CANVAS_HEIGHT = NO_OF_GENS * SQUARE_SIZE
CANVAS_WIDTH = (2 * NO_OF_GENS - 1) * SQUARE_SIZE + 1 if ((800 // NO_OF_GENS) % 2 == 0) else (2 * NO_OF_GENS - 1) * SQUARE_SIZE


def int_to_bin(num):
    return format(num, '08b')


def visualize(grid, current_grid_depth):
    for cell in grid.cells.keys():
        graph.draw_rectangle((cell[0] * SQUARE_SIZE, current_grid_depth * SQUARE_SIZE),
                            (cell[0] * SQUARE_SIZE - SQUARE_SIZE, current_grid_depth * SQUARE_SIZE + SQUARE_SIZE),
                            line_color="black",
                            fill_color="black")


sg.theme('Dark Blue 3')

layout = [[sg.Text('Enter rule number you wish to view: ')],
          [sg.Input(key='-IN-'), sg.Button('Enter')],
          [
              sg.Graph(
                  canvas_size=(CANVAS_WIDTH, CANVAS_HEIGHT),
                  background_color="white",
                  graph_bottom_left=(0, CANVAS_HEIGHT),
                  graph_top_right=(CANVAS_WIDTH, 0),
                  key="graph"
              )
          ]]

window = sg.Window('Wolfram Rules', layout)

g_test = Grid(dimensions=(2 * NO_OF_GENS + 1,))

c_test = Cell(CellState(value=1))

g_test.add_cell_at(c_test, (NO_OF_GENS,))

graph = window.Element("graph")

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Enter':
        graph.erase()
        if values['-IN-'] != '':
            grid_depth = 0
            sr_test = SystemRule(ews.ALLOWED_DIMENSIONALITIES,
                                 ews.tf, int_to_bin(int(values['-IN-'])))

            s_test = System(gen0=g_test, system_rule=sr_test)
            # graph.draw_line((CANVAS_WIDTH // 2, 0),
            #                (CANVAS_WIDTH // 2, CANVAS_HEIGHT),
            #                color="black",
            #                width=3)
            if grid_depth == 0:
                visualize(s_test.get_latest_gen(), grid_depth)
                grid_depth += 1

            for i in range(NO_OF_GENS):
                visualize(s_test.get_next_gen(), grid_depth)
                grid_depth += 1

window.close()
