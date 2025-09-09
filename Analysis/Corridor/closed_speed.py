'''
Dynamics in a closed corridor
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
import matplotlib.pyplot as plt

# Storage
from storage import storage

# ──────────────────────────────────────────────────────────────────────────

# Corridor length
l_a = [10, 30, 50]
l_a = [10, 30, 50]

xlim = [0.05, 10]

# ─── Figure ───────────────────────────────────────────────────────────────

plt.style.use('dark_background')
fig, ax = plt.subplots(1,1, figsize=(7,7))

for j, a in enumerate(l_a):

  # Storage
  S = storage(f'Corridor/closed_speed_a={a}.h5')

  l_m = S['l_m']
  l_eta = S['l_eta']
  V = S['V']

  cm = plt.cm.cool(np.linspace(0, 1, l_m.size))

  for i, m in enumerate(l_m):

    # Guide line
    x = l_eta
    # y = 1/a**0.5*(m/x)
    y = np.sqrt(m/x/a)
    # ax.plot(x, y, '-', color=cm[i])

    # # Points
    # ax.plot(x, V[:,i], '+', color=cm[i], label=f'm={m}')

    ax.plot(y, V[:,i], '+', color=cm[i], label=f'm={m}, a={a}')

x = np.linspace(xlim[0], xlim[1], 100)
ax.plot(x, x, 'w--', label=f'guide')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(0.05, 2)

ax.set_xlabel('$\eta$')
ax.set_ylabel('speed')
ax.legend()

ax.set_title(f'Closed corridor')
ax.grid(True)

plt.show()