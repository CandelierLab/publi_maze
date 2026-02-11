'''
Make fits of zeta
Extract resolution time tau and energy per agent
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

a = 20
algo = 'Prims'

# ─── Agents

# Parameters
ndpd = 16
l_dst = np.round(np.logspace(-1, 2, ndpd*3+1)*1000)/1000
l_eta = np.round(np.logspace(0, 3, ndpd*3+1)*10)/10

n_runs_max = 10

# ──────────────────────────────────────────────────────────────────────────

n_dst = len(l_dst)
n_eta = len(l_eta)

# Base tag
base_tag = 'Parameter space' + os.sep + algo + os.sep + f'a={a}' + os.sep

# ═══ Computation ══════════════════════════════════════════════════════════

def set_value(F, key, val):
  F[key] = val
  return F

# Storage
F_global = storage(base_tag + 'fields')

F_global['dst'] = l_dst
F_global['eta'] = l_eta

f_solved = np.zeros((n_eta, n_dst, n_runs_max))
f_z0 = np.zeros((n_eta, n_dst, n_runs_max))
f_Z = np.zeros((n_eta, n_dst, n_runs_max))
f_tau = np.zeros((n_eta, n_dst, n_runs_max))
f_energy = np.zeros((n_eta, n_dst, n_runs_max))

for i, eta in enumerate(l_eta):

  for j, dst in enumerate(l_dst):

    print(f'dst={dst} ─ eta={eta} ', end='', flush=True)
    tref = time.perf_counter()

    # Parameter dir
    p_dir = base_tag + f'density={dst:.03f} - eta={eta:.01f}'

    # ─── Check fit file

    F_local = storage(p_dir + os.sep + 'fits.h5')
    if not F_local.exists():
      F_local['solved'] = np.full(n_runs_max, np.nan)
      F_local['z0'] = np.full(n_runs_max, np.nan)
      F_local['Z'] = np.full(n_runs_max, np.nan)
      F_local['tau'] = np.full(n_runs_max, np.nan)
      F_local['energy'] = np.full(n_runs_max, np.nan)

    # ─── List runs

    p_dir = base_tag + f'density={dst:.03f} - eta={eta:.01f}'
    L = storage.list(p_dir)
    l_dir = [d for d in L if d.startswith('run ')]
    n_runs = len(l_dir)

    # ─── Scan runs ─────────────────────────────

    for fname in l_dir:

      # ─── Check fit

      run = int(fname[4:-3])

      if np.isnan(F_local['solved'][run]):

        S = storage(p_dir + os.sep + fname)

        # print('success', S['success'])

        if S['success'].size:
          '''
          At least one maze was solved
          '''

          # Fit
          z0, Z, k, tau = fit_many(S['success'])

          solved = tau.size - np.count_nonzero(np.isnan(tau))
          F_local['solved'] = set_value(F_local['solved'], run, solved)
          F_local['z0'] = set_value(F_local['z0'], run, np.mean(z0))
          F_local['Z'] = set_value(F_local['Z'], run, np.mean(Z))
          F_local['tau'] = set_value(F_local['tau'], run, np.mean(tau))

          tau[np.isnan(tau)] = S['success'].shape[1]-1
          tau[tau>S['success'].shape[1]-1] = S['success'].shape[1]-1
          tau = np.round(tau).astype(int)        
          F_local['energy'] = set_value(F_local['energy'], run, np.mean(S['energy'][:, tau].flatten())/dst/a**2)
        
        else:
          
          F_local['solved'] = set_value(F_local['solved'], run, 0)
          
    # ─── Aggregate values ──────────────────────

    f_solved[i,j,:] = F_local['solved']
    f_z0[i,j,:] = F_local['z0']
    f_Z[i,j,:] = F_local['Z']
    f_tau[i,j,:] = F_local['tau']
    f_energy[i,j,:] = F_local['energy']

    print(f' {time.perf_counter()-tref:.02f} sec')

F_global['solved'] = f_solved
F_global['z0'] = f_z0
F_global['Z'] = f_Z
F_global['tau'] = f_tau
F_global['energy'] = f_energy

    