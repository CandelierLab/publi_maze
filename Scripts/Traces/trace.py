'''
Trace to display
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

algo = 'Prims'
a = 20

# ─── Agents

# Parameters
dst = 5
l_eta = [500]

# ─── Simulation

# Runs
n_steps = int(1e5)

# ═══ Computation ══════════════════════════════════════════════════════════

for eta in l_eta:

  # ─── Storage ─────────────────────────────

  strg = storage('Traces' + os.sep + 
                  algo + os.sep + 
                  f'a={a}_density={dst}_eta={eta}.h5')

  # Check existence
  # if strg.exists(): continue
  
  print(f'\n─── {algo} dst={dst}, eta={eta}', '─'*20)

  # ─── Maze ─────────────────────────────────────────────────────────────────

  M = maze(size=a, algorithm=algo, seed=0)
  M.create_LR_loop()

  # ─── Engine ───────────────────────────────────────────────────────────────

  E = Engine(M.graph, storage=strg)
  E.storage.save_success = True
  E.steps = n_steps

  # ─── Agents ───────────────────────────────────────────────────────────────

  N = int(dst*M.size) # density times the number of cases
  E.add_agents(N, eta)

  # ═══ Simulation ═══════════════════════════════════════════════════════════

  # Run
  E.run()