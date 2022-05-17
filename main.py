from grid import Grid
from cell import Cell
from system import System


g = Grid(dimensions=2, initial_state=0)

c1 = Cell(state=0)
c2 = Cell(state=1)
g.add_cell_at(c1, (0, 1))
g.add_cell_at(c2, (1, 3))

for i in range(3, 10): g.add_cell_at(Cell(state=i), (0, i))

c3 = c2.copy()
c3.state = 2
g.add_cell_at(c3, (4, 3))
g.swap_cells(c1, c2)
for item in g.cells.items(): print(item)
for a in g.visualize(): print(a)

################################################################################################

g2 = Grid(dimensions=3, initial_state=5)
g2.add_cell_at(Cell(state=4), (0, 0, 0))
g2.add_cell_at(Cell(), (0, 0, 1))
g2.add_cell_at(Cell(state=2), (0, 3, 1))
g2.add_cell_at(Cell(state=3), (6, 2, 2))
for item in g2.cells.items(): print(item)
for a in g2.visualize(): print(a)
# System(gen0=g2, system_rule=System.LINEAR_RULE_0).get_next_gen()

################################################################################################

g_simple = Grid(dimensions=1, initial_state=0)
g_simple.add_cell_at(Cell(state=1), (30,))
# g_simple.add_cell_at(Cell(state=0), (20,))
print(*g_simple.visualize())
s = System(gen0=g_simple, system_rule=System.LINEAR_RULE_182)
for _ in range(30): print(*s.get_next_gen().visualize())