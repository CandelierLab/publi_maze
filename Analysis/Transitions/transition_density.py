'''
ANALYSIS
Transition in density
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Maze
from maze import maze

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 20

algo = 'Prims'

# Zeta random
zeta_r = maze.zeta_random(algo, a)

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load fields ────────────────────────────────

F = storage(base_tag + 'transition_density')

l_dst = F['dst']
l_eta = F['eta']
f_tau = F['tau'].flatten()
f_tau[f_tau==0] = np.nan

print(f_tau)

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(7,7))

ax.plot(l_dst, f_tau, '.-')
# ax.plot(l_eta, f_tau[:,40], '.-')

# ─── Plot settings

# Labels
ax.set_xlabel('density $d$')
ax.set_ylabel('solving time $\\tau$')
ax.set_title('$\eta = 100$')

# Axes limits
# ax.set_xlim(np.min(l_dst), np.max(l_dst))
# ax.set_ylim(np.min(l_eta), np.max(l_eta))

# Log scale
ax.set_xscale('log')
ax.set_yscale('log')

ax.grid('on')
# ax.set_box_aspect(1)

plt.show()