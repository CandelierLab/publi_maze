'''
Solving transition as a function of density
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np

# Graph
from maze import maze

# Engine
from engine import Engine
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 20

algo = 'Prims'

# ─── Agents

# Parameters
ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.array([100])

# ─── Simulation

# Runs
n_mazes = 10
n_runs = 100
trigger = 0.9
max_steps = int(1e5)

# ═══ Computation ══════════════════════════════════════════════════════════

for run in range(n_mazes):

  for dst in l_dst:

    for eta in l_eta:

      # ─── Storage ─────────────────────────────

      strg = storage('Parameter space' + os.sep + 
                     algo + os.sep + 
                     f'a={a}' + os.sep +
                     f'density={dst:.03f} - eta={eta:.01f}' + os.sep +
                     f'run {run:04d}.h5')

      # Check existence
      if strg.exists(): 
        continue
      
      print(f'\n─── {algo} dst={dst}, eta={eta} ─── run {run:04d}', '─'*20)

      # ─── Maze ─────────────────────────────────────────────────────────────────

      M = maze(size=a, algorithm=algo, seed=run)
      M.create_LR_loop()

      # ─── Engine ───────────────────────────────────────────────────────────────

      E = Engine(M.graph, storage=strg, multi=n_runs)
      E.storage.save_success = True
      E.max_steps = max_steps

      # ─── Agents ───────────────────────────────────────────────────────────────

      N = int(dst*M.size) # density times the number of cases
      E.add_agents(N, eta)

      # ═══ Simulation ═══════════════════════════════════════════════════════════

      # Trigger
      E.trigger = trigger

      # Run
      E.run()