'''
Agents in a corridor
'''

# Reset command window display
import os
os.system('clear')

# Maze (graph)
from maze import corridor

# Engine
from engine import Engine

# Display
import Animation.maze

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Number of parallel universes
multi = 1

# Maze
a = 50

# Agents
density = 5
eta = 100

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = corridor(size=a, periodic=False)

# ─── Engine ───────────────────────────────────────────────────────────────

E = Engine(M.graph, platform='GPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size)
E.add_agents(N, eta)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M)

E.animation.colormap.range = [0,density*5]

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_algorithm = False

E.window.autoplay = False

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Run
E.run()