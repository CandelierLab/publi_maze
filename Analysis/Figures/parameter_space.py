'''
Parameter space
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

algo = 'Prims'
a = 20

# Zeta random
zeta_r = maze.zeta_random(algo, a)

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)

# Base tag
base_tag = 'Parameter space' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load data ─────────────────────────────────

F = storage(base_tag + algo + os.sep + f'a={a}' + os.sep + 'fields')

l_dst = F['dst']
l_eta = F['eta']
f_tau = F['tau']

# F = storage(base_tag + 'expected' + os.sep + f'a={a} n_bins=200')

# th_N = F['N']
# th_eta = F['eta']
# th_v = F['v']
# th_L = F['L']

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(4.5, 4.5))

# ─── Colormap ──────────────────────────────────

cdict = {'red':   [[0.0,  0.0, 0.0],
                   [0.10, 0.0, 0.0],
                   [0.15, 0.0, 0.0],
                   [0.75, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'green': [[0.0,  1.0, 1.0],
                   [0.10, 0.8, 0.8],
                   [0.15, 0.2, 0.2],
                   [0.40, 0.0, 0.0],
                   [0.90, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'blue':  [[0.0,  1.0, 1.0],
                   [0.10, 1.0, 1.0],
                   [0.15, 0.8, 0.8],
                   [0.75, 0.0, 0.0],
                   [1.0,  1.0, 1.0]]}

cm = LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)

# ─── Plot ──────────────────────────────────────

# ─── Resolution time map

X, Y = np.meshgrid(l_dst, l_eta)

c = ax.pcolormesh(X, Y, np.log10(f_tau), cmap=cm, vmin=2.5, rasterized=True)
fig.colorbar(c, ax=ax)

# ─── Model guidelines

# # # th_d = th_N/a**2
# # # th_X, th_Y = np.meshgrid(th_d, th_eta)

# # # # Expected length
# # # plt.contour(th_X, th_Y, th_L, levels=[lmbd], colors='k', linestyles='--')

# # # # Speed contour
# # # plt.contour(th_X, th_Y, th_v, levels=[0.5], colors='k', linestyles=':')

# ─── Plot settings

# Labels
ax.set_xlabel('density $d$')
ax.set_ylabel('kinetic parameter $\eta$')

# Axes limits
ax.set_xlim(np.min(l_dst), np.max(l_dst))
ax.set_ylim(np.min(l_eta), np.max(l_eta))

# Log scale
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_box_aspect(1)

plt.show()