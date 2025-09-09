'''
Dynamics in a periodic corridor
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Maze (graph)
from maze import corridor

# Engine
from engine import Engine
from GPU.GPU import GPU_engine
from agents import agents

# ═══ Parameters ═══════════════════════════════════════════════════════════

eta = 50

# Initial mass
m = 1000

# Initial density
d0 = 0

# Corridor length
a = 30

# Number of iterations
T = 100

# ──────────────────────────────────────────────────────────────────────────

# Maze
M = corridor(size=a, periodic=True)

# Inition position
ipos = np.round(a/2)

# ═══ Computation ══════════════════════════════════════════════════════════

# ─── Engine

E = Engine(M.graph)

# ─── Agents

E.agents = agents(E, m, eta)
E.agents.position = np.full(m, ipos, dtype=int)
E.agents.origin = np.full(m, ipos-1, dtype=int)

# ─── Simulation

E.store_success = False
E.steps = T

# Create GPU object
E.gpu = GPU_engine(E)
E.gpu.import_position = True

# Compute initial densities
E.gpu.compute_densities()

# ─── Histogram

bins = np.arange(a+1)
xbin = np.arange(a)
h = np.histogram(E.agents.position, bins=bins)[0]

# ──────────────────────────────────────────────────────────────────────────
def filter(y):

  N = y.size
  xi = np.linspace(0,N,1000)
  yi = np.interp(xi, np.arange(N), y)
  F = savgol_filter(yi, 100, 2, mode='nearest')
  return xi, F

# ═══ Figure ═══════════════════════════════════════════════════════════════

plt.style.use('dark_background')
fig, ax = plt.subplots(3,1, figsize=(7,7), gridspec_kw={'height_ratios': [1, 10, 10]})
plt.subplots_adjust(hspace=0.5)

# ─── First axis ────────────────────────────────

pimg = ax[0].imshow(np.reshape(h, (1,a)), vmin=0, vmax=2*m/a, cmap='RdBu_r')

ax[0].axis('off')
ax[0].set_title(f'step 0')

# ─── Second axis ───────────────────────────────

hist = ax[1].bar(xbin, h)

# ─── Filter

xi, Z = filter(h)
filt = ax[1].plot(xi, Z, 'r-')[0]

ppos = [xi[np.argmax(Z)] - ipos]
pmax = ax[1].axvline(ppos, color='w', linestyle=':')

# ─── Settings

ax[1].set_xlim(0, a)
ax[1].set_ylim(0, m/2)
ax[1].set_xlabel('position')
ax[1].set_ylabel('histogram')

# ─── Third axis ────────────────────────────────

pplt = ax[2].plot([0], ppos, '.-')[0]

ax[2].set_xlim(0, T)
ax[2].set_ylim(0, 100)

ax[2].set_xlabel('time step')
ax[2].set_ylabel('peak displacement')


# ──────────────────────────────────────────────────────────────────────────
def update(frame):

  global ppos, ipos

  # ─── Update engine

  if frame>0:
    E.update(frame)

  h = np.histogram(E.agents.position, bins=bins)[0]

  # ─── Density plot

  pimg.set_data(np.reshape(h, (1,a)))

  ax[0].set_title(f'step {frame}')

  # ─── Histogram

  for i, b in enumerate(hist):
    b.set_height(h[i])

  # ─── Find peak

  xi, Z = filter(h)
  filt.set_ydata(Z)

  pp = xi[np.argmax(Z)]
  ppos.append(pp - ipos)
  pmax.set_xdata([pp]*2)

  # ─── Speed

  pplt.set_xdata(np.arange(len(ppos)))
  pplt.set_ydata(np.unwrap(ppos, period=a))
  
ani = animation.FuncAnimation(fig=fig, func=update, 
                              frames=T, 
                              interval=100, 
                              repeat=False)


# ani.save('Movies/corridor_periodic.mp4')

plt.show()