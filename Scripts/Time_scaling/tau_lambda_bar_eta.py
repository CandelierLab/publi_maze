'''
Average resolution time for several mazes
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import numpy as np
import pickle

# Project packages
from maze import maze
from engine import Engine
from storage import storage
from Analysis.Fit.zeta import fit_many

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Mazes
l_algo = maze.algorithms().keys()
l_a = np.arange(5,51)

# Agents
density_limits = [5,100]

# Simulation
n_runs = 10
trigger = 0.9

# ──────────────────────────────────────────────────────────────────────────

def random_logint(I):
  J = np.log10(I)
  return 10**(np.random.rand()*(J[1] - J[0]) + J[0])

# ═══ Computation ══════════════════════════════════════════════════════════

for algo in l_algo:
   
  for i, a in enumerate(l_a):

    # ─── Storage

    S = storage(f'Time scaling/scaling_eta/{algo}/a={a}.h5')

    # Check existence
    if S.exists(): continue
    
    # ─── Maze ──────────────────────────────────

    M = maze(size=int(a), algorithm=algo, seed=0)
    M.create_LR_loop()

    # Lambda
    lmbda = len(M.graph.solution[0])

    # ─── Parameters

    # Density (randomly drawn in log scale)
    dns = int(np.round(random_logint(density_limits)))
    
    # Eta
    I_eta = [max(lmbda/100, 10), 20*dns]
    eta = random_logint(I_eta)

    print(f'─── {algo} a={a}, dns={dns}, eta={eta}', flush=True)



    # ═══ Simulations ════════════════════════════════════════════════════════
   
    # ─── Engine ──────────────────────────────

    E = Engine(M.graph, multi=n_runs)

    # ─── Agents ──────────────────────────────

    N = int(dns*M.size) # density times the number of cases
    E.add_agents(N, eta)

    # ─── Run ─────────────────────────────────
    
    # Trigger
    E.trigger = trigger

    # Run
    E.run()

    # ─── Fits ────────────────────────────────

    zeta_0, L, k, tau = fit_many(E.l_success)

    # ─── Storage ─────────────────────────────────

    # Parameters
    S['lambda'] = lmbda
    S['lambda_bar'] = a**2 - lmbda
    S['density'] = dns
    S['eta'] = eta

    # Results
    S['zeta_0'] = zeta_0
    S['L'] = L
    S['k'] = k
    S['tau'] = tau