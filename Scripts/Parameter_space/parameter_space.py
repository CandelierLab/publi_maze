'''
Parameter space exploration
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

# ─── Agents

# Parameters
ndpd = 4
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

# print('dst', l_dst)
# print('eta', l_eta)

# l_dst = np.array([l_dst[14]])
# l_eta = np.array([l_eta[-1]])

# print('dst', l_dst)
# print('eta', l_eta)

# import sys
# sys.exit()

# ─── Simulation

# Runs
n_runs = 1
n_multi = 100
trigger = 0.9

# Computation limit
max_steps = int(1e5)
max_energy = int(1e4)

# ═══ Computation ══════════════════════════════════════════════════════════

for run in range(n_runs):

  for dst in l_dst:

    for eta in l_eta:

      # ─── Storage ─────────────────────────────

      strg = storage('Parameter space' + os.sep + algo + os.sep + os.sep +
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

      E = Engine(M.graph, storage=strg, multi=n_multi)
      E.storage.save_success = True
      E.storage.save_energy = True
      
      E.max_steps = max_steps
      E.max_energy = max_energy

      # ─── Agents ───────────────────────────────────────────────────────────────

      N = int(dst*M.size) # density times the number of cases
      E.add_agents(N, eta)

      # ═══ Simulation ═══════════════════════════════════════════════════════════

      # Trigger
      E.trigger = trigger

      # Run
      E.run()
      