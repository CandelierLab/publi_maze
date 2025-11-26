'''
Number of agents in a swarm
'''

# Reset command window display
import os, sys
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
Nmax = 100*a**2

l_eta = np.logspace(0, 3, 4)
l_x0 = np.geomspace(1, Nmax, 50)

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

# x = np.logspace(-2, 3, 100)
# ax.plot(x, (x/(x+10))**x, '-')

# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.axhline(0.5, color='w', linestyle=':')

# plt.show()

# sys.exit()

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

for i, eta in enumerate(l_eta):

  x = l_x0
  y = N[i,:]
  # y = (y-y[0])/(y[-1]-y[0])

  ax.plot(x, y, '.-', label=f'{eta}')
  ax.plot(x, eta*np.log(x+1)+x, '--')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('$x_0$')
ax.set_ylabel('$N$')

ax.legend()

plt.show()