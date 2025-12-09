'''
Probability of unfixing
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

rho_Prims = 0.67
a = 20

ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

# ──────────────────────────────────────────────────────────────────────────

n_dst = len(l_dst)
n_eta = len(l_eta)

lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

pu = np.zeros((n_eta, n_dst))

for i, eta in enumerate(l_eta):

  for j, dst in enumerate(l_dst):

    n = dst*a**2/lmbd
    p = n/(n+eta)
    g = (p*(1-p))**n

    pu[i,j] = lmbd*rho_Prims*g/2

    # b = 1-(1-g)**lmbd


# ═══ Figure ═══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)
cm = plt.cm.inferno

X, Y = np.meshgrid(l_dst, l_eta)

c = ax.pcolormesh(X, Y, np.log10(pu), cmap=cm, vmin=-10, vmax=0, rasterized=True)
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