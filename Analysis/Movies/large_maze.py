'''
ANALYSIS
Dynamics in a very large maze
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Maze (graph)
from maze import maze

# Engine
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Maze
algo = 'Prims'
a = 1000
seed = 0

p = [140, 400]
b = 30
sub = [p[0]-b, p[0]+b, p[1]-b, p[1]+b]

vmax = 50

fname = '/home/raphael/Science/Projects/CM/Maze/Movies/Large_1000.mp4'

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Load densities

S = storage(f'Large_maze/{algo}/run_a={a}_seed={seed}.h5')

# Steps
steps = np.concatenate((np.arange(0, 10000, 100),
                                np.arange(10000, 100000, 100),
                                np.arange(100000, 1000000, 1000),
                                np.arange(1000000, 2e7, 10000))).astype(int)

zeta = S['success'].flatten()

# ═══ Figure ════════════════════════════════════════════════════════

plt.style.use('dark_background')
fig, ax = plt.subplots(1, 2, figsize=(20, 10))

# Image
D = np.reshape(S[str(0)], (a,a))
Img = ax[0].imshow(D, vmin=0, vmax=vmax)
Sub = ax[1].imshow(D[sub[0]:sub[1], sub[2]:sub[3]], vmin=0, vmax=vmax)

ax[0].axis('off')
ax[1].axis('off')

ax[0].add_patch(plt.Rectangle((sub[2], sub[0]), 2*b, 2*b, ls="-", lw=2, ec="w", fc="none"))

ax[0].set_title(f'$\zeta={zeta[0]:.02f}$')
ax[1].set_title(f'step {0}')

# ───────────────────────────────────────────────
def update(frame):

  # if not frame: return

  i = str(steps[frame])

  D = np.reshape(S[i], (a,a))
  Img.set_array(D)
  Sub.set_array(D[sub[0]:sub[1], sub[2]:sub[3]])

  ax[0].set_title(f'$\zeta={zeta[steps[frame]]:.02f}$')  
  ax[1].set_title(f'step {i}')

ani = animation.FuncAnimation(fig=fig, 
                              func=update, 
                              frames=steps.size,
                              repeat=False)

ani.save(fname)

plt.show()
