'''
Soliton density profiles, expected length and speed
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Storage
from storage import storage

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

a = 20
n_bins = 200

# ─── Routine

nps = 100
routine = []
for m in np.geomspace(30, 3000, nps):
  routine.append((m, 3))
for eta in np.geomspace(3, 300, nps):
  routine.append((3000, eta))
for m in np.flip(np.geomspace(30, 3000, nps)):
  routine.append((m, 300))
for eta in np.flip(np.geomspace(3, 300, nps)):
  routine.append((30, eta))

# ──────────────────────────────────────────────────────────────────────────

lmbd = round(1.612*a**1.044)
Lmbd = lmbd + 10

Tmax = 100

# Base tag
base_tag = 'Parameter space' + os.sep + 'expected' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load data ─────────────────────────────────

F = storage(base_tag + f'a={a} n_bins={n_bins}')

l_N = F['N']
l_eta = F['eta']
f_v = F['v']
f_L = F['L']
f_p_lmbd = F['p_lmbd']

def profile(N, eta):

  n = np.zeros((Tmax, Tmax))
  n[0,0] = N

  for t in range(1,Tmax):

    n_1 = np.roll(n[:,t-1],1)
    n[:,t] = n_1**2/(n_1 + eta) + n[:,t-1]*eta/(n[:,t-1] + eta)

  return n

# ═══ Figure ════════════════════════════════════════════════════════

fig, ax = plt.subplots(1, 3, figsize=(20,5))

# ─── Soliton Profile ───────────────────────────

N = routine[0][0]
eta = routine[0][1]

n = profile(N, eta)

ax[0].yaxis.set_inverted(True)
prof = ax[0].pcolormesh(np.log10(n).T, cmap =  plt.cm.magma, vmin=0, vmax=4, rasterized=True)
fig.colorbar(prof, ax=ax[0], shrink=0.75, pad=0.02, ticks=[0, 1, 2, 3, 4])

# Text
ax[0].text(12, 8, '─→', color='w', fontsize=10)

# Axes
ax[0].set_title('soliton density profile ($log_{10}(n)$)')
ax[0].set_xlabel('position $x$ (square)')
ax[0].set_ylabel('time $t$ (step)')

# ─── Soliton expected length ───────────────────

X, Y = np.meshgrid(l_N, l_eta)

c = ax[1].pcolormesh(X, Y, f_L, cmap = plt.cm.inferno, vmin=0, vmax=Lmbd, rasterized=True)

# Colorbar
cbar = fig.colorbar(c, ax=ax[1], shrink=0.75, pad=0.02, ticks=[0, 20, 40, Lmbd])
cbar.ax.set_yticklabels(['0', '20', '40', '$\Lambda$'])  # vertically oriented colorbar

# lambda
ax[1].contour(X, Y, f_L, levels=[lmbd], colors='k', linestyles='--')
ax[1].text(4000, 8, '$\ell = \lambda$', color='k', fontsize=14)

# Marker
marker_1 = ax[1].scatter(N, eta, s=100, marker='x', color='r')

# Axes
ax[1].set_xscale('log')
ax[1].set_yscale('log')

ax[1].set_xlim(min(l_N), max(l_N))
ax[1].set_ylim(min(l_eta), max(l_eta))

ax[1].set_title('expected length $\ell$ (square)')
ax[1].set_xlabel('total number $m$')
ax[1].set_ylabel('kinetic parameter $\eta$')

# ─── Soliton speed ─────────────────────────────

c = ax[2].pcolormesh(X, Y, f_v, cmap = plt.cm.inferno, vmin=0, vmax=1, rasterized=True)
fig.colorbar(c, ax=ax[2], shrink=0.75, pad=0.02, ticks=[0, 0.5, 1])

# Marker
marker_2 = ax[2].scatter(N, eta, s=100, marker='x', color='r')

# Axes
ax[2].set_xscale('log')
ax[2].set_yscale('log')

ax[2].set_xlim(min(l_N), max(l_N))
ax[2].set_ylim(min(l_eta), max(l_eta))

ax[2].set_title('soliton speed v (square/step)')
ax[2].set_xlabel('total number $m$')
ax[2].set_ylabel('kinetic parameter $\eta$')

# ──────────────────────────────────────────────────────────────────────────
def update(frame):

  # ─── Parameters

  N = routine[frame][0]
  eta = routine[frame][1]

  # ─── Profile

  prof.set_array(np.log10(profile(N, eta).T))
  
  # ─── Markers

  marker_1.set_offsets(routine[frame])
  marker_2.set_offsets(routine[frame])

ani = animation.FuncAnimation(fig=fig, func=update, 
                              frames=len(routine), 
                              interval=40, 
                              repeat=False)

# ani.save('Movies/profiles_length_speed.mp4')

fig.tight_layout()
plt.show()