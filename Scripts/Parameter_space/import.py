'''
Import run of the parameter space (for transfer)
'''

# Reset command window display
import os, sys
import shutil

from storage import storage

os.system('clear')

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Run
run = 2

a = 20
algo = 'Prims'

# Source folder

src = storage.root() + f'Parameter space/run_{run:02d}/'

# Destination folder

dest = storage.root() + f'Parameter space/{algo}/a={a}/'


# ══════════════════════════════════════════════════════════════════════════

# Check destination existence
if not os.path.exists(dest):
  os.makedirs(dest)

# ─── Scan source ───────────────────────────────

for D in os.listdir(src):
  
  file = src + D + os.sep + f'run {run:04d}.h5'

  print(D)

  # Move file
  if os.path.exists(file):
    shutil.move(file, dest + D)

  if not os.path.exists(file):
    os.rmdir(src + D)

  # sys.exit()

