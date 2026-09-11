'''
Theroretical param space, injection protocol -- with density fluctuations

The corridor is a zero-range process: each agent hops with p_m = rho/(rho+eta),
which depends only on its own site occupancy. Its stationary law is therefore a
product measure with single-site weights

    w(n) = z^n prod_{k=1..n} (k+eta)/k^2

and the ZRP identity <u(n)> = z fixes the fugacity to the injected flux, z = omega.
The gap probability of eq.(pgap) is then averaged over P(n) = w(n)/Z instead of
being evaluated at the mean density rho~ (mean-field), which is what shifts the
A/B boundary up in density and back to a slope of -1.
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

# Truncation of the occupancy distribution
n_max = 600

# ═══ Computation ══════════════════════════════════════════════════════════

fig, ax = plt.subplots(1,1)
# fig, ax = plt.subplots(1,2, figsize=(15,6))
# cm = plt.cm.turbo(np.linspace(0, 1, l_x0.size))

omega, eta = np.meshgrid(l_omega, l_eta)

rho = omega*(1 + np.sqrt(1 + 4*eta/omega))/2

c = ax.pcolormesh(omega, eta, rho, vmin=0, vmax=10, rasterized=True)
# c = ax.pcolormesh(omega, eta, np.log10(rho), vmin=0, vmax=3, rasterized=True)
fig.colorbar(c, ax=ax)

# ─── Occupancy distribution (zero-range process, fugacity z = omega)

n = np.arange(n_max+1).reshape(-1, 1, 1)

# log w(n), built as a cumulative sum over k = 1..n
log_w = np.concatenate((np.zeros((1,) + omega.shape),
                        np.cumsum(np.log(omega) + np.log(n[1:] + eta)
                                  - 2*np.log(n[1:]), axis=0)))

log_Z = np.max(log_w, axis=0) + np.log(np.sum(
  np.exp(log_w - np.max(log_w, axis=0)), axis=0))

P = np.exp(log_w - log_Z)

# ─── Gap probability

# Mean-field: eq.(pgap) evaluated at the mean density
p_g_mf = (rho*eta/(rho+eta)**2)**rho

# With fluctuations: eq.(pgap) averaged over P(n).
# The n = 0 term of the first factor is 1 (an already empty site stays empty),
# and it is what dominates at low density -- the mean field cannot produce it.
p_all_leave = np.sum(P*np.where(n > 0, (n/(n+eta))**np.maximum(n, 1), 1.), axis=0)
p_no_arrival = np.sum(P*(eta/(n+eta))**n, axis=0)

p_g = p_all_leave*p_no_arrival

# ─── Contour lines

# p_unfix = 1/2, i.e. lmbda*chi*p_g = 1 (one gap per step over the solution)
val = [1/lmbda/chi]

# Time-integrated variant: no gap over a whole solving time tau ~ 2(S-lmbda).
# Same slope, rho~* = 6.0 instead of 2.45.
# val = [1/lmbda/chi/(2*(400-lmbda))]

ax.contour(omega, eta, p_g_mf, val, colors='w', linestyles=':')
ax.contour(omega, eta, p_g, val, colors='w', linestyles='--')

# Both contours leave the frame through the bottom edge; this reports where they
# stand whatever the plotted range (lower l_omega to 1e-3 to see them in full).
print(f'{"eta":>8} | {"omega*":>10} {"rho~*":>6}  (fluct.) | {"omega*":>10} {"rho~*":>6}  (mean field)')
for i in range(0, l_eta.size, 5):
  out = [f'{l_eta[i]:8.1f}']
  for field in (p_g, p_g_mf):
    f = np.log(field[i,:]/val[0])
    s = np.flatnonzero(np.diff(np.sign(f)))
    if s.size:
      j = s[0]
      lw = np.log(l_omega)
      w = np.exp(lw[j] - f[j]*(lw[j+1]-lw[j])/(f[j+1]-f[j]))
      out.append(f'{w:10.4g} {w*(1+np.sqrt(1+4*l_eta[i]/w))/2:6.2f}')
    else:
      out.append(f'{"< grid":>10} {"":6}')
  print(' | '.join(out))

ax.set_xscale('log')
ax.set_yscale('log'),

ax.set_xlabel(r'$\omega$')
ax.set_ylabel(r'$\eta$')
ax.set_title(r'$\rho^\ast$   (: mean field,  -- with fluctuations)')

plt.show()
