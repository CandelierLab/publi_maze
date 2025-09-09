'''
JUST A MAZE

A demo to generate and visualize a maze.
NB: This is static, there is no agent involved.
'''

import os

from maze import maze

# Reset command window display
os.system('clear')

# ─── Maze

M = maze(size = 20, 
        algorithm = 'Prims',
        seed = 0)

M.create_LR_loop()       

# ─── Display 

# Show
M.show(disp_graph=False, disp_solution=True, disp_id=False)