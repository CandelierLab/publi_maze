'''
Model of the resolution time
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

# plt.style.use('dark_background')

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
f_v = F['v']
f_L = F['L']
f_p_lmbd = F['p_lmbd']

# Densities
l_d = l_N/a**2

# Resolution time
tau = (a**2-lmbd)/f_p_lmbd/f_v

# ═══ Figure ════════════════════════════════════════════════════════

X, Y = np.meshgrid(l_d, l_eta)

fig, ax = plt.subplots(1,1)

c = ax.pcolormesh(X, Y, np.log10(tau), cmap = plt.cm.inferno, vmin=2, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax)

# Expected length
plt.contour(X, Y, f_L, levels=[lmbd], colors='k', linestyles='--')

# Speed contour
plt.contour(X, Y, f_v, levels=[0.5], colors='k', linestyles=':')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(min(l_d), max(l_d))
ax.set_ylim(min(l_eta), max(l_eta))

ax.set_xlabel('$N$')
ax.set_ylabel('$\eta$')

plt.show()