# File: sudoku9.py
#
# Solves a Sudoku puzzle on a D-Wave quantum computer, 
# using a hybrid classical/quantum minimum vertex coloring algorithm.
#
# This is an approximate algorithm and it is not guaranteed to find
# the correct solution. In fact, it often fails to find the correct
# solution. The program displays a 'score' which counts the number
# of pairs of cells that have been assigned the same number, even 
# though they are in the same row, column, or block.

import networkx as nx
from itertools import combinations
import dwave_networkx as dnx
from hybrid.reference.kerberos import KerberosSampler

def adjacent(i, j):
    return i != j and (i // 9 == j // 9 or i % 9 == j % 9 or (
        (i // 27 == j // 27) and (i % 9 // 3 == j % 9 // 3)))

def make_sudoku_graph(clues):
    G = nx.Graph()
    edges = ((i, j) for i, j in combinations(range(81), 2) if adjacent(i, j))
    G.add_edges_from(edges)
    for c1, c2 in combinations(clues, 2):
        if c1[1] != c2[1]:
            G.add_edge(c1[0], c2[0])
    return G

def decode(coloring, clues):
    lookup = {coloring[x]: y for x, y in clues if x in coloring}
    solution = [lookup.get(coloring.get(i, '?'), 9) for i in range(81)]
    return solution

def make_clues(board):
    clues = [(i, int(x)) for i, x in enumerate(board) if x.isdigit() and x != '0']
    missing = set(range(1, 10)) - set(x for (i, x) in clues)
    for i, j in enumerate(missing):
        clues.append((81 + i, j))
    return clues

def disp(solution):
    for i in range(0, 81, 9):
        print(*solution[i: i+9])

def solve(grid, use_dwave=False, max_iter=10, convergence=3):
    clues = make_clues(grid)
    G = make_sudoku_graph(clues)
    if use_dwave:
        coloring = dnx.min_vertex_coloring(G, sampler=KerberosSampler(), chromatic_lb=9, chromatic_ub=9, max_iter=max_iter, convergence=convergence)
    else:
        coloring = nx.coloring.greedy_color(G, 'saturation_largest_first')
    solution = decode(coloring, clues)
    disp(solution)
    print('Cost: %d\n' % cost(solution))


def cost(a):
    return sum(
        a[i] == a[j]
        for i, j in combinations(range(81), 2) 
        if adjacent(i, j))



if __name__ == '__main__':
    grid = '53..7....' \
           '6..195...' \
           '.98....6.' \
           '8...6...3' \
           '4..8.3..1' \
           '7...2...6' \
           '.6....28.' \
           '...419..5' \
           '....8..79'

    grid2 = '..1......' \
            '.6.8..3..' \
            '.8....546' \
            '1..64.8..' \
            '...132...' \
            '..7.98..4' \
            '653....1.' \
            '..9..4.5.' \
            '......2..'
    solve(grid2, True, max_iter=20, convergence=5)

