'''
Swarm speed (Pmove as a function of x0 and eta)
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt


plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_x0 = np.geomspace(0.1, 100, 100)
l_eta = np.geomspace(1, 1000, 100)

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)
cm = plt.cm.turbo(np.linspace(0, 1, 256))

v = np.zeros((l_eta.size, l_x0.size))

for i, eta in enumerate(l_eta):

  for j, x0 in enumerate(l_x0):

    v[i,j] = x0/(x0+eta)

X, Y = np.meshgrid(l_x0, l_eta)

# c = ax.pcolormesh(X, Y, v, vmin=0, vmax=1, rasterized=True)
c = ax.pcolormesh(X, Y, np.log(v), rasterized=True)
fig.colorbar(c, ax=ax)

ax.set_xscale('log')
ax.set_yscale('log')
# ax.legend()

# ax.set_xlabel('$x_0$')
# ax.set_xlabel('$\eta$')
# ax.set_ylabel('$L$')

plt.show()