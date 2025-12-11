'''
Probability of a breakup
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_eta = np.geomspace(1,100,10)
l_n0 = np.geomspace(1,1000,10)
        
kmax = 1000

a = 20
lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

K = np.arange(1, kmax+2)

fig, ax = plt.subplots(1,1)
# cm = plt.cm.turbo(np.linspace(0,1,l_eta.size))
cm = plt.cm.jet(np.linspace(0,1,l_n0.size))

for i, n0 in enumerate(l_n0):

  b = np.zeros(l_eta.size)

  for j, eta in enumerate(l_eta):

    nk = eta/(K + eta/n0)
    bk = np.zeros(kmax)
    for k in range(kmax):
      bk[k] = (nk[k]/(nk[k]+eta))**nk[k] * (eta/(nk[k+1]+eta))**nk[k+1]

    # ax.plot(K[:-1], bk, '-', color=cm[i], label=f'{eta:.02f}')

    b[j] = bk[lmbd]

  ax.plot(l_eta, b, '-', color=cm[i], label=f'{n0:.02f}')

ax.plot(l_eta, np.exp(-3.6*l_eta/lmbd), 'w--')

# ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()

# ax.set_xlabel('$k$')
# ax.set_ylabel('$b_k$')

ax.set_xlabel('$\eta$')
ax.set_ylabel('$b_\lambda$')


plt.show()