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
a = 50
density = 20
eta = 500

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

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = maze(size=a, algorithm=algo, seed=seed)
M.create_LR_loop()

# ─── Engine ───────────────────────────────────────────────────────────────

# E = Engine(M.graph, multi=multi)
E = Engine(M.graph, platform='GPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M, log_densities=True, colorbar=False)

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_locking = False

# Colorbar
import anim
E.window.information.canva.item.cbar = anim.plane.colorbar(
    position = [0.8, 1],
    dimension = [0.2, 2],
    colormap = E.animation.colormap,
    ticks_number = 6,
    ticks_fontsize = 0.1,
    ticks_color = '#AAA'
  )
E.window.information.canva.item.cbar.subitem['tick_0_text'].string = '0'
E.window.information.canva.item.cbar.subitem['tick_0_text'].x = -0.21
E.window.information.canva.item.cbar.subitem['tick_1_text'].string = '1'
E.window.information.canva.item.cbar.subitem['tick_1_text'].x = -0.21
E.window.information.canva.item.cbar.subitem['tick_2_text'].string = '10'
E.window.information.canva.item.cbar.subitem['tick_2_text'].x = -0.25
E.window.information.canva.item.cbar.subitem['tick_3_text'].string = '100'
E.window.information.canva.item.cbar.subitem['tick_3_text'].x = -0.29
E.window.information.canva.item.cbar.subitem['tick_4_text'].string = '1,000'
E.window.information.canva.item.cbar.subitem['tick_4_text'].x = -0.35
E.window.information.canva.item.cbar.subitem['tick_5_text'].string = '10,000'
E.window.information.canva.item.cbar.subitem['tick_5_text'].x = -0.39

# E.window.movieFile = '/home/raphael/Bureau/movies_log_densitie.mp4'

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Trigger
# E.trigger = 0.9

# Run
E.run()