'''
Agents in a maze with LR solutions
'''

# Reset command window display
import os
os.system('clear')

import anim

# Maze (graph)
from maze import maze

# Engine
from engine import Engine

# Display
import Animation.maze

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Maze
a = 10
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
density = 2
eta = 25

# Steps
n_steps = 500

# ──────────────────────────────────────────────────────────────────────────

mdir = '/home/raphael/Science/Projects/CM/Maze/Movies/'

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = maze(size=a, algorithm=algo, seed=seed)
M.create_LR_loop()

# ─── Engine ───────────────────────────────────────────────────────────────

E = Engine(M.graph, platform='GPU')

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

E.animation.colormap = anim.colormap(name='Blues')
E.animation.colormap.range = [0, 5]

# Information
E.animation.window.information.show_time = False
E.animation.window.information.canva.boundaries = [[0,1],[0,3]]

E.animation.window.information.canva.item.cbar = anim.plane.colorbar(
  position = [0.8, 1],
  dimension = [0.2, 2],
  colormap = E.animation.colormap,
  ticks_number = 2,
  ticks_fontsize = 0.1,
  ticks_color = '#000'
)

# E.window.autoplay = False # type: ignore

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Number of steps
E.steps = n_steps

# Record the animation in a movie
# E.window.movieFile = mdir + f'test.mp4'

# Run
E.run()
