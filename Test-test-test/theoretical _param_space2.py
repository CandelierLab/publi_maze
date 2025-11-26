'''
Expectation of the swarm length
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
dmax = 100
Nmax = dmax*a**2

l_eta = np.geomspace(1, 1000, 50)
l_x0 = np.geomspace(0.1, Nmax, 100)
l_d = np.geomspace(0.1, dmax, 50)

# ──────────────────────────────────────────────────────────────────────────

K = np.log(a**2)/np.log(2)

# ═══ Computation ══════════════════════════════════════════════════════════

lmbd = round(1.612*a**1.044)

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

# ─── Colormap ──────────────────────────────────

cdict = {'red':   [[0.0,  0.0, 0.0],
                   [0.10, 0.0, 0.0],
                   [0.15, 0.0, 0.0],
                   [0.75, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'green': [[0.0,  1.0, 1.0],
                   [0.10, 0.8, 0.8],
                   [0.15, 0.2, 0.2],
                   [0.40, 0.0, 0.0],
                   [0.90, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'blue':  [[0.0,  1.0, 1.0],
                   [0.10, 1.0, 1.0],
                   [0.15, 0.8, 0.8],
                   [0.75, 0.0, 0.0],
                   [1.0,  1.0, 1.0]]}

cm = LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)

# ─── Computation ───────────────────────────────

pL = np.zeros((l_eta.size, l_d.size))
v = np.zeros((l_eta.size, l_d.size))
tau_agg = np.zeros((l_eta.size, l_d.size))

for i, eta in enumerate(l_eta):

  # ─── Get x0(d)

  # Expected swarm cardinality
  N = np.zeros(l_x0.size)

  for j, x0 in enumerate(l_x0):

    P = 1
    nk = 0

    for k in range(5000):

      xk = eta/(k + eta/x0)
      nk += xk
      bk = (xk/(xk+eta))**xk
      N[j] += nk*bk*P
      P *= 1-bk

  # Convert to density
  d = N/lmbd

  # Interpolation
  X0 = np.interp(l_d, d, l_x0)

  # ─── Probability of sufficient length + speed

  for j, x0 in enumerate(X0):

    # Head speed
    v[i,j] = x0/(x0+eta)

    # Aggregation time
    tau_agg[i,j] = 2*(a**2 - lmbd) # + K*eta - 1

    # Probability of sufficient length
    P = 1

    for k in range(lmbd):

      xk = eta/(k + eta/x0)
      bk = (xk/(xk+eta))**xk
      pL[i,j] += bk*P
      P *= 1-bk

# Proba to have at least a length of lambda
pL = 1-pL
pL[pL<1e-10] = 1e-10

# ═══ Figure ════════════════════════════════════════════════════════════════

X, Y = np.meshgrid(l_d, l_eta)

# ─── tau ────────────────────────────────────────────────────────────────────

tau = tau_agg/pL/v

c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, vmin=2.5, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax)

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlabel('$d$')
ax.set_ylabel('$\eta$')

plt.show()