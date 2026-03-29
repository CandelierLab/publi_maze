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
density = 20
eta = 200

seed = 0
 
algo = 'Prims'

mname = f'2 loops/beta=0.20 - d={density} - eta={eta} test .mp4'

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = maze(size=a, algorithm=algo, seed=seed)
# M.create_LR_loop()

M.graph.solution = []

# Large loop
M.graph.add_edge(365,366)
M.graph.solution.append([365,366,346,326,327,328,308,307,287,267,247,248,228,229,230,231,211,191,192,172,152,132,131,130,129,128,127,126,125,145,144,164,184,204,224,244,264,284,304,324,344])

# Second loop, disconnected
M.graph.add_edge(393,394)
# M.graph.solution.append([393,394,374,354,334,33,332,352,372,392])

# Second lood, connected
# M.graph.add_edge(27,47)
# M.graph.solution.append([365,366,346,326,327,328,308,307,287,267,247,248,228,229,230,231,211,191,192,172,152,132,131,130,129,128,127,126,125,145,144,164,184,204,224,244,264,284,304,324,344,112,111,91,71,51,31,30,29,28,27,47,67,87,107])

# M.graph.add_edge(14, 15)

# Show
# M.show(disp_graph=False, disp_solution=True, disp_id=True)

# ─── Engine ───────────────────────────────────────────────────────────────

# E = Engine(M.graph, multi=multi)
E = Engine(M.graph, platform='GPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M, log_densities=True)

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_locking = False

# E.window.movieFile = '/home/raphael/Science/Articles/2026 - @ - Maze/Code/Movies/Softmax/' + mname

# ═══ Simulation ═══════════════════════════════════════════════════════════

E.steps = 2000

# Trigger
# E.trigger = 0.9

# Run
E.run()