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

a = 20
lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

l_x0 = np.geomspace(0.1, 100, 50)
# l_x0 = np.array([100])

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(12,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

L = np.zeros((l_eta.size, l_x0.size))

for i, eta in enumerate(l_eta):

  for j, x0 in enumerate(l_x0):

    P = 1

    y = []

    for k in range(5000):

      xk = eta/(k + eta/x0)
      bk = (xk/(xk+eta))**xk
      L[i,j] += (k+1)*bk*P
      P *= 1-bk

    #   y.append(L[i,j])

    # ax.plot(y, '.-')

# # # cm = plt.cm.turbo(np.linspace(0, 1, l_eta.size))

# # # for i, eta in enumerate(l_eta):

# # #   ax[0].plot(l_x0, L[i,:], '-', color=cm[i], label=f'{eta:.02f}')

# # #   ax[0].set_xlabel('$x_0$')
# # #   ax[0].set_ylabel('$L$')

# # # ax[0].set_xscale('log')
# # # # ax[0].set_yscale('log')

# # # cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

# # # for i, x0 in enumerate(l_x0):

# # #   ax[1].plot(l_eta, L[:,i], '-', color=cm[i], label=f'{eta:.02f}')

# # #   ax[1].set_xlabel('$\eta$')
# # #   ax[1].set_ylabel('$L$')

# # # ax[1].plot(l_eta, l_eta, 'w:')

X, Y = np.meshgrid(l_x0, l_eta)

# c = ax.pcolormesh(X, Y, v, vmin=0, vmax=1, rasterized=True)
c = ax.pcolormesh(X, Y, np.log10(L), rasterized=True)
fig.colorbar(c, ax=ax)

plt.contour(X, Y, L, levels=[4], colors='w', linestyles=':')


ax.set_xscale('log')
ax.set_yscale('log')

# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.legend()

# ax.set_xlabel('$x_0$')
# ax.set_xlabel('$\eta$')
# ax.set_ylabel('$L$')

plt.show()