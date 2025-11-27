'''
Parameter space exploration for loopss
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np

# Corridor (graph)
from maze import corridor

# Engine
from engine import Engine
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Loop

lmbd = 37

# ─── Agents

# Parameters
ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

# l_dst = np.array([5])
# l_eta = np.array([10])

# ─── Simulation

# Runs
n_runs = 100
steps = int(1e4)

# ═══ Computation ══════════════════════════════════════════════════════════

for dst in l_dst:

  for eta in l_eta:

    # ─── Storage ─────────────────────────────

    strg = storage(f'Loop a={lmbd}' + os.sep +
                    f'density={dst:.03f} - eta={eta:.01f}.h5')

    # Check existence
    if strg.exists(): 
      continue
    
    print(f'\n─── dst={dst}, eta={eta}', '─'*20)

    # ─── Graph & engine ───────────────────────────────────────────────────

    M = corridor(size=lmbd, periodic=True)

    E = Engine(M.graph, storage=strg, multi=n_runs)
    E.store_success = False
    E.store_blanks = True
    E.storage.save_blanks = True
    

    # ─── Agents ───────────────────────────────────────────────────────────────

    N = int(dst*M.size) # density times the number of cases
    E.add_agents(N, eta)

    # ═══ Simulation ═══════════════════════════════════════════════════════════

    E.steps = steps + int(eta*lmbd)

    # Run
    E.run()