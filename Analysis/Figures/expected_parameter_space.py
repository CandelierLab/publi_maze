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

l_eta = np.geomspace(1, 10000, 50)
l_d = np.geomspace(0.01, 1000, 50)

niter = 5000

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)

# ═══ Resolution time ══════════════════════════════════════════════════════

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
N_explo = np.zeros((l_eta.size, l_d.size))

for i, eta in enumerate(l_eta):

  l_x0 = N2x0(l_d*lmbd,eta)
  
  # ─── Probability of sufficient length + speed

  for j, x0 in enumerate(l_x0):

    # Head speed
    v[i,j] = x0/(x0+eta)

    # Exploration time
    N_explo[i,j] = 2*(a**2 - lmbd)

    # Probability of sufficient length
    P = 1

    x = eta/(np.arange(lmbd+1) + eta/x0)

    for k in range(lmbd):

      bk = ((x[k]/(x[k]+eta))**x[k])*((eta/(x[k+1]+eta))**x[k+1])
      pL[i,j] += bk*P
      P *= 1-bk

# Proba to have at least a length of lambda
pL = 1-pL
pL[pL<1e-10] = 1e-10

# ═══ Swarm length limit ═══════════════════════════════════════════════════

# ─── In density

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

d_c_ll = N/a**2

# ─── In eta

eta_c = np.zeros(l_d.size)

for i, d in enumerate(l_d):

  n0 = d*a**2
  eta_c[i] = lmbd*n0/(n0 - 1)

# ═══ Fixing limit ═════════════════════════════════════════════════════════

d_c_fx = lmbd/a**2

# ─── tau ────────────────────────────────────────────────────────────────────

tau = N_explo/pL/v

# ═══ Figure ════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(5,5))
cm = plt.cm.inferno

X, Y = np.meshgrid(l_d, l_eta)

# ─── Resolution time ───────────────────────────

c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, vmin=0, vmax=10, rasterized=True)

plt.contour(X, Y, tau, levels=[2.5*(a**2-lmbd)], colors='w', linestyles=':')
fig.colorbar(c, ax=ax)

# ─── Swarm length limit ────────────────────────

ax.plot(d_c_ll, l_eta, '--', color='k')

# ─── Unfixing limit ────────────────────────────

ax.axvline(d_c_fx, linestyle=':', color='k')

# ─── Low eta limit ─────────────────────────────

ax.plot(l_d, eta_c, '-.', color='k')

# ─── Plot parameters ───────────────────────────

ax.set_xlabel('$d$')
ax.set_ylabel('$\eta$')

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlim(min(l_d), max(l_d))
ax.set_ylim(min(l_eta), max(l_eta))


ax.set_box_aspect(1)

plt.show()