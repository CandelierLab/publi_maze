'''
Dynamics in a periodic corridor
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

# Maze (graph)
from maze import corridor

# Engine
from engine import Engine
from GPU.GPU import GPU_engine
from agents import agents

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_m = np.geomspace(50, 1000, 5, dtype=int)
l_eta = np.geomspace(0.1, 200, 50)

# Number of iterations
T = 100

# Number of runs (for averaging)
n_runs = 10

# ──────────────────────────────────────────────────────────────────────────

# Corridor length
a = 2*T

# Storage
S = storage('Corridor/open_speed.h5')

# Maze
M = corridor(size=a, periodic=True)

# Initial position
ipos = T

# ═══ Computation ══════════════════════════════════════════════════════════

# if S.exists: sys.exit()

# ──────────────────────────────────────────────────────────────────────────
def filter(y):

  N = y.size
  xi = np.linspace(0,N,1000)
  yi = np.interp(xi, np.arange(N), y)
  F = savgol_filter(yi, 100, 2, mode='nearest')
  return xi, F

# ──────────────────────────────────────────────────────────────────────────
def linear(x, a, b):
  return a*x+b

V = np.zeros((l_eta.size, l_m.size))

for i, m in enumerate(l_m):

  for j, eta in enumerate(l_eta):

    print(f'm={m}, eta={eta}')

    v = np.zeros(n_runs)

    for k in range(n_runs):

      # ─── Engine

      E = Engine(M.graph)

      # ─── Agents

      E.agents = agents(E, m, eta)
      E.agents.position = np.full((1,m), ipos, dtype=int)
      E.agents.origin = np.full((1,m), ipos-1, dtype=int)

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
      xbin = np.arange(a) + 0.5
      h = np.histogram(E.agents.position, bins=bins)[0]

      # ─── Filter

      xi, Z = filter(h)
      E.ppos = np.zeros(T)
      E.ppos[0] = xi[np.argmax(Z)] - ipos
      
      # ──────────────────────────────────────────────────────────────────────────
      def update(frame):

        global ipos

        # ─── Update engine

        if frame>0:
          E.update(frame)

        h = np.histogram(E.agents.position, bins=bins)[0]
        xi, Z = filter(h)
        E.ppos[frame+1] = xi[np.argmax(Z)] - ipos

      # ─── Main loop ────────────────────────────────────────────────────────

      # Start run
      E.running = True

      for step in range(E.steps-1):
        update(step)

      # End run
      E.end()

      # ─── Velocity fit ─────────────────────────────────────────────────────

      popt, pcov = curve_fit(linear, np.arange(T), np.unwrap(E.ppos, period=a))
      v[k] = popt[0]

    # Median speed
    V[j,i] = np.median(v)

# ─── Save ───────────────────────────────────────────────────────────────

S['l_m'] = l_m
S['l_eta'] = l_eta
S['V'] = V