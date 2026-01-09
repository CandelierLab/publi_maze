'''
Swarm profile (through time)
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

N = 1000
eta = 10

# Maximal time 
Tmax = 100

# ═══ Computation ══════════════════════════════════════════════════════════

n = np.zeros((Tmax, Tmax))
n[0,0] = N

for t in range(1,Tmax):

  # Profile
  for k in range(t+1):
    n[k,t] = n[k-1,t-1]**2/(n[k-1,t-1] + eta) + n[k,t-1]*eta/(n[k,t-1] + eta)

# ═══ Display ══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1, 2, figsize=(15,7))

# ─── Profiles

cm = plt.cm.spring(np.linspace(0, 1, 10))

for i,t in enumerate(range(0, Tmax, np.round(Tmax/10).astype(int))):
  ax[0].plot(n[:,t], '-', color=cm[i])

ax[0].set_yscale('log')
ax[0].set_ylim(1e-1, N)
ax[0].axhline(1, color='w', linestyle='--')

ax[0].set_xlabel('$x$')
ax[0].set_ylabel('$n_x^t$')

# ─── 2D map

# # # X, Y = np.meshgrid(np.log10(np.arange(Tmax)), np.log10(np.arange(Tmax)))
# # # X[X<0] = 0
# # # Y[Y<0] = 0
# # # c = ax[1].pcolormesh(X, Y, np.log10(n), cmap =  plt.cm.inferno, vmin=0, vmax=np.log10(N), rasterized=True)

ax[1].yaxis.set_inverted(True)
c = ax[1].pcolormesh(np.log10(n).T, cmap =  plt.cm.magma, vmin=0, vmax=np.log10(N), rasterized=True)
fig.colorbar(c, ax=ax[1])

# ax[1].set_xscale('log')
# ax[1].set_yscale('log')

ax[1].set_xlabel('$x$')
ax[1].set_ylabel('$t$')

# x = np.arange(Tmax)
# y = 5*x**0.5
# ax[1].plot(x, y, 'w--')

plt.show()