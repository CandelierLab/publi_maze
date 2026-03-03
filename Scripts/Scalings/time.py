'''
Scaling: time
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import datetime
import numpy as np

# Project packages
from maze import maze
from engine import Engine
from storage import storage
from Analysis.Fit.zeta import fit_many

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Mazes
l_algo = maze.algorithms().keys()
# l_algo = ['Prims']

b = 2
l_a = np.round(np.geomspace(5, 100, 5*b+1))

# Time
t_eta = [3, 300]
t_dns = 30

# Simulation
n_multi = 10
trigger = 0.9

# Computation limit
max_steps = int(1e5)
max_energy = int(1e5)

# ──────────────────────────────────────────────────────────────────────────

def random_logint(I):
  J = np.log10(I)
  return 10**(np.random.rand()*(J[1] - J[0]) + J[0])

# ═══ Computation ══════════════════════════════════════════════════════════

for algo in l_algo:
   
  for i, a in enumerate(l_a):

    print(f'\n─── {algo} a={a}')
    
    # ─── Storage

    S = storage(f'Scalings/Time/{algo}_a={a}.h5')

    # Check existence
    if S.exists(): 
      continue
    
    # ─── Maze ──────────────────────────────────

    M = maze(size=int(a), algorithm=algo)
    M.create_LR_loop()

    # Lambda
    lmbda = len(M.graph.solution[0])

    # ─── Parameters

    # Density (randomly drawn in log scale)
    dns = t_dns
    eta = random_logint(t_eta)
    
    print(f'Energy: dns={dns:.02f}, eta={eta:.02f}', '─'*5, datetime.datetime.now(), flush=True)

    # ─── Engine ──────────────────────────────

    E = Engine(M.graph, multi=n_multi)
    E.store_success = True
    E.store_energy = True
    
    E.max_steps = max_steps
    E.max_energy = max_energy

    # ─── Agents ──────────────────────────────

    N = int(dns*M.size) # density times the number of cases
    E.add_agents(N, eta)

    # ─── Run ─────────────────────────────────
    
    # Trigger
    E.trigger = trigger

    # Run
    E.run(skip_checks=True)

    # ─── Fits ────────────────────────────────

    success = E.l_success.astype(np.float16)
    energy = E.l_energy.astype(np.uint32)

    zeta_0, L, k, tau = fit_many(success)

    # ─── Storage ─────────────────────────────────

    # Parameters
    S['max_steps'] = max_steps
    S['max_energy'] = max_energy

    # Variables
    S['lambda'] = lmbda
    S['lambda_bar'] = M.size - lmbda
    S['density'] = N/M.size
    S['eta'] = eta

    # Results
    S['zeta_0'] = zeta_0
    S['L'] = L
    S['k'] = k
    S['tau'] = tau

    tau[np.isnan(tau)] = success.shape[1]-1
    tau = np.round(tau).astype(int) 
    tau[tau>=success.shape[1]] = success.shape[1]-1
    
    S['energy'] =  np.array([energy[i,j]/N for i,j in enumerate(tau)])

    # Clear engine
    del E