'''
ANALYSIS
Parameter space: resolutino time and energy per agent
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt

# Maze
from maze import maze

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 20
algo = 'Prims'

# l_runs = [1,2]
l_runs = []

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load fields ────────────────────────────────

F = storage(base_tag + 'fields')

l_dst = F['dst']
l_eta = F['eta']
f_tau = F['tau']
f_energy = F['energy']

# ─── Run filter ────────────────────────────────

# Runs
if l_runs is None or not len(l_runs):
  l_runs = np.arange(f_tau.shape[2])

f_tau = np.nanmean(f_tau[:,:,l_runs], axis=2)
f_energy = np.nanmean(f_energy[:,:,l_runs], axis=2)

# ═══ Figure ════════════════════════════════════════════════════════

plt.style.use('dark_background')
fig, ax = plt.subplots(1,2, figsize=(15,7))

# Colormap
cm = plt.cm.inferno

X, Y = np.meshgrid(l_dst, l_eta)

# ─── Resolution time ──────────────────────────────────────────────────────

c = ax[0].pcolormesh(X, Y, np.log10(f_tau), cmap=cm, vmin=2.5, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax[0])

# ─── Plot settings

# Labels
ax[0].set_title('resolution time')
ax[0].set_xlabel('density $d$')
ax[0].set_ylabel('kinetic parameter $\eta$')

# Axes limits
ax[0].set_xlim(np.min(l_dst), np.max(l_dst))
ax[0].set_ylim(np.min(l_eta), np.max(l_eta))

# Log scale
ax[0].set_xscale('log')
ax[0].set_yscale('log')

ax[0].set_box_aspect(1)

# ─── Energy ───────────────────────────────────────────────────────────────

c = ax[1].pcolormesh(X, Y, np.log10(f_energy), cmap=cm, rasterized=True)
fig.colorbar(c, ax=ax[1])

# ─── Plot settings

# Labels
ax[1].set_title('energy')
ax[1].set_xlabel('density $d$')
ax[1].set_ylabel('kinetic parameter $\eta$')

# Axes limits
ax[1].set_xlim(np.min(l_dst), np.max(l_dst))
ax[1].set_ylim(np.min(l_eta), np.max(l_eta))

# Log scale
ax[1].set_xscale('log')
ax[1].set_yscale('log')

ax[1].set_box_aspect(1)

plt.show()