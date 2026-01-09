'''
Model explaining the parameter space
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
f_v = F['v']
f_L = F['L']
f_p_lmbd = F['p_lmbd']

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(2, 2)

X, Y = np.meshgrid(l_N, l_eta)

c = ax[0,0].pcolormesh(X, Y, f_L, cmap = plt.cm.inferno, rasterized=True)
fig.colorbar(c, ax=ax[0,0])

ax[0,0].set_xscale('log')
ax[0,0].set_yscale('log')

ax[0,0].set_xlim(min(l_N), max(l_N))
ax[0,0].set_ylim(min(l_eta), max(l_eta))

ax[0,0].set_xlabel('$N$')
ax[0,0].set_ylabel('$\eta$')

c = ax[0,1].pcolormesh(X, Y, f_v, cmap = plt.cm.inferno, rasterized=True)
fig.colorbar(c, ax=ax[0,1])

ax[0,1].set_xscale('log')
ax[0,1].set_yscale('log')

ax[0,1].set_xlim(min(l_N), max(l_N))
ax[0,1].set_ylim(min(l_eta), max(l_eta))

ax[0,1].set_xlabel('$N$')
ax[0,1].set_ylabel('$\eta$')

c = ax[1,0].pcolormesh(X, Y, f_p_lmbd, cmap = plt.cm.inferno, rasterized=True)
fig.colorbar(c, ax=ax[1,0])

ax[1,0].set_xscale('log')
ax[1,0].set_yscale('log')

ax[1,0].set_xlim(min(l_N), max(l_N))
ax[1,0].set_ylim(min(l_eta), max(l_eta))

ax[1,0].set_xlabel('$N$')
ax[1,0].set_ylabel('$\eta$')

tau = (a**2-lmbd)/f_p_lmbd/f_v

c = ax[1,1].pcolormesh(X, Y, np.log10(tau), cmap = plt.cm.inferno, vmin=2, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax[1,1])

ax[1,1].set_xscale('log')
ax[1,1].set_yscale('log')

ax[1,1].set_xlim(min(l_N), max(l_N))
ax[1,1].set_ylim(min(l_eta), max(l_eta))

ax[1,1].set_xlabel('$N$')
ax[1,1].set_ylabel('$\eta$')

plt.show()