'''
Proportion of mobile agents
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Storage
from storage import storage

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 20
n_bins = 200

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)

# Base tag
base_tag = 'Parameter space' + os.sep + 'expected' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load data ─────────────────────────────────

F = storage(base_tag + f'a={a} n_bins={n_bins}')

l_N = F['N']
l_eta = F['eta']
f_mob = F['p_mob']

# ═══ Figure ════════════════════════════════════════════════════════

l_d = l_N/a**2
X, Y = np.meshgrid(l_d, l_eta)

fig, ax = plt.subplots(1,1, figsize=(5,5))

c = ax.pcolormesh(X, Y, f_mob, cmap = plt.cm.inferno, vmin=0, vmax=1, rasterized=True)
fig.colorbar(c, ax=ax)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(min(l_d), max(l_d))
ax.set_ylim(min(l_eta), max(l_eta))

ax.set_title('Proportion of mobile agents ($n>\eta$)')
ax.set_xlabel('density $d$')
ax.set_ylabel('kinetic parameter $\eta$')

ax.set_box_aspect(1)

plt.show()