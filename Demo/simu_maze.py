'''
Agents in a maze with left-right solutions
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
import matplotlib.pyplot as plt

# Maze (graph)
from maze import maze

# Engine
from engine import Engine

# Display
import Animation.maze

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Number of parallel universes
multi = 1
# Maze

a = 20
seed = 0

# algo = 'AldousBroder'
# algo = 'BacktrackingGenerator'
# algo = 'BinaryTree'
# algo = 'Division'
# algo = 'GrowingTree'
# algo = 'HuntAndKill'
# algo = 'Kruskal'
algo = 'Prims'
# algo = 'Sidewinder'
# algo = 'Wilsons'

# Agents
density = 5

eta = 100
gamma = 10

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = maze(size=a, algorithm=algo, seed=seed)
M.create_LR_loop()

# ─── Engine ───────────────────────────────────────────────────────────────

# E = Engine(M.graph, multi=multi)
E = Engine(M.graph, platform='CPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta, gamma=gamma)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M)

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_locking = False

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Trigger
E.trigger = 0.9


# Run
E.run()