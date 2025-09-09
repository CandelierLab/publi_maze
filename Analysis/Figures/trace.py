'''
Zeta(t) traces + fit
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt

# Storage
from storage import storage
from Analysis.Fit.zeta import fit_one

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

algo = 'Prims'
a = 20

dst = 5
eta = 500

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = 'Traces' + os.sep + algo + os.sep + f'a={a}_density' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(4,2))
# fig, ax = plt.subplots(1,1, figsize=(8,4))

# ─── Load fields ────────────────────────────────

F = storage('Traces' + os.sep + 
            algo + os.sep + 
            f'a={a}_density={dst}_eta={eta}.h5')

zeta = F['success'].flatten()
zeta_0, L, K, tau = fit_one(zeta)

# ─── Plot

ax.plot(zeta, linewidth=3, color='k')

t = np.geomspace(10, 1e5, 10000)
ax.plot(t, zeta_0 + L/(1 + np.exp((-K*(t-tau)))), '--', color='r', linewidth=3, label=f'$d$={dst}')

# ═══ Figure ════════════════════════════════════════════════════════


ax.set_xscale('log')
ax.set_xlim(10, 1e5)

ax.set_ylim(0, 1)
ax.set_yticks([0, 0.5, 1])

ax.set_xlabel('step')
ax.set_ylabel('$\zeta$')

ax.set_aspect(1.5)
ax.legend()

plt.show()