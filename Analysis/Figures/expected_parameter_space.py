'''
Expectation of the paremeter space
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
from scipy.special import lambertw

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20

l_eta = np.geomspace(1, 1000, 50)
l_d = np.geomspace(0.1, 100, 50)

# ═══ Computation ══════════════════════════════════════════════════════════

lmbd = round(1.612*a**1.044)
print(f'a={a}, lambda={lmbd}, dmin={lmbd/a**2}')

def N2x0(N, eta):
  x = np.real(eta*lambertw(np.exp((N+1)/eta)/eta)-1)

  # Manage infinite values
  I = x==np.inf
  x[I] = N[I]

  return x

# ─── Computation ───────────────────────────────

pL = np.zeros((l_eta.size, l_d.size))  
L = np.zeros((l_eta.size, l_d.size))
v = np.zeros((l_eta.size, l_d.size))
tau_agg = np.zeros((l_eta.size, l_d.size))

for i, eta in enumerate(l_eta):

  l_x0 = N2x0(l_d*lmbd,eta)
  
  # ─── Probability of sufficient length + speed

  for j, x0 in enumerate(l_x0):

    # Head speed
    v[i,j] = x0/(x0+eta)

    # Aggregation time

    # S = 0
    # K = np.log2(a**2)
    # for k in range(int(K/2)):
    #   xk = N2x0(l_d[j]*2**k, eta)
    #   vk = xk/(xk+eta)
    #   S += 2**k/vk

    tau_agg[i,j] = 2*(a**2 - lmbd) # + K*eta - 1
    # tau_agg[i,j] = a**2 # + K*eta - 1

    # tau_agg[i,j] = S

    # Probability of sufficient length
    P = 1

    x = eta/(np.arange(lmbd+1) + eta/x0)

    for k in range(lmbd):

      bk = ((x[k]/(x[k]+eta))**x[k])*((eta/(x[k+1]+eta))**x[k+1])
      pL[i,j] += bk*P
      P *= 1-bk

    # for k in range(5000):

    #   xk = eta/(k + eta/x0)
    #   bk = (xk/(xk+eta))**xk
    #   L[i,j] += (k+1)*bk*P
    #   P *= 1-bk

# Proba to have at least a length of lambda
pL = 1-pL
pL[pL<1e-10] = 1e-10

# ─── tau ────────────────────────────────────────────────────────────────────

print(tau_agg[0,0], np.log10(tau_agg[0,0]))

tau = tau_agg/pL/v

# ═══ Figure ════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(5,5))

# ─── Colormap ──────────────────────────────────

# cdict = {'red':   [[0.0,  0.0, 0.0],
#                    [0.10, 0.0, 0.0],
#                    [0.15, 0.0, 0.0],
#                    [0.75, 1.0, 1.0],
#                    [1.0,  1.0, 1.0]],
#          'green': [[0.0,  1.0, 1.0],
#                    [0.10, 0.8, 0.8],
#                    [0.15, 0.2, 0.2],
#                    [0.40, 0.0, 0.0],
#                    [0.90, 1.0, 1.0],
#                    [1.0,  1.0, 1.0]],
#          'blue':  [[0.0,  1.0, 1.0],
#                    [0.10, 1.0, 1.0],
#                    [0.15, 0.8, 0.8],
#                    [0.75, 0.0, 0.0],
#                    [1.0,  1.0, 1.0]]}

# cm = LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)
cm = plt.cm.inferno

X, Y = np.meshgrid(l_d, l_eta)

# ─── Expected swarm length ─────────────────────

# ax = axes[0,0]

# c = ax.pcolormesh(X, Y, L, cmap = cm, vmin=0, vmax=5, rasterized=True)
# # c = ax.pcolormesh(X, Y, np.log10(L), cmap = cm, rasterized=True)
# fig.colorbar(c, ax=ax)

# ax.set_xscale('log')
# ax.set_yscale('log'),

# ax.set_xlabel('$d$')
# ax.set_ylabel('$\eta$')

# ax.set_box_aspect(1)

# ─── Swarm speed ───────────────────────────────

# ax = axes[0,1]

# c = ax.pcolormesh(X, Y, np.log10(v), cmap = cm, rasterized=True)
# # c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, rasterized=True)
# fig.colorbar(c, ax=ax)

# ax.set_xscale('log')
# ax.set_yscale('log'),

# ax.set_xlabel('$d$')
# ax.set_ylabel('$\eta$')

# ax.set_box_aspect(1)

# ─── Resolution time ───────────────────────────

# ax = axes[1,0]

# c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, vmin=0, vmax=15, rasterized=True)
c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, vmin=2.5, vmax=5, rasterized=True)
fig.colorbar(c, ax=ax)

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlabel('$d$')
ax.set_ylabel('$\eta$')

ax.set_box_aspect(1)

plt.show()