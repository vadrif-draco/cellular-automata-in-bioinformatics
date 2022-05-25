from cell import Cell, CellState
from grid import Grid
from system import System, SystemRule
from premade_systems import elementary_wolfram_system as ews
from premade_systems import protein_domain_evolution_system as pd


g = Grid(dimensions=(5, 10))
c1 = Cell(state=CellState(value=0))
c2 = Cell(state=CellState(value=1))
g.add_cell_at(c1, (0, 1))
g.add_cell_at(c2, (1, 3))

for i in range(3, 10): g.add_cell_at(Cell(CellState(value=i)), (0, i))

c3 = c2.copy()
c3.state = CellState(value=2)
g.add_cell_at(c3, (4, 3))
g.swap_cells(c1, c2)
for item in g.cells.items(): print(item)
g.visualize()
print()

################################################################################################

g2 = Grid(dimensions=(8, 5, 4))
g2.add_cell_at(Cell(CellState(value=4)), (0, 0, 0))
g2.add_cell_at(Cell(CellState(value=0)), (0, 0, 1))
g2.add_cell_at(Cell(CellState(value=2)), (0, 3, 1))
g2.add_cell_at(Cell(CellState(value=3)), (6, 2, 2))
for item in g2.cells.items(): print(item)
g2.visualize()
print()

################################################################################################


g_test = Grid(dimensions=(27,))

c_test = Cell(CellState(value=1))

g_test.add_cell_at(c_test, (0,))
# g_test.add_cell_at(c_test, (12,))
# g_test.add_cell_at(c_test, (14,))
# g_test.add_cell_at(c_test, (17,))

sr_test = SystemRule(ews.ALLOWED_DIMENSIONALITIES,
                     ews.tf, ews.RULE_001)

s_test = System(gen0=g_test, system_rule=sr_test)

s_test.get_latest_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()
s_test.get_next_gen().visualize()

################################################################################################

pdg_test = Grid(dimensions=(21,))
pdc_test = Cell(CellState(value='Y'))
pdc2_test = Cell(CellState(value='X'))
pdg_test.add_cell_at(pdc_test, (10,))
pdg_test.add_cell_at(pdc2_test, (11,))



pdsr_test = SystemRule(pd.ALLOWED_DIMENSIONALITIES,
                       pd.tf, 
                       pd.F2B, 
                       pd.B2F)

pds_test = System(gen0=pdg_test, system_rule=pdsr_test)
pds_test.get_latest_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()
pds_test.get_next_gen().visualize()