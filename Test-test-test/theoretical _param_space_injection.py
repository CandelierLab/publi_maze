'''
Theroretical param space, injection protocol
'''

# Reset command window display
import os
os.system('clear')

import numpy as np

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ═══ Parameters ═══════════════════════════════════════════════════════════

l_eta = np.geomspace(1, 1000, 51)
l_omega = np.geomspace(0.01, 10, 53)

chi = 0.67
lmbda = 37

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

omega, eta = np.meshgrid(l_omega, l_eta)

rho = omega*(1 + np.sqrt(1 + 4*eta/omega))/2

c = ax.pcolormesh(omega, eta, rho, vmin=0, vmax=10, rasterized=True)
# c = ax.pcolormesh(omega, eta, np.log10(rho), vmin=0, vmax=3, rasterized=True)
fig.colorbar(c, ax=ax)

# ─── Contour line

p_g = (rho*eta/(rho+eta)**2)**rho
val = [1/lmbda/chi]
ax.contour(omega, eta, p_g, val, colors='w', linestyles=':')

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlabel(r'$\omega$')
ax.set_ylabel(r'$\eta$')
ax.set_title(r'$\rho^\ast$')

plt.show()