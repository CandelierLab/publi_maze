'''
ANALYSIS
Parameter space for loops
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

# ─── Corridor

lmbd = 37

ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

# l_dst = np.array([10])
# l_eta = np.array([10])

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = f'Loop a={lmbd}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

strg = storage(base_tag + f'xi.h5')

if strg.exists():

  xi = strg['xi']

else:

  # Fixing ratio
  xi = np.full((l_eta.size, l_dst.size), fill_value=np.nan)

  for i, eta in enumerate(l_eta):

    tshift = int(eta*lmbd)

    for j, dst in enumerate(l_dst):

      # ─── Storage ─────────────────────────────

      S = storage(base_tag + f'density={dst:.03f} - eta={eta:.01f}.h5')

      # Skip absent files
      if not S.exists(): continue

      # Load blanks
      Nb = S['blanks'][:, tshift:]

      # Compute fixing ratio xi
      xi[i,j] = np.count_nonzero(Nb==0)/Nb.size

      print('Computing', i,j)

  # Store
  strg['xi'] = xi

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(7,7))

# ─── Plot ──────────────────────────────────────

X, Y = np.meshgrid(l_dst, l_eta)

c = ax.pcolormesh(X, Y, xi, vmin=0, vmax=1, rasterized=True)
# c = ax.pcolormesh(X, Y, np.log10(xi), vmin=-10, vmax=0, rasterized=True)
fig.colorbar(c, ax=ax)

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