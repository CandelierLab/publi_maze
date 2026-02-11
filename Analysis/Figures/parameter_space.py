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
from matplotlib.colors import LinearSegmentedColormap

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

# Computation limits
max_steps = int(1e5)
max_energy = int(1e5)

vmin_tau = 2.25
vmax_tau = 5

vmin_eng = 1.5
vmax_eng = 5

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

f_tau[np.isnan(f_tau)] = max_steps
f_energy[np.isnan(f_energy)] = max_energy

# ═══ Figure ════════════════════════════════════════════════════════

# ─── Colormap ──────────────────────────────────

# cdict = {'red':   [[0.0,  0.0, 0.0],
#                    [0.10, 0.0, 0.0],
#                    [0.15, 0.0, 0.0],
#                    [0.75, 1.0, 1.0],
#                    [1.0,  1.0, 1.0]],
#          'green': [[0.0,  1.0, 1.0],
#                    [0.10, 0.8, 0.8],
#                    [0.15, 0.2, 0.2],
#                    [0.40, 0.0, 0.0],
#                    [0.90, 1.0, 1.0],
#                    [1.0,  1.0, 1.0]],
#          'blue':  [[0.0,  1.0, 1.0],
#                    [0.10, 1.0, 1.0],
#                    [0.15, 0.8, 0.8],
#                    [0.75, 0.0, 0.0],
#                    [1.0,  1.0, 1.0]]}

cdict = {'red':   [[0.0,  0.0, 0.0],
                   [0.08, 0.0, 0.0],
                   [0.15, 0.0, 0.0],
                   [0.20, 0.0, 0.0],
                   [0.75, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'green': [[0.0,  0.0, 0.0],
                   [0.08, 0.0, 0.0],
                   [0.15, 0.8, 0.8],
                   [0.25, 0.2, 0.2],
                   [0.40, 0.0, 0.0],
                   [0.90, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'blue':  [[0.0,  0.0, 0.0],
                   [0.08, 0.0, 0.0],
                   [0.15, 1.0, 1.0],
                   [0.20, 0.8, 0.8],
                   [0.75, 0.0, 0.0],
                   [1.0,  1.0, 1.0]]}

cm = LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)
# cm = plt.cm.inferno

# ─── Figure ───────────────────────────────────────────────────────────────

fig, ax = plt.subplots(1,2, figsize=(15,7))

X, Y = np.meshgrid(l_dst, l_eta)

print(np.min(np.log10(f_tau)), np.min(np.log10(f_energy)))

print((np.min(np.log10(f_tau))-vmin_tau)/(vmax_tau - vmin_tau))
print((np.min(np.log10(f_energy))-vmin_eng)/(vmax_eng - vmin_eng))

# ─── Resolution time ───────────────────────────

c = ax[0].pcolormesh(X, Y, np.log10(f_tau), cmap=cm, vmin=vmin_tau, vmax=vmax_tau, rasterized=True)
fig.colorbar(c, ax=ax[0])

# ─── Plot settings

# Labels
ax[0].set_title('resolution time $\\tau$')
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

c = ax[1].pcolormesh(X, Y, np.log10(f_energy), cmap=cm, vmin=vmin_eng, vmax=vmax_eng, rasterized=True)
fig.colorbar(c, ax=ax[1])

# ─── Plot settings

# Labels
ax[1].set_title('energy/agent')
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