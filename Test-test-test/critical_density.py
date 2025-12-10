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

l_eta = np.geomspace(1,1000,100)

niter = 5000

# ──────────────────────────────────────────────────────────────────────────

S = a**2
lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

N = np.zeros(l_eta.size)

for i, eta in enumerate(l_eta):

  n0 = eta/(eta+lmbd)

  nk = eta/(np.arange(niter+1) + eta/n0)

  Nk = 0
  dk = 1

  for k in range(niter):
   
    Nk += nk[k]
    bk = (nk[k]/(nk[k] + eta))**nk[k] * (eta/(nk[k+1] + eta))**nk[k+1]

    N[i] += Nk*bk*dk
    
    dk *= (1-bk)

dc = N/S

# Approximation
dc_ = l_eta/S*(1/(l_eta - lmbd) + np.log(1+l_eta/(l_eta - lmbd)))

fig, ax = plt.subplots(1,1)

ax.plot(l_eta, dc, '-')
ax.plot(l_eta, dc_, '--')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('$\eta$')
ax.set_ylabel('$d_c$')

plt.show()