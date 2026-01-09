'''
Distances between the dead ends and the solution
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from alive_progress import alive_bar

# Maze (graph)
from maze import maze

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20

# Number of mazes
m = 1000

algo = 'Prims'
# ──────────────────────────────────────────────────────────────────────────


# ═══ Computation ══════════════════════════════════════════════════════════

L = np.array([])

with alive_bar(m) as bar:
  for i in range(m):

    # ─── Generate maze graph

    M = maze(size=a, algorithm=algo, seed=i)
    M.create_LR_loop()

    # ─── Localize nodes

    # Dead ends
    Id = [node for (node, deg) in M.graph.degree() if deg==1]

    # Solution
    Is = M.graph.solution[0]

    # ─── Compute distances

    l = np.zeros(len(Id))
    for k, id in enumerate(Id):
      ls = nx.shortest_path_length(M.graph, source=id)
      l[k] = np.min([ls[i] for i in Is])

    # ─── Store

    L = np.concatenate([L, l])

    bar()

# M.show(disp_graph=False, disp_solution=True, disp_id=True)

# ═══ Display ══════════════════════════════════════════════════════════════

print('Mean distance to solution:', np.mean(L))

fig, ax = plt.subplots(1,1)

ax.hist(L, bins=np.arange(np.max(L)))

plt.show()