'''
Dynamics in an open corridor
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

# Storage
S = storage('Corridor/open_speed.h5')

l_m = S['l_m']
l_eta = S['l_eta']
V = S['V']

xlim = [0.3, 50]

# ─── Figure ───────────────────────────────────────────────────────────────

plt.style.use('dark_background')
fig, ax = plt.subplots(1,1, figsize=(7,7))
cm = plt.cm.cool(np.linspace(0, 1, l_m.size))

for i, m in enumerate(l_m):

  # Guide line
  x = l_eta
  y = np.sqrt(m/x)

  # ax.plot(x, y, '-', color=cm[i])

  # # Points
  # ax.plot(x, V[:,i], '+', color=cm[i], label=f'm={m}')

  ax.plot(y, V[:,i], '+', color=cm[i], label=f'm={m}')

x = np.linspace(xlim[0], xlim[1], 100)
ax.plot(x, x/7.5, 'w--', label=f'guide')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(xlim)
ax.set_ylim(0.03, 1.5)

ax.set_xlabel('$\sqrt{m/\eta}$')
ax.set_ylabel('speed')
ax.legend()

ax.set_title(f'Open corridor')

plt.show()