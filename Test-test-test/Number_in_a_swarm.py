'''
Number of agents in a swarm
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
Nmax = 100*a**2

l_eta = np.geomspace(1, 1000, 50)
l_x0 = np.geomspace(0.1, Nmax, 50)

# ═══ Computation ══════════════════════════════════════════════════════════

# fig, ax = plt.subplots(1,1)
fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

N = np.zeros((l_eta.size, l_x0.size))
Nt = np.zeros((l_eta.size, l_x0.size))

for i, eta in enumerate(l_eta):

  for j, x0 in enumerate(l_x0):

    Nt[i,j] = x0 + eta*np.log(eta)

    P = 1
    nk = 0

    for k in range(5000):

      xk = eta/(k + eta/x0)
      nk += xk
      bk = (xk/(xk+eta))**xk
      N[i,j] += nk*bk*P
      P *= 1-bk

# ═══ Figure ════════════════════════════════════════════════════════════════

X, Y = np.meshgrid(l_x0, l_eta)

# ─── L ────────────────────────────────────────────────────────────────────

c = ax[0].pcolormesh(X, Y, np.log10(N), vmin=-1, vmax=np.log10(Nmax), rasterized=True)
fig.colorbar(c, ax=ax[0])

ax[0].set_xscale('log')
ax[0].set_yscale('log'),

ax[0].set_xlabel('$x_0$')
ax[0].set_ylabel('$\eta$')
ax[0].set_title('Expected number of agents in a swarm ($log_{10}$)')

# ─── v ────────────────────────────────────────────────────────────────────

c = ax[1].pcolormesh(X, Y, np.log10(Nt), vmin=-1, vmax=np.log10(Nmax), rasterized=True)
fig.colorbar(c, ax=ax[1])

ax[1].set_xscale('log')
ax[1].set_yscale('log')

ax[1].set_xlabel('$x_0$')
ax[1].set_ylabel('$\eta$')
ax[1].set_title('Simplified expression ($log_{10}$)')

plt.show()