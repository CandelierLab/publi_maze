'''
ANALYSIS

Resolution time as a function of the maze parameters
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
l_a = np.arange(5,51)

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
    S = storage(f'Time scaling/scaling_eta/{algo}/a={a}.h5')      
    if not S.exists(): continue

    # Load data
    lambda_bar = S['lambda_bar']
    eta = S['eta']
    tau = S['tau']

    X[i] = lambda_bar/eta
    Y[i] = np.mean(tau/eta)

  # Algorithm scatter
  ax.scatter(X, Y, s=10, color=cm[k], label=algo)

# ─── Guide

x = np.geomspace(0.01, 1000, 100)
a = 2
ax.plot(x, a*x, color='w', linestyle=':')

# ─── Plot options ─────────────────────────────────────────────────────────

ax.set_xlim(0.01, 1000)
ax.set_ylim(0.01, 1000000)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel(r'$\bar{\lambda}/\eta$')
ax.set_ylabel(r'$\tau/\eta$')
ax.legend()

plt.show()