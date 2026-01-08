'''
Expectation of the paremeter space
'''

# Reset command window display
import os, sys
os.system('clear')

import numpy as np
from scipy.special import lambertw

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
rho_Prims = 0.67

l_eta = np.geomspace(1, 10000, 50)
l_d = np.geomspace(0.01, 1000, 50)

# l_eta = np.array([100])
# l_d = np.array([1])

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
tau = np.zeros((l_eta.size, l_d.size))
K = np.zeros((l_eta.size, l_d.size))

N_explo = (a**2 - lmbd)

# l_n0 = 100*np.ones(50)
# l_n0 = l_d*lmbd

for i, eta in enumerate(l_eta):

  for j, d in enumerate(l_d):

    for k in range(100):

      tau_m = 2**k
      n0 = d*2**k

      # Head speed
      v = n0/(n0+eta)

      # Probability of insufficient length
      P = 1
      p_il = 0
      x = eta/(np.arange(lmbd+1) + eta/n0)
      
      for l in range(lmbd):

        bk = ((x[l]/(x[l]+eta))**x[l])*((eta/(x[l+1]+eta))**x[l+1])
        p_il += bk*P
        P *= 1-bk

      # ─── Probability of unfixing

      # n = d*a**2/lmbd
      # p = n/(n+eta)
      # g = (p*(1-p))**n

      # p_u = lmbd*rho_Prims*g/2
      # tau_u = 1/p_u

      # ─── Probability of sufficient length + speed

      p_l = (1-p_il)
      if p_l<1e-20: p_l = 1e-20

      tau_l = N_explo/v/p_l

      # print('k', k, 'n0', n0, 'tau_m', tau_m, 'tau_l', tau_l, 'p_l', p_l)

      if tau_l>tau_m: # or tau_u<tau_m:
        # Iterate
        tau[i,j] += tau_m
        # pass

      else:
        # Keep resolution time
        K[i,j] += k
        tau[i,j] += tau_l
        break
        
    # sys.exit()

# sys.exit()

# Proba to have at least a length of lambda
# pL = 1-pL
# pL[pL<1e-20] = 1e-20

# ═══ Swarm length limit ═══════════════════════════════════════════════════

# # ─── In density

# N = np.zeros(l_eta.size)

# for i, eta in enumerate(l_eta):

#   n0 = eta/(eta+lmbd)

#   nk = eta/(np.arange(niter+1) + eta/n0)

#   Nk = 0
#   dk = 1

#   for k in range(niter):
   
#     Nk += nk[k]
#     bk = (nk[k]/(nk[k] + eta))**nk[k] * (eta/(nk[k+1] + eta))**nk[k+1]
#     N[i] += Nk*bk*dk    
#     dk *= (1-bk)

# d_frag = N/a**2

# ═══ Fixing limit ═════════════════════════════════════════════════════════

# d_c_fx = lmbd/a**2

# ─── tau ────────────────────────────────────────────────────────────────────

# tau = N_explo/pL/v

# ═══ Figure ════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1, figsize=(7,7))
cm = plt.cm.inferno

X, Y = np.meshgrid(l_d, l_eta)

# ─── Resolution time ───────────────────────────

c = ax.pcolormesh(X, Y, np.log10(tau), cmap = cm, vmin=2.5, vmax=5, rasterized=True)
# c = ax.pcolormesh(X, Y, K, rasterized=True)

# plt.contour(X, Y, tau, levels=[2.5*(a**2-lmbd)], colors='w', linestyles=':')
fig.colorbar(c, ax=ax)

# ─── Swarm length limit ────────────────────────

# ax.plot(d_frag, l_eta, ':', color='k')

# ─── Unfixing limit ────────────────────────────

# ax.axvline(d_c_fx, linestyle='--', color='k')

# ─── Plot parameters ───────────────────────────

ax.set_xlabel('$d$')
ax.set_ylabel('$\eta$')

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlim(min(l_d), max(l_d))
ax.set_ylim(min(l_eta), max(l_eta))


ax.set_box_aspect(1)

plt.show()