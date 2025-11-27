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
import anim
import Animation.maze

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Number of parallel universes
multi = 1

# Maze
a = 37

# Agents
density = 5
eta = 10

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = corridor(size=a, periodic=True)

# ─── Engine ───────────────────────────────────────────────────────────────

E = Engine(M.graph, platform='GPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size)
E.add_agents(N, eta)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M)

E.animation.colormap = anim.colormap(name='inferno', ncolors=density*5+1)
E.animation.colormap.cmap.colors[0,0:3] = 1.0
print(E.animation.colormap.cmap.colors)
E.animation.colormap.range = [0,density*5]

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_algorithm = False

E.window.autoplay = False

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Run
E.run()