'''
"Critical" density
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20

eta = np.geomspace(1,1000,100)

# ──────────────────────────────────────────────────────────────────────────

S = a**2
lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

dc = eta/S*(1/(eta + lmbd) + np.log(1+eta/(eta + lmbd)))

fig, ax = plt.subplots(1,1)

ax.plot(eta, dc, '.-')


ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('$\eta$')
ax.set_ylabel('$d_c$')

plt.show()