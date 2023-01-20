import PySimpleGUI as sg
from cell import Cell, CellState
from grid import Grid
from system import System, SystemRule
from premade_systems import elementary_wolfram_system as ews


NO_OF_GENS = 40
SQUARE_SIZE = 400 // NO_OF_GENS
# SQUARE_SIZE = 10
CANVAS_HEIGHT = NO_OF_GENS * SQUARE_SIZE
CANVAS_WIDTH = (2 * NO_OF_GENS - 1) * SQUARE_SIZE + 1 \
               if ((400 // NO_OF_GENS) % 2 == 0) else \
               (2 * NO_OF_GENS - 1) * SQUARE_SIZE
canvas_state = 'CLEAR'


def int_to_bin(num):
    return format(num, '08b')


def visualize(grid, current_grid_depth):
    for cell in grid.cells.keys():
        graph.draw_rectangle((cell[0] * SQUARE_SIZE, current_grid_depth * SQUARE_SIZE),
                             (cell[0] * SQUARE_SIZE + SQUARE_SIZE, current_grid_depth * SQUARE_SIZE + SQUARE_SIZE),
                             line_color="black",
                             fill_color="black")


def mouse_location_to_column(mouse_location_x):
    return mouse_location_x // SQUARE_SIZE


def clear_canvas():
    global canvas_state
    global g_test

    canvas_state = 'CLEAR'
    graph.erase()

    g_test = Grid(dimensions=(2 * NO_OF_GENS + 1,))


def update_no_of_gens(value):
    global NO_OF_GENS
    global SQUARE_SIZE
    global CANVAS_HEIGHT
    global CANVAS_WIDTH

    NO_OF_GENS = value
    SQUARE_SIZE = 400 // NO_OF_GENS
    current_grid_depth = 0
    graph.erase()
    for gen in s_test.generations:
        visualize(gen, current_grid_depth)
        current_grid_depth += 1


sg.theme('Dark Blue 3')

layout = [[sg.Text('Enter rule number you wish to view: ')],
          [sg.Input(key='-IN-'), sg.Button('Enter'), sg.Button('Clear')],
          [sg.Text('Number of generations: '),
           sg.Slider(range=(1, 100),
                     default_value=40,
                     resolution=1,
                     orientation='h',
                     enable_events=True,
                     trough_color="white",
                     key="slider",
                     )],
          [
              sg.Graph(
                  canvas_size=(CANVAS_WIDTH, CANVAS_HEIGHT),
                  background_color="white",
                  graph_bottom_left=(0, CANVAS_HEIGHT),
                  graph_top_right=(CANVAS_WIDTH, 0),
                  key="graph",
                  drag_submits=True,
                  enable_events=True,
                  motion_events=True,
              )
          ]]

window = sg.Window('Wolfram Rules', layout)

graph = window.Element("graph")

g_test = Grid(dimensions=(2 * NO_OF_GENS + 1,))

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'graph+MOVE':
        if canvas_state == 'CLEAR':
            column = mouse_location_to_column(values['graph'][0])
            if (column,) not in g_test.cells.keys():
                if 'hover_column' in locals():
                    graph.delete_figure(hover_column)

                hover_column = graph.draw_rectangle((column * SQUARE_SIZE, 0),
                                                    (column * SQUARE_SIZE + SQUARE_SIZE, CANVAS_HEIGHT),
                                                    line_color="light gray",
                                                    fill_color="light gray")

    if event == 'graph':
        column = mouse_location_to_column(values['graph'][0])
        if canvas_state != 'CLEAR':
            clear_canvas()

        graph.delete_figure(hover_column)
        g_test.add_cell_at(Cell(CellState(value=1)), (column,))

        graph.draw_rectangle((column * SQUARE_SIZE, 0),
                             (column * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE),
                             line_color="red",
                             fill_color="red")

    if event == 'Enter':
        if canvas_state == 'DRAWN':
            clear_canvas()

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
            if len(g_test.cells) == 0:
                c_default = Cell(CellState(value=1))
                g_test.add_cell_at(c_default, (NO_OF_GENS,))

            if grid_depth == 0:
                visualize(s_test.get_latest_gen(), grid_depth)
                s_test.get_latest_gen().visualize()
                grid_depth += 1

            for i in range(NO_OF_GENS):
                visualize(s_test.get_next_gen(), grid_depth)
                # s_test.get_next_gen().visualize()
                grid_depth += 1

            canvas_state = 'DRAWN'

    if event == 'slider':
        clear_canvas()
        update_no_of_gens(int(values['slider']))

    if event == 'Clear':
        clear_canvas()

window.close()
