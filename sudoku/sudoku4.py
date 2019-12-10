# File: sudoku4.py

import networkx as nx
from itertools import combinations
import dwave_networkx as dnx
from hybrid.reference.kerberos import KerberosSampler

def adjacent(i, j):
    return i != j and any(i & k == j & k for k in (3, 10, 12))

def make_sudoku_graph(clues):
    G = nx.Graph()
    edges = ((i, j) for i, j in combinations(range(16), 2) if adjacent(i, j))
    G.add_edges_from(edges)
    for c1, c2 in combinations(clues, 2):
        if c1[1] != c2[1]:
            G.add_edge(c1[0], c2[0])
    return G

def decode(coloring, clues):
    lookup = {coloring[x]: y for x, y in clues}
    solution = [lookup[coloring[i]] for i in range(16)]
    disp(solution)

def disp(solution):
    for i in range(0, 16, 4):
        print(solution[i: i+4])

def main():
    clues = [(0, 4), (2, 1), (7, 2), (8, 3), (13, 4)]
    G = make_sudoku_graph(clues)
    coloring = dnx.min_vertex_coloring(G, sampler=KerberosSampler(), chromatic_ub=4, max_iter=10, convergence=3)
    # coloring = nx.coloring.greedy_color(G)
    decode(coloring, clues)


if __name__ == '__main__':
    main()

