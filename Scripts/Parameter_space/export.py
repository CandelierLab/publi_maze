'''
Export run of the parameter space (for transfer)
'''

# Reset command window display
import os, sys
import shutil

from storage import storage

os.system('clear')

# ═══ Parameters ═══════════════════════════════════════════════════════════

# Run
run = 1

a = 20
algo = 'Prims'

# Source folder

src = storage.root() + f'Parameter space/{algo}/a={a}/'

# Destination folder

dest = storage.root() + f'Parameter space/run_{run:02d}/'

# ══════════════════════════════════════════════════════════════════════════

# Check destination existence
if not os.path.exists(dest):
  os.makedirs(dest)

# ─── Scan source ───────────────────────────────

for D in os.listdir(src):

  if D == 'fields.h5': continue
  
  for d in os.listdir(src + D):

    # Check run correspondence
    if int(d[4:-3]) == run:
      
      print(D, d)

      # Make dir
      os.makedirs(dest + D, exist_ok=True)

      # Copy file
      shutil.copy2(src + D + os.sep + d, dest + D + os.sep + d) 

      # sys.exit()

