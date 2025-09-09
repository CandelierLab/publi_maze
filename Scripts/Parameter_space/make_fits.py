'''
Make the fits
'''

# Reset command window display
import os, sys
os.system('clear')

# Standard packages
import numpy as np
import re
import time
# Maze
from maze import maze

# Fit
from Analysis.Fit.zeta import fit_many

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# ─── Maze

a = 10

# algo = 'AldousBroder'
# algo = 'BacktrackingGenerator'
# algo = 'BinaryTree'
# algo = 'Division'
# algo = 'GrowingTree'
# algo = 'HuntAndKill'
# algo = 'Kruskal'
algo = 'Prims'
# algo = 'Sidewinder'
# algo = 'Wilsons'

# ─── Agents

# Parameters
ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

# Zeta random
zeta_r = maze.zeta_random(algo, a)

# ──────────────────────────────────────────────────────────────────────────

n_dst = len(l_dst)
n_eta = len(l_eta)

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

# Storage
out = storage(base_tag + 'fields')

out['dst'] = l_dst
out['eta'] = l_eta

f_solved = np.zeros((n_eta, n_dst))
f_z0 = np.zeros((n_eta, n_dst))
f_Z = np.zeros((n_eta, n_dst))
f_tau = np.zeros((n_eta, n_dst))

for i, eta in enumerate(l_eta):

  for j, dst in enumerate(l_dst):

    print(f'dst={dst} ─ eta={eta} ', end='', flush=True)
    tref = time.perf_counter()

    # ─── List runs

    p_dir = base_tag + f'density={dst:.03f} - eta={eta:.01f}'
    L = storage.list(p_dir)
    l_dir = [d for d in L if d.startswith('run ')]
    n_runs = len(l_dir)

    # ─── Fit and aggregate data

    l_z0 = np.empty(0)
    l_Z = np.empty(0)
    l_k = np.empty(0)
    l_tau = np.empty(0)

    for fname in l_dir:

      S = storage(p_dir + os.sep + fname)

      z0, Z, k, tau = fit_many(S['success'])

      l_z0 = np.concatenate((l_z0, z0))
      l_Z = np.concatenate((l_Z, Z))
      l_k = np.concatenate((l_k, k))
      l_tau = np.concatenate((l_tau, tau))

    # ─── Compute fields

    f_solved[i,j] = 1 - np.count_nonzero(np.isnan(l_tau))/l_tau.size
    f_z0[i,j] = np.nanmean(l_z0)
    f_Z[i,j] = np.nanmean(l_Z)
    f_tau[i,j] = np.nanmean(l_tau)

    print(f' {time.perf_counter()-tref:.02f} sec')

out['solved'] = f_solved
out['z0'] = f_z0
out['Z'] = f_Z
out['tau'] = f_tau

    