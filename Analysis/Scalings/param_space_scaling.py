'''
ANALYSIS

Scaling with the parameter space data
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import numpy as np
import re
import time
import matplotlib.pyplot as plt

# Maze
from maze import maze

# Fit
from Analysis.Fit.zeta import fit_many

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 20
algo = 'Prims'

# ─── Agents

# Parameters
ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

n_runs_max = 10

l_dst = [l_dst[40]]
l_eta = l_eta[8:41]
# l_eta = [l_eta[8]]

# print(l_eta)
# sys.exit()

# ──────────────────────────────────────────────────────────────────────────

n_dst = len(l_dst)
n_eta = len(l_eta)

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

plt.style.use('dark_background')
fig, ax = plt.subplots(1,1, figsize=(10,10))

for i, eta in enumerate(l_eta):

  for j, dst in enumerate(l_dst):

    print(f'dst={dst} ─ eta={eta}')
    tref = time.perf_counter()

    # Parameter dir
    p_dir = base_tag + f'density={dst:.03f} - eta={eta:.01f}'

    # ─── List runs

    p_dir = base_tag + f'density={dst:.03f} - eta={eta:.01f}'
    L = storage.list(p_dir)
    l_dir = [d for d in L if d.startswith('run ')]
    n_runs = len(l_dir)

    # ─── Scan runs ─────────────────────────────

    for fname in l_dir:

      # ─── Check fit

      run = int(fname[4:-3])
    
      S = storage(p_dir + os.sep + fname)

      if S['success'].size:
        '''
        At least one maze was solved
        '''

        # Fit
        z0, Z, k, tau = fit_many(S['success'])

        tau[np.isnan(tau)] = S['success'].shape[1]-1
        tau[tau>S['success'].shape[1]-1] = S['success'].shape[1]-1
        tau = np.round(tau).astype(int)        
        energy = np.mean(S['energy'][:, tau].flatten())/dst/a**2
      
      else:

        print('No maze solved for run', run)        
        continue

      ax.plot(np.ones(tau.shape)/eta, tau/eta, '.')
      break

ax.set_xscale('log')
ax.set_yscale('log')

plt.show()