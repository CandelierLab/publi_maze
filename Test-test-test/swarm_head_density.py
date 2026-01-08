'''
Swarm head density
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

N = 100

l_eta = np.array([5])
# l_eta = np.geomspace(1,1000,100)

a = 20

# ──────────────────────────────────────────────────────────────────────────

S = a**2
lmbd = round(1.612*a**1.044)

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)

for eta in l_eta:

  l_k = np.arange(lmbd)

  # ─── Computed values

  l_n0 = N*np.ones(lmbd)
  for k in l_k:
    if k:
      l_n0[k] = l_n0[k-1]**2/(l_n0[k-1] + eta)

  print(l_n0)
  ax.plot(l_k, l_n0, '--')

  # ─── Compressed form

  l_n0 = N*np.ones(lmbd)

  for k in l_k:

    if not k: continue

    a = (1-eta/N)**k
    b = np.sum((eta/N)**np.arange(k*(k+1)/2))
    l_n0[k] = N*a/b

  ax.plot(l_k, l_n0, '+')

# print(l_n0)

# ═══ Display ══════════════════════════════════════════════════════════════

# # # fig, ax = plt.subplots(1,1)

# # # ax.plot(l_eta, dc, '-')
# # # ax.plot(l_eta, dc_, '--')

# # # ax.set_xscale('log')
# # # ax.set_yscale('log')

# # # ax.set_xlabel('$\eta$')
# # # ax.set_ylabel('$d_c$')

plt.show()