'''
Parameter space demo
'''

# Reset command window display
import os
os.system('clear')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.image import imread
import matplotlib.animation as animation

# Storage
from storage import storage

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Maze
a = 20
algo = 'Prims'

m_d = np.array([1, 3, 9])
m_eta = np.array([20, 100, 500])

t = np.unique(np.round(np.geomspace(1, 1e5, 750)).astype(int))

# ──────────────────────────────────────────────────────────────────────────

# Base tag
base_tag = 'Parameter space' + os.sep

# Inset root
mdir = f'Movies/Parameter_space/Insets/'

# ═══ Computation ══════════════════════════════════════════════════════════

def movie_frame(d, eta, t):
  ifile = mdir + f'd={d}_eta={eta}/frame_{t}.png'
  return imread(ifile) if os.path.exists(ifile) else 0

# ─── Load data ─────────────────────────────────

F = storage(base_tag + algo + os.sep + f'a={a}' + os.sep + 'fields')

l_dst = F['dst']
l_eta = F['eta']
f_tau = F['tau']

# ═══ Figure ═══════════════════════════════════════════════════════════════

fig = plt.figure(constrained_layout=True, figsize=(14, 7))
subfigs = fig.subfigures(1, 2)

# ─── Parameter space ──────────────────────────────────────────────────────

ax_ = subfigs[0].subplots(1, 1)

# ─── Colormap

cdict = {'red':   [[0.0,  0.0, 0.0],
                   [0.10, 0.0, 0.0],
                   [0.15, 0.0, 0.0],
                   [0.75, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'green': [[0.0,  1.0, 1.0],
                   [0.10, 0.8, 0.8],
                   [0.15, 0.2, 0.2],
                   [0.40, 0.0, 0.0],
                   [0.90, 1.0, 1.0],
                   [1.0,  1.0, 1.0]],
         'blue':  [[0.0,  1.0, 1.0],
                   [0.10, 1.0, 1.0],
                   [0.15, 0.8, 0.8],
                   [0.75, 0.0, 0.0],
                   [1.0,  1.0, 1.0]]}

cm = LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)

# ─── Resolution time map

X, Y = np.meshgrid(l_dst, l_eta)

c = ax_.pcolormesh(X, Y, np.log10(f_tau), cmap=cm, vmin=2.5, rasterized=True)
fig.colorbar(c, ax=ax_, shrink=0.5, pad=0.02)

# Markers
i = 0
for eta in np.flip(m_eta):
  for d in m_d:
    ax_.scatter(d, eta, s=50, marker='x', color='k')
    ax_.text(d*0.75, eta*1.1, f'${chr(97+i)}$', fontsize=14)
    i += 1


# Labels
ax_.set_title('Resolution time $log_{10}(\\tau)$')
ax_.set_xlabel('density $d$')
ax_.set_ylabel('kinetic parameter $\eta$')

# Axes limits
ax_.set_xlim(np.min(l_dst), np.max(l_dst))
ax_.set_ylim(np.min(l_eta), np.max(l_eta))

# Log scale
ax_.set_xscale('log')
ax_.set_yscale('log')

ax_.set_box_aspect(1)

# ─── Mazes ────────────────────────────────────────────────────────────────

s_time = subfigs[1].suptitle(f't=0')
ax = subfigs[1].subplots(3,3)

Img = [[0,0,0],[0,0,0],[0,0,0]]

for i, d in enumerate(m_d):
  for j, eta in enumerate(m_eta):

    i_ = 2-j
    j_ = i

    img = movie_frame(d, eta, t[0])
    if isinstance(img, np.ndarray):

      Img[i][j] = ax[i_,j_].imshow(img)
      ax[i_,j_].set_axis_off()

      ax[i_,j_].text(0, -5, f'${chr(97+i+(2-j)*3)}$', fontsize=14)

    # break
  # break

# ──────────────────────────────────────────────────────────────────────────
def update(frame):

  s_time.set_text(f't={t[frame]}')

  # ─── Images

  for i, d in enumerate(m_d):
    for j, eta in enumerate(m_eta):

      img = movie_frame(d, eta, t[frame])

      if isinstance(img, np.ndarray):
        Img[i][j].set_array(img)

      # break
    # break

ani = animation.FuncAnimation(fig=fig, func=update, 
                              frames=t.size, 
                              interval=40,
                              repeat=False)

ani.save('Movies/parameter_space_demo.mp4')

plt.show()

