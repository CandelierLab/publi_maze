'''
Parameter space demo insets
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QImage
import matplotlib.pyplot as plt

# Maze (graph)
from maze import maze

# Engine
from engine import Engine

# Display
import anim
import Animation.maze

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Maze
a = 20

# Parameters
density = 3
eta = 100

# Algorithm
algo = 'Prims'
seed = 0

steps = 1e5
t = np.unique(np.round(np.geomspace(1, 1e5, 750)).astype(int))

# ──────────────────────────────────────────────────────────────────────────

mdir = f'Movies/Parameter_space/Insets/d={density}_eta={eta}/'

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

M = maze(size=a, algorithm=algo, seed=seed)
M.create_LR_loop()

# ─── Engine ───────────────────────────────────────────────────────────────

class engine(Engine):

  # ────────────────────────────────────────────────────────────────────────
  def update(self, iteration):

    super().update(iteration)

    if iteration in t:

      # Grab image
      img = self.window.grab().toImage().scaledToWidth(1000).convertToFormat(QImage.Format.Format_RGB888)

      # Crop
      img = img.copy(QRect(214,12,776,776)).scaledToWidth(194)

      img.save(mdir+f'frame_{iteration}.png', 'png', 100)

E = engine(M.graph, platform='GPU')

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta)

# ─── Display ──────────────────────────────────────────────────────────────

E.setup_display(Animation.maze.density, maze=M, log_densities=True, colorbar=False, 
                style='white', wall_color='k', wall_thickness=.1)

# Make it as fast as possible
E.window.dt = 0

E.animation.colormap = anim.colormap(name='Blues')
E.animation.colormap.range = [0,np.log10(density*a**2/50)]

# Information
E.animation.window.information.show_time = False
E.animation.window.information.show_locking = False

# E.window.movieFile = '/home/raphael/Bureau/movies_log_densitie.mp4'

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Steps
# E.steps = 1

E.steps = steps
# E.animation.window.autoplay = False

# Run
E.run()