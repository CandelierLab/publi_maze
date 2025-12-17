'''
Swarm-centered animation
'''

import os
import numpy as np
from scipy.ndimage import gaussian_filter1d
import anim

os.system('clear')

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, N, L):

    aspect_ratio = 1
    self.H = L/aspect_ratio/1.2

    super().__init__(window, boundaries=[[0,L], [-0.1*self.H, 1.1*self.H]])

    # ─── Definitions

    # Number of agents
    self.N = N

    # Corridor length
    self.L = L

    # Dynamic parameter
    self.eta = 5

    # x-positions
    # self.x = self.L/2*np.ones(self.N)
    self.bins = np.arange(self.L+1)
    self.xbins = (self.bins[1:]+self.bins[:-1])/2

    self.x = self.L*np.random.rand(self.N)
    self.y = np.linspace(0, self.H, self.N)

    # ─── Colormap
    self.cm = anim.colormap()

    # ─── Items

    for i in range(self.N):
      self.item[f'agent_{i}'] = anim.plane.circle(
        position = [self.x[i], self.y[i]],
        radius = 0.5,
        color = self.cm.qcolor(i/N)
      )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Density field
    D = np.histogram(self.x, bins=self.bins)[0].astype(float)
    
    # Smooth density field
    # D = gaussian_filter1d(D, 1, mode='wrap')

    for i in range(self.N):

      # Local density 
      d = np.interp(self.x[i], self.xbins, D)

      # Speed
      # v = d/(d + self.eta)*2
      v = self.eta/(d + self.eta)
      
      # Update position
      self.x[i] = (self.x[i] - v) % self.L
      y = self.y[i] #*d/5

      # Update view
      self.item[f'agent_{i}'].position = [self.x[i], y]
    
    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Swarm-centered animation')

# Add animation
W.add(Canva, N=100, L=50)

# Allow backward animation
W.allow_backward = False
W.allow_negative_time = False

W.show()