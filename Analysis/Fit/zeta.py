'''
Fits of zeta
'''

# Reset command window display
import os
os.system('clear')

# Standard packages
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

# suppress warnings
import warnings
warnings.filterwarnings('ignore')

# ═══ Functions ════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────
def fit_one(zeta, n_samples=100, display=False, ax=None):
  
   # ─── Prepare display

  show_at_the_end = False
  if display and ax is None:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(1,1, figsize=(7,7))
    show_at_the_end = True
    
  # ─── Computation ─────────────────────────────

  # Check numpyity
  zeta = np.array(zeta)

  # Initial point
  zeta_0 = zeta[0].item()

  # Resampling
  t = np.arange(zeta.size)
  ti = np.linspace(t[0], t[-1], n_samples)
  zi = np.interp(ti, t, zeta)
  zi[zi<zeta_0] = zeta_0
    
  def ffit(t, L, k, tau):
    return zeta_0 + L/(1 + np.exp((-k*(t-tau))))
 
  # ─── Initial tau

  # tau_init = zeta.size/4

  zh = (zeta[0]+zeta[-1])/2
  tau_init = zeta.size - np.argmax(zeta[::-1]<=zh) - 1

  fit_bounds = ([0, 0, tau_init/10], [1, 1, zeta.size])
  p0 = [0.5, 0.5, tau_init]

  try:

    param = curve_fit(ffit, ti, zi, p0=p0, bounds=fit_bounds)[0]

    L = param[0].item()
    k = param[1].item()
    tau = param[2].item()

  except:
    L = None
    k = None
    tau = None

  # ─── Display

  if display:
    ax.plot(zeta)
    ax.plot(ti, zi, '-')
    ax.plot(t, ffit(t, L, k, tau), 'r-')

    ax.axvline(tau_init, color='w', linestyle=':')

    # Display options
    ax.set_ylim(0,1)

    # Show
    if show_at_the_end: 
      plt.show()

  return zeta_0, L, k, tau

# ───────────────────────────────────────────────
def fit_many(Zeta, **kwargs):
    
  # Check numpyity
  Zeta = np.array(Zeta)

  N = Zeta.shape[0]

  # ─── Computation ─────────────────────────────

  zeta_0 = np.zeros(N)
  L = np.zeros(N)
  k = np.zeros(N)
  tau = np.zeros(N)

  for i in range(N):
    zeta = Zeta[i,:]    
    zeta_0[i], L[i], k[i], tau[i] = fit_one(zeta, **kwargs)

  return zeta_0, L, k, tau