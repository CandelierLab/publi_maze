''' 
Maze

!! NB: this description is not up to date !!

─── Indexing ─────────────────────────────────────────────────────────────

The squares are indexed from bottom to top and left to right, starting at 0.
For instance:

┌─────────┬─────────┐
│ 12   13 │ 14   15 │
│    ─────┘    ─────┤
│ 8    9    10   11 │
│    ─────┬─────    │
│ 4    5  │ 6    7  │     
├─────    │    │    │     
│ 0    1    2  │ 3  │
└──────────────┴────┘

--- Loops & solutions

It is possible to add a loop with the `create_loop` method. Il automatically
defines a solution.

Each solution is represented by an array of cell indices starting from the 
lowest index and turning counterclockwise (trigonometric convention). In
the above exemple, the solution is thus [1, 2, 6, 7, 11, 10, 9, 8, 4, 5].

--- Sink

A special node (-1) can be added to act as a sink, i.e. agents arriving on 
this node are removed.

═══ entries mazes ════════════════════════════════════════════════════════

entries mazes have 2 entries. Without loss of generality, one entry is always
on the left side (input) and the other one is either on the right or top 
side (output). The terms 'input' and 'output' are used for internal 
computations and have no other meaning in general since both entries are
interchangeable.

--- Entry positions

The positions of the entries can be set at random or manually. The following
convention applies:

      9    8    7    6    5     ↰ 
      ▼    ▼    ▼    ▼    ▼    
    ┌────┬────┬────┬────┬────┐
4 ▶ │    │    │    │    │    │ ◀ 4
    ├────┼────┼────┼────┼────┤ 
3 ▶ │    │    │    │    │    │ ◀ 3
    ├────┼────┼────┼────┼────┤
2 ▶ │    │    │    │    │    │ ◀ 2 
    ├────┼────┼────┼────┼────┤
1 ▶ │    │    │    │    │    │ ◀ 1
    ├────┼────┼────┼────┼────┤
0 ▶ │    │    │    │    │    │ ◀ 0
    └────┴────┴────┴────┴────┘
↑                                ↑
in entry position                out entry position
(input_pos)                      (output_pos)

--- Solutions

Each solution is represented by an array of cell indices starting from the 
input entry index and ending by the output entry. In the exemple below, 
the solution is [4, 5, 1, 2, 6, 7, 11, 10, 14].

              ▼
  ┌─────────┐    ─────┐
  │ 12   13 │ 14   15 │
  │    ─────┘    ─────┤
  │ 8    9    10   11 │
  └─────────┬─────    │
▶   4    5  │ 6    7  │
  ┌─────    │    ─────┤
  │ 0    1    2    3  │
  └───────────────────┘
'''

# ─── Standard modules

import numpy as np
import warnings
import time

# ─── Maze generation

import networkx as nx
from graph import *
from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator
from mazelib.generate.BinaryTree import BinaryTree
# NB: CellularAutomaton creates mazes containing loops
from mazelib.generate.Division import Division
# NB: Ellers do not work for a>=20 (mazelib bug ?)
from mazelib.generate.GrowingTree import GrowingTree
from mazelib.generate.HuntAndKill import HuntAndKill
from mazelib.generate.Kruskal import Kruskal
from mazelib.generate.Prims import Prims
from mazelib.generate.Sidewinder import Sidewinder
from mazelib.generate.Wilsons import Wilsons

# ─── Visualization

import anim
import Animation.maze

class maze:

  # ────────────────────────────────────────────────────────────────────────
  @staticmethod
  def algorithms():
    return {
      'AldousBroder': AldousBroder,
      'BacktrackingGenerator': BacktrackingGenerator,
      'BinaryTree': BinaryTree,
      'Division': Division,
      'GrowingTree': GrowingTree,   # options: backtrack_chance=0.5
      'HuntAndKill': HuntAndKill,
      'Kruskal': Kruskal,
      'Prims': Prims,
      'Sidewinder': Sidewinder,
      'Wilsons': Wilsons,
      }

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, size=(5,5), algorithm=Prims, options=None, seed=None, verbose=False):
    '''
    Constructor

    Arguments
    * size        int, (int,int)  (5,5)
    * algorithm   mazelib algo    Prims
    * seed        int             None
    '''

    self.verbose = verbose

    # ─── Size & dimension

    if isinstance(size, (int, float)):
      self.dimension = 2
      self.X = size
      self.Y = size      
    else:
      self.dimension = len(size)
      self.X = int(size[0])
      self.Y = int(size[1])
      if self.dimension>2:
        self.Z = int(size[2])

    # Number of cells
    match self.dimension:
      case 2: self.size = self.X*self.Y
      case 3: self.size = self.X*self.Y*self.Z

    # Periodicity
    self.periodic = False
    ''' NB: periodicity is yet to implement '''

    # ─── Random number generator

    self.seed = seed
    self.rng = np.random.default_rng(self.seed)

    # ─── Maze generation ───────────────────────

    self.algorithm = self.algorithms()[algorithm] if isinstance(algorithm, str) else algorithm

    # ─── Generate maze

    if self.verbose:
      print('Generating maze ...', end='')
      tref = time.perf_counter()

    # Default options
    if options is None:
      match self.algorithm.__name__:
        case 'GrowingTree': options = {'backtrack_chance': 0.5}
        case _: options = {}

    # Generate maze
    m = Maze(self.seed)
    m.generator = self.algorithm(self.X, self.Y, **options)
    m.generate()

    if self.verbose:
      print(f' {time.perf_counter()-tref:.02f} s')      

    # ─── Graph

    if self.verbose:
      print('converting to graph ...', end='')
      tref = time.perf_counter()

    self.graph = graph(algorithm=algorithm)
    self.graph.add_nodes_from(range(self.size))

    for k in range(self.size):

      i = k // self.X
      j = k % self.X
    
      # linear transformation to the mazelib grid
      u = 2*self.Y - 2*i - 1
      v = 2*j + 1

      # Horizontal edges
      if m.grid[u, v+1] == 0:
        self.graph.add_edge(k, k+1)        
        self.graph.add_edge(k+1, k)
        
      # Vertical edges
      if m.grid[u-1, v] == 0:
        self.graph.add_edge(k, k + self.X)        
        self.graph.add_edge(k + self.X, k)

    if self.verbose:
      print(f' {time.perf_counter()-tref:.02f} s')

  # ════════════════════════════════════════════════════════════════════════
  #                                 DISPLAY
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):
    '''
    Custom print method
    '''
    
    s = '----------------------\n'
    s += f'Maze of size ({self.X} x {self.Y})'
    s += f'- seed {self.seed}\n' if self.seed is not None else '\n'

    if self.graph.solution is not None:
      s += 'Solutions:\n'
      for solution in self.graph.solution:
        s += f' - size={len(solution)}, {solution}' 
    else:
      s += 'No solution.'

    return s

  # ────────────────────────────────────────────────────────────────────────
  def show(self, style='dark', **kwargs):
    '''
    Display the maze in an animation.
    
    → Produces just a static view, no dynamics involved.

    Arguments:
    * style ['dark', 'light']   The window style
    * **kwargs that are directly passed to the maze initialization method.
    '''

    # Create window
    W = anim.window('Maze view', style=style)
    W.autoplay = False

    # Create static animation
    A = Animation.maze.base(W, self, **kwargs)

    # Display
    W.add(A)
    W.show()

  # ────────────────────────────────────────────────────────────────────────
  def walls(self):
    '''
    Define the maze walls based on the underlying network.
    '''

    walls = []

    # --- Outer walls

    for i in range(self.X):

      # Bottom
      walls.append([[i, 0,],[i+1, 0]])

      # Top
      walls.append([[i, self.Y],[i+1, self.Y]])

    for i in range(self.Y):

      # Left
      if i!=self.solution_wall['left']:
        walls.append([[0, i],[0, i+1]])

      # Right
      if i!=self.solution_wall['right']:
        walls.append([[self.X, i],[self.X, i+1]])

    # --- Inner walls

    for i in range(self.size):

      # Vertical walls (horizontal edges)
      if i+1 < self.size and (i+1)%self.X>0 and not self.graph.has_edge(i, i+1):
        x = int(i % self.X + 1)
        y = int(i // self.X)
        walls.append([[x,y], [x,y+1]])
        
      # Horizonal walls (vertical edges)
      if i+self.X < self.size and not self.graph.has_edge(i, i+self.X):

        x = int(i % self.X)
        y = int(i // self.X + 1)
        walls.append([[x,y], [x+1,y]])

    return walls

  # ════════════════════════════════════════════════════════════════════════
  #                              SOLUTIONS   
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def create_LR_loop(self):
    '''
    Create a loop from the left to the right side
    '''

    # Random number generator
    # rng = np.random.Generator(np.random.PCG64())

    if self.verbose:
      print('Creating LR loop ...', end='')
      tref = time.perf_counter()

    # ─── Nodes to join

    # Store for display
    self.solution_wall = {'left': self.rng.choice(self.Y), 
                          'right': self.rng.choice(self.Y)}

    # Left side
    iL = self.solution_wall['left']*self.X

    # Right side
    iR = (self.solution_wall['right']+1)*self.X - 1
    
    # ─── Solution
    
    # Add the edge
    self.graph.add_edge(iL, iR)

    # Solution
    solution = [e[0] for e in nx.find_cycle(self.graph, iL)]
    
    if self.graph.solution is None: self.graph.solution = []
    self.graph.solution.append(self.format_loop_solution(solution))

    if self.verbose:
      print(f' {time.perf_counter()-tref:.02f} s')

  # ────────────────────────────────────────────────────────────────────────
  def create_loop(self, size=None, closeto=None, largest=False):
    '''
    Create a loop
    '''
    
    print('CP 4')


    # --- Find all possible loops ------------------------------------------

    loops = []

    for i in range(self.size):

      for j in ['horizontal', 'vertical']:

        # Loop through all possible (u,v) pairs
        u = i
        match j:
          case 'horizontal':
            if i+1 < self.size and (i+1)%self.X>0: v = i+1
            else: continue
              
          case 'vertical':
            if i+self.X < self.size: v = i+self.X
            else: continue

        # Abort if there is already an edge
        if self.graph.has_edge(u,v): continue

        # Temporarily add the edge (remove wall)
        self.graph.add_edge(u,v)
   
        # Find the loop
        loop = {'edge': [u, v],
                'solution': [e[0] for e in nx.find_cycle(self.graph, u)]}
        loop['size'] = len(loop['solution'])
        loops.append(loop)
      
        # Remove the extra edge
        self.graph.remove_edge(u,v)

    # --- Choose one loop --------------------------------------------------

    sizes = [l['size'] for l in loops]

    if largest:

      # Largest loop index
      k = np.argmax(sizes)

    elif size is not None:

      try:
        k = sizes.index(size)

      except ValueError:
        warnings.warn(f'Could not find the correct loop size ({size}), aborting loop creation.')
        return

    elif closeto is not None:
      
      k = np.argmin(np.abs(np.array(sizes) - closeto))

    else:
      raise ValueError("Either 'largest', 'size' or 'closeto' must be set to create a loop.")

    # --- Add the loop -----------------------------------------------------
    
    # Open the wall
    self.graph.add_edge(loops[k]['edge'][0], loops[k]['edge'][1])

    # Append solution
    if self.graph.solution is None: self.graph.solution = []
    self.graph.solution.append(self.format_loop_solution(loops[k]['solution']))

    print('CP 5')

  # ────────────────────────────────────────────────────────────────────────
  def format_loop_solution(self, solution):
    '''
    format a solution
    '''

    s = np.roll(solution, -np.argmin(solution))
    if s[1]>s[0]+1: s = np.roll(np.flip(s),1)

    return s

  # ────────────────────────────────────────────────────────────────────────
  def create_path(self, source=0, exit=None):
    '''
    Create a path for the injection protocol
    '''
    
    if exit is None: 
      exit = self.graph.number_of_positions-1

    # Add sink
    self.graph.add_sink()
    self.graph.add_edge(exit, -1)

    # Append solution
    if self.graph.solution is None: self.graph.solution = []
    self.graph.solution.append(nx.shortest_path(self.graph, source=source, target=exit))

  # ────────────────────────────────────────────────────────────────────────
  def properties(self):

    P = {}

    # Solution length
    solution = self.graph.solution[0]
    P['lambda'] = len(solution)

    # Degree historgram
    degrees = np.array([len(v) for k,v in self.graph.adj.items()])    
    P['n1'] = np.count_nonzero(degrees==1)
    P['n2'] = np.count_nonzero(degrees==2)
    P['n3'] = np.count_nonzero(degrees==3)
    P['n4'] = np.count_nonzero(degrees==4)

    # Number of intersections on the solution
    P['psi'] = np.count_nonzero(degrees[solution]>=3)
     
    return P

  # ════════════════════════════════════════════════════════════════════════
  #                                   I/O   
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def save(self, fname, mode='a'):
    '''
    Save the maze

    Args:
        fname (str): Path of the file to save to
        mode (str, optional): Writing mode. Defaults to 'a'.
    '''

    pass

    # with h5py.File(fname, mode) as hf:

    #   # Maze group
    #   if 'Maze' not in hf:
    #     hf.create_group('Maze')

    #   # Maze attributes
    #   hf['Maze'].attrs['dimension'] = self.dimension
    #   hf['Maze'].attrs['X'] = self.X
    #   hf['Maze'].attrs['Y'] = self.Y
    #   if self.dimension>2:
    #     hf['Maze'].attrs['Z'] = self.Z
    #   hf['Maze'].attrs['size'] = self.size

    #   hf['Maze'].attrs['seed'] = self.seed
    #   hf['Maze'].attrs['algorithm'] = self.algorithm.__qualname__

    #   # ─── Graph

    #   # Preparation
    #   edges = np.zeros((self.graph.number_of_edges(),5), dtype=int)
    #   corr = {d:i for i,d in enumerate(direction.iter())}

    #   for i, (u,v,attr) in enumerate(self.graph.edges(data=True)):
    #     edges[i,0] = u
    #     edges[i,1] = v
    #     edges[i,2] = corr[attr['dir_out']]
    #     edges[i,3] = corr[attr['dir_in']]
    #     edges[i,4] = attr['sink']
      
    #   hf['Maze'].attrs['edges'] = edges

    #   # ─── Solutions

    #   hf['Maze'].attrs['number_of_solutions'] = len(self.solution)

    #   if len(self.solution)==1:
    #     hf['Maze'].attrs['solution'] = self.solution[0]

  # ────────────────────────────────────────────────────────────────────────
  def load_maze(fname):
    '''
    Loads a maze

    Args:
        fname (str): Maze to load
    '''

    pass

    # with h5py.File(fname, 'r') as hf:

    #   # Generic maze
    #   M = maze(size = (hf['Maze'].attrs['X'], hf['Maze'].attrs['Y']),
    #           seed = hf['Maze'].attrs['seed'], 
    #           generate = False)
              
    #   # --- Graph

    #   # Preparation
    #   E = hf['Maze'].attrs['edges']
    #   edges = []
    #   corr = direction.iter()

    #   for i in range(E.shape[0]):
    #     edges.append((E[i,0], E[i,1], {'dir_out':corr[E[i,2]], 'dir_out':corr[E[i,3]], 'sink':E[i,4]==1}))

    #   M.graph = nx.DiGraph()
    #   M.graph.add_nodes_from(range(M.size))
    #   M.graph.add_edges_from(edges)

    #   # --- Solutions

    #   if hf['Maze'].attrs['number_of_solutions']:
    #     M.solution.append(hf['Maze'].attrs['solution'])
      
    #   return M
  
    # return None

  # ────────────────────────────────────────────────────────────────────────
  @staticmethod
  def zeta_random(algorithm, a):
    '''
    Zeta for random agents 
    '''

    match algorithm:

      case 'BacktrackingGenerator':
        L = 0.6235122738275044*a**1.7153603050738568

      case 'AldousBroder':
        L = 1.2380808328180626*a**1.42223295699136

      case 'HuntAndKill':
        L = 1.6464178403006435*a**1.2836320254326805

      case 'GrowingTree':
        L = 1.5822590439975206*a**1.14538308932715

      case 'Division':
        L = 1.080765192143326*a**1.3300342966413374

      case 'Sidewinder':
        L = 1.6284670946518438*a**1.1077510587877915

      case 'BinaryTree':
        L = 1.65052302341451*a**1.044670627663041

      case 'Wilsons':
        L = 1.2271953763549792*a**1.253804357120484

      case 'Kruskal':
        L = 1.2859757805275038*a**1.217698365303512
        
      case 'Prims':
        L = 1.6122598899515375*a**1.0435050146196303

    return L/a**2
  
# ══════════════════════════════════════════════════════════════════════════
#
#                              CORRIDORS   
#
# ══════════════════════════════════════════════════════════════════════════

class corridor:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, size=10, periodic=False):
    '''
    Constructor
    '''

    # ─── Size & dimension

    self.dimension = 1
    self.X = size
    self.Y = 1
    self.size = self.X

    # Periodicity
    self.periodic = periodic

    # ─── Graph

    if self.periodic:
      edges = [(i, (i+1)%size) for i in range(size)]
    else:
      edges = [(i, (i+1)) for i in range(size-1)]

    self.graph = graph(edges)

    # self.graph.add_nodes_from(range(self.size))

    # ─── Misc (for compatibility)

    self.graph.algorithm = ''
    self.walls = lambda : []
    self.graph.solution = [np.arange(size)]

