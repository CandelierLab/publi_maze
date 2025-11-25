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

l_eta = np.geomspace(1,1000,50)
# l_eta = np.array([100])

# ═══ Computation ══════════════════════════════════════════════════════════

l_x0 = np.geomspace(0.1, 100, 50)
# l_x0 = np.array([100])

# fig, ax = plt.subplots(1,1)
fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

L = np.zeros((l_eta.size, l_x0.size))
v = np.zeros((l_eta.size, l_x0.size))

for i, eta in enumerate(l_eta):

  for j, x0 in enumerate(l_x0):

    v[i,j] = x0/(x0+eta)

    P = 1

    for k in range(5000):

      xk = eta/(k + eta/x0)
      bk = (xk/(xk+eta))**xk
      L[i,j] += (k+1)*bk*P
      P *= 1-bk

# ═══ Figure ════════════════════════════════════════════════════════════════

X, Y = np.meshgrid(l_x0, l_eta)

# ─── L ────────────────────────────────────────────────────────────────────

c = ax[0].pcolormesh(X, Y, np.log10(L), vmin=0, vmax=3, rasterized=True)
fig.colorbar(c, ax=ax[0])

# Contour lines
a = np.array([20])
lambdas = 1.612*a**1.044
lambdas = [20]
ax[0].contour(X, Y, L, lambdas, colors='w', linestyles=':')

ax[0].set_xscale('log')
ax[0].set_yscale('log'),

ax[0].set_xlabel('$x_0$')
ax[0].set_ylabel('$\eta$')
ax[0].set_title('Expected swarm length ($log_{10}$)')

# ─── v ────────────────────────────────────────────────────────────────────

c = ax[1].pcolormesh(X, Y, np.log10(v), vmin=-4, vmax=0, rasterized=True)
fig.colorbar(c, ax=ax[1])

ax[1].set_xscale('log')
ax[1].set_yscale('log')

ax[1].set_xlabel('$x_0$')
ax[1].set_ylabel('$\eta$')
ax[1].set_title('Swarm head velocity ($log_{10}$)')

plt.show()