'''
Expected parameter space
'''

# Reset command window display
import os, sys
os.system('clear')

import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar

# Storage
from storage import storage

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
d_deadend_loop = 10

n_bins = 200

l_eta = np.geomspace(1, 1000, n_bins)
l_N = np.geomspace(10, 10000, n_bins)

# l_N = np.array([10])
# l_eta = np.array([1000])

tmax = 100000

# Base tag
base_tag = 'Parameter space' + os.sep + 'expected' + os.sep

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)
Lmbd = lmbd + d_deadend_loop

# ═══ Computation ══════════════════════════════════════════════════════════

# Storage
out = storage(base_tag + f'a={a} n_bins={n_bins}')

out['N'] = l_N
out['eta'] = l_eta

v = np.zeros((l_eta.size, l_N.size))
L = np.zeros((l_eta.size, l_N.size))
p_lmbd = np.zeros((l_eta.size, l_N.size))
p_mob = np.zeros((l_eta.size, l_N.size))

with alive_bar(l_eta.size*l_N.size) as bar:
    
  for i, eta in enumerate(l_eta):

    for j, N in enumerate(l_N):

      # ─── Profile @ L ──────────────────────────────────────────────────────

      t = 0
      n_ = np.array([N, 0])

      while t<tmax:

        t += 1
        n = np.zeros(t+1)
 
        n_1 = np.roll(n_,1)
        n = n_1**2/(n_1 + eta) + n_*eta/(n_ + eta)
        
        # Stop condition
        if np.argmax(n)>=Lmbd: break

        # Update reference
        n_ = np.append(n, 0)

      if t==tmax:
        v[i,j] = 0
        L[i,j] = Lmbd
        p_lmbd[i,j] = 1
        continue

      # Proportion of mobile agents
      pmob = np.sum(n[n>=eta])/N

      # Profile
      n = np.flip(n[:Lmbd+1])

      # ─── Velocity ─────────────────────────────────────────────────────────

      v[i,j] = n[0]/(n[0] + eta)

      # ─── Expected length, proba of insufficient length ────────────────────

      # Initialization
      l = 0
      p_il = 0
      P = 1

      for k in range(Lmbd):

        bk = ((n[k]/(n[k]+eta))**n[k])*((eta/(n[k+1]+eta))**n[k+1])

        # print(k, bk, P)

        # Expected length
        l += k*bk*P

        # Proba of insufficient length
        if k<=lmbd: 
          p_il += bk*P

        # Update aggregator
        P *= 1-bk

      # Expected length
      L[i,j] = l + Lmbd*P

      # ─── Probability of length at least lambda ────────────────────────────

      p_lmbd[i,j] = 1 - p_il

      # ─── Proportion of mobile agents ──────────────────────────────────────

      p_mob[i,j] = pmob

      bar()

# Storage
out['v'] = v
out['L'] = L
out['p_lmbd'] = p_lmbd
out['p_mob'] = p_mob

# ═══ Display ══════════════════════════════════════════════════════════════

# fig, ax = plt.subplots(1, 1, figsize=(7,7))

# ax.plot(n)

# plt.show()