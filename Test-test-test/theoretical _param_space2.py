'''
Expectation of the swarm length
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
dmax = 100
Nmax = dmax*a**2

l_eta = np.geomspace(1, 1000, 50)
l_x0 = np.geomspace(0.1, Nmax, 100)
l_d = np.geomspace(0.1, dmax, 50)

# ═══ Computation ══════════════════════════════════════════════════════════

lmbd = round(1.612*a**1.044)

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

pL = np.zeros((l_eta.size, l_d.size))
v = np.zeros((l_eta.size, l_d.size))

for i, eta in enumerate(l_eta):

  # ─── Get x0(d)

  # Expected swarm cardinality
  N = np.zeros(l_x0.size)

  for j, x0 in enumerate(l_x0):

    P = 1
    nk = 0

    for k in range(5000):

      xk = eta/(k + eta/x0)
      nk += xk
      bk = (xk/(xk+eta))**xk
      N[j] += nk*bk*P
      P *= 1-bk

  # Convert to density
  d = N*10/a**2

  # Interpolation
  X0 = np.interp(l_d, d, l_x0)

  # ─── Probability of sufficient length + speed

  for j, x0 in enumerate(X0):

    # Head speed
    v[i,j] = x0/(x0+eta)

    # Probability of sufficient length
    P = 1

    for k in range(lmbd):

      xk = eta/(k + eta/x0)
      bk = (xk/(xk+eta))**xk
      pL[i,j] += bk*P
      P *= 1-bk

# Proba to have at least a length of lambda
pL = 1-pL
pL[pL<1e-10] = 1e-10

# ═══ Figure ════════════════════════════════════════════════════════════════

X, Y = np.meshgrid(l_d, l_eta)

# ─── L ────────────────────────────────────────────────────────────────────

c = ax.pcolormesh(X, Y, np.log10(1/pL/v*a**2), vmin=2.5, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax)

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlabel('$d$')
ax.set_ylabel('$\eta$')

plt.show()