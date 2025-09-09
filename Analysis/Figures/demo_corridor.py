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
a = 10

# Agents
density = 5
eta = 10

mdir = '/home/raphael/Science/Projects/CM/Maze/Movies/'

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = corridor(size=a, periodic=False)

# ─── Engine ───────────────────────────────────────────────────────────────

# E = Engine(M.graph, multi=multi)
E = Engine(M.graph, platform='CPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta)

# ─── Storage ──────────────────────────────────────────────────────────────

# E.storage = dataDir + 'seed_' + str(m) + '.h5'
# E.storage = '/home/raphael/Science/Projects/CM/Maze/Files/test.h5'
# E.force_storage = True

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M,
                style = 'white',
                wall_thickness = 0.1,
                wall_color = 'black')

# E.animation.show_densities = True
E.animation.colormap = anim.colormap(name='Blues')
E.animation.colormap.range = [0, 15]

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_algorithm = False

E.window.autoplay = False # type: ignore

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Number of steps
# E.steps = 100
# E.max_steps = 500

# Trigger
# E.trigger = 0.9

# Record the animation in a movie
E.window.movieFile = mdir + f'test.mp4'

# Run
E.run()