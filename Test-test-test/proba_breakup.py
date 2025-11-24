'''
Probability of a breakup
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_eta = np.geomspace(1,10,10)

# ═══ Computation ══════════════════════════════════════════════════════════

d = np.arange(1, 10000)

fig, ax = plt.subplots(1,1)
cm = plt.cm.turbo(np.linspace(0,1,l_eta.size))


for i, eta in enumerate(l_eta):

  y = (d/(d+eta))**d

  ax.plot(d, y, '-', color=cm[i], label=f'{eta:.02f}')


ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()

ax.set_xlabel('$d$')
ax.set_ylabel('$p_{b}$')

plt.show()