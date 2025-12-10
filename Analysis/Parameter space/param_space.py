'''
ANALYSIS
Kinetic average zeta curves and fit
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

# algo = 'AldousBroder'
# algo = 'BacktrackingGenerator'
# algo = 'BinaryTree'
# algo = 'Division'
# algo = 'GrowingTree'
# algo = 'HuntAndKill'
# algo = 'Kruskal'
algo = 'Prims'
# algo = 'Sidewinder'
# algo = 'Wilsons'

# Zeta random
zeta_r = maze.zeta_random(algo, a)

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load fields ────────────────────────────────

F = storage(base_tag + 'fields')

l_dst = F['dst']
l_eta = F['eta']
f_tau = F['tau']

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(7,7))

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

cm = LinearSegmentedColormap('colormap', segmentdata=cdict, N=256)

# ─── Plot ──────────────────────────────────────

X, Y = np.meshgrid(l_dst, l_eta)

c = ax.pcolormesh(X, Y, np.log10(f_tau), cmap=cm, vmin=2.5, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax)

# ─── critical density

lmbd = round(1.612*a**1.044)
dc = l_eta/a**2*(1/(l_eta + lmbd) + np.log(1+l_eta/(l_eta + lmbd)))

ax.plot(dc, l_eta, '--', color='k')

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