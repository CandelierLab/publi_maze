'''
Agents in a very large maze
'''

# Reset command window display
import os, sys
os.system('clear')

import numpy as np
import time
import pickle

# Maze (graph)
from maze import maze

# Engine
from storage import storage
from engine import Engine

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Maze
algo = 'Prims'
a = 1000
seed = 0

# Agents
density = 10
eta = 100000

max_steps = int(2e7)

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Maze ─────────────────────────────────────────────────────────────────

'''
Maze creation times (Prims)
───────────────────────────
a=100:  0.2s
a=200:  1.3s
a=500:  19.8s
a=1000: 157s
'''

S = storage(f'Large_maze/{algo}/maze_a={a}_seed={seed}', ext=None)

tref = time.perf_counter()

if S.exists():

  print('Loading maze ...', end='', flush=True)
  with open(S.filepath, 'rb') as f:
    M = pickle.load(f)

else:

  print('Creating maze ...', end='', flush=True)
  M = maze(size=a, algorithm=algo, seed=seed)
  M.create_LR_loop()

  print(f' {time.perf_counter()-tref} sec')
  tref = time.perf_counter()

  print('Saving maze ...', end='', flush=True)
  with open(S.filepath, 'wb') as f:
    pickle.dump(M, f)

print(f' {time.perf_counter()-tref:.02f} sec')

# ─── Engine ───────────────────────────────────────────────────────────────

E = Engine(M.graph, platform='GPU', multi=1)

# ─── Agents ───────────────────────────────────────────────────────────────

N = int(density*M.size) # density times the number of cases
E.add_agents(N, eta)

# ─── Storage ──────────────────────────────────────────────────────────────

E.storage = storage(f'Large_maze/{algo}/run_a={a}_seed={seed}.h5')
E.storage.save_success = True
E.store_densities = True
E.store_steps = np.concatenate((np.arange(0, 1000),
                                np.arange(1000, 10000, 10),
                                np.arange(10000, 100000, 100),
                                np.arange(100000, 1000000, 1000),
                                np.arange(1000000, max_steps, 10000))).astype(int)

E.storage['steps'] = E.store_steps

# ═══ Simulation ═══════════════════════════════════════════════════════════

# Number of steps
# E.steps = 1000
E.max_steps = max_steps

# Trigger
E.trigger = 0.9

# Run
E.run()