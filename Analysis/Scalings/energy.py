'''
ANALYSIS

Energy scaling
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt

from maze import maze
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_algo = maze.algorithms().keys()
# l_algo = ['Wilsons']

b = 1
l_a = np.round(np.geomspace(5, 100, 5*b+1))

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Figure ───────────────────────────────────────────────────────────────

plt.style.use('dark_background')
fig, ax = plt.subplots(1,1, figsize=(7,7))
cm = plt.cm.rainbow(np.linspace(0, 1, len(l_algo)))

# ─── Load data ────────────────────────────────────────────────────────────

for k, algo in enumerate(l_algo):

  X = np.zeros(l_a.size)
  Y = np.zeros(l_a.size)
   
  for i, a in enumerate(l_a):

    # Storage
    S = storage(f'Scalings/Energy/{algo}_a={a}.h5')
    if not S.exists(): continue


    # Load data
    lambda_bar = S['lambda_bar']
    dns = S['density']
    tau = S['tau']
    max_steps = S['max_steps']
    max_energy = S['max_energy']
    energy = S['energy']

    # print('--------', dns)
    # print(tau)
    # print(energy)
    energy[energy>max_energy*0.95] = np.nan
    # print(energy)
    
    # if dns<2: continue

    X[i] = lambda_bar
    Y[i] = np.nanmean(energy)

    # print('X', X)
    # print('Y', Y)
    
  # print(X, Y)

  # Algorithm scatter
  ax.scatter(X, Y, s=10, color=cm[k], label=algo)

  # sys.exit()

# ─── Guide

# x = np.geomspace(0.01, 1000, 100)
# a = 2
# ax.plot(x, a*x, color='w', linestyle=':')

# ─── Plot options ─────────────────────────────────────────────────────────

# ax.set_xlim(0.5, 5)
# ax.set_ylim(1e-2, 1e6)

ax.set_xscale('log')
ax.set_yscale('log')

# ax.set_xlabel(r'$\bar{\lambda}$')
ax.set_ylabel(r'$E$')
# ax.legend()

plt.show()