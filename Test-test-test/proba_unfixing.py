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

eta = 50
n = np.unique(np.round(np.linspace(1, 100, 10)))

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)
d = n*lmbd/a**2

# ═══ Computation ══════════════════════════════════════════════════════════

d = 4
n = d*a**2/lmbd

p = n/(n+eta)
g = (p*(1-p))**n

print(lmbd*rho_Prims*g/2)

b = 1-(1-g)**lmbd


# ═══ Figure ═══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)

ax.plot(d, lmbd*rho_Prims*g/2, '.-')
# ax.plot(n, np.exp(-n), 'r-')

# ax.plot(n, b, 'r.-')

# x = np.linspace(0,1,100)
# K = np.array([100])
# cm = plt.cm.summer(np.linspace(0,1,K.size))
# for ki, k in enumerate(K):
#   ax.plot(x, 1-(1-x)**k, color=cm[ki])
#   ax.plot(x, x/(x+1/k), '--', color=cm[ki])


# ax.set_xscale('log')
ax.set_yscale('log')

plt.show()