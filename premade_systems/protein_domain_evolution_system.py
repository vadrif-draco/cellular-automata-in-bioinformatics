import random
from cmath import inf
from typing import TextIO, Tuple
from grid import Grid
from cell import Cell, CellState

ALLOWED_DIMENSIONALITIES = [1]
INITIAL_CELL_STATE = CellState('Φ')  # XXX: y no use?


class ProteinSequence:
    def __init__(self, header: str, sequence: str) -> None:
        self.header = header
        self.sequence = sequence


F2B = {
    'X': {
        'α': 0.3,
        'X': 0.1,
        'Y': 0.6,
        'Z': 0.4,
        # 'Ω': 0.2
    },
    'Y': {
        'α': 0.5,
        'X': 0.6,
        'Y': 0.3,
        'Z': 0.7,
        # 'Ω': 0.3
    },
    'Z': {
        'α': 0.2,
        'X': 0.2,
        'Y': 0.1,
        'Z': 0.3,
        # 'Ω': 0.3
    }
}

B2F = {
    'X': {
        # 'α': 0.3,
        'X': 0.1,
        'Y': 0.3,
        'Z': 0.2,
        'Ω': 0.2
    },
    'Y': {
        # 'α': 0.5,
        'X': 0.6,
        'Y': 0.3,
        'Z': 0.1,
        'Ω': 0.3
    },
    'Z': {
        # 'α': 0.2,
        'X': 0.4,
        'Y': 0.7,
        'Z': 0.3,
        'Ω': 0.3
    }
}


def tf(*tfargs) -> Grid:

    prev_gen_grid: Grid = tfargs[0]
    f2b: dict[str, dict[str, float]] = tfargs[1][0]
    b2f: dict[str, dict[str, float]] = tfargs[1][1]

    next_gen_grid: Grid = prev_gen_grid.copy()

    left = min(prev_gen_grid.cells.keys(), key=lambda key: key[0])
    right = max(prev_gen_grid.cells.keys(), key=lambda key: key[0])

    if left[0] > 0 and prev_gen_grid.cells[left].state.value != 'α':
        prev_gen_left_cell = prev_gen_grid.cells[left]
        next_gen_left_cell = __roulette_select_cell(f2b[prev_gen_left_cell.state.value])
        next_gen_grid.add_cell_at(next_gen_left_cell, ((left[0] - 1),))

    if right[0] < prev_gen_grid.dimensions[0] - 1 and prev_gen_grid.cells[right].state.value != 'Ω':
        prev_gen_right_cell = prev_gen_grid.cells[right]
        next_gen_right_cell = __roulette_select_cell(b2f[prev_gen_right_cell.state.value])
        next_gen_grid.add_cell_at(next_gen_right_cell, ((right[0] + 1),))

    return next_gen_grid


def __roulette_select_cell(rule_population_matrix: dict[str, float]) -> Cell:
    population_fitness = sum(rule_population_matrix.values())
    probabilities = [domain_fitness / population_fitness for domain_fitness in rule_population_matrix.values()]

    roulette_selection = random.choices(list(rule_population_matrix.keys()), weights=probabilities)

    return Cell(CellState(roulette_selection[0]))


def parse_fasta_file(fasta_file: TextIO) -> list[ProteinSequence]:
    seqs = []
    index = 0
    for line in fasta_file:
        if line[0] == '>':
            if index >= 1:
                seqs.append(ProteinSequence(header, seq))
            index += 1
            header = line[1:]
            seq = []
        else:
            seq += line[:-1]

    seqs.append(ProteinSequence(header, ''.join(seq)))

    return seqs


def protein_to_domains(protein: ProteinSequence, domains: list[str]) -> list[str]:
    # Note:
    # The implementation of this function is currently very subjective and depends
    # on our own intrepretation. Normally, the domains would've been chosen using
    # other algorithms and machine learning. For example, the original paper suggests
    # using HMMER and Pfam databases. Also another method would be to use DomainWorld
    # https://domainworld.uni-muenster.de/
    seq = protein.sequence
    protein_domains = []
    while True:
        min_index = inf
        min_domain = ''
        for domain in domains:
            index = seq.find(domain)
            if index < min_index and index != -1:
                min_index = index
                min_domain = domain
            elif index == min_index:
                min_domain = min(min_domain, domain)

        if min_domain == '':
            break

        protein_domains.append(min_domain)
        seq = seq.replace(min_domain, '')

    if len(seq) != 0:
        protein_domains.append(seq)

    return protein_domains


def calculate_probabilities(protein_domains: list[list[ProteinSequence]], possible_domains: list[str])\
        -> Tuple[dict[str, dict[str, float]], dict[str, dict[str, float]]]:
    # Note:
    # The implementation of this function is currently very subjective and depends
    # on our own intrepretation. Normally, the domains would've been chosen using
    # other algorithms and machine learning. For example, the original paper suggests
    # using HMMER and Pfam databases. Also another method would be to use DomainWorld
    # https://domainworld.uni-muenster.de/
    # Here, we use the existing sequences as our training set to calculate probabilities.
    occurrences = {}
    f2b = {}
    b2f = {}

    for domain in possible_domains:
        occurrences[domain] = 0
        f2b[domain] = dict.fromkeys(possible_domains, 0.01)
        b2f[domain] = dict.fromkeys(possible_domains, 0.01)

    for domains in protein_domains:
        for domain in range(len(domains) - 1):
            occurrences[domains[domain]] += 1
            f2b[domains[domain]][domains[domain + 1]] += 1
            b2f[domains[domain + 1]][domains[domain]] += 1

    for domains in protein_domains:
        for domain in range(len(domains) - 1):
            f2b[domains[domain]][domains[domain + 1]] /= occurrences[domains[domain]]
            b2f[domains[domain + 1]][domains[domain]] /= occurrences[domains[domain]]

    return (f2b, b2f)
