'''
ENGINE
'''

import os
import warnings
import numpy as np
import h5py
from alive_progress import alive_bar
import anim

from graph import *
from agents import agents
from GPU.GPU import GPU_engine
from CPU.CPU import CPU_engine
from storage import storage

class Engine:
  '''
  Dynamical simulations on graph.

  Manages:
  * Steps, driven by the internal engine clock (no visualization) or the animation clock (visualization)
  * Sets of agents
  * Random number generator

  ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
  Success

  The task is evaluated at each time step with the ratio self.success(t), 
  which is the proportion of agents on the solution squares.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, graph:graph, rng=None, storage=None, platform='GPU', multi=1):
    '''
    Constructor
    '''

    # ─── Graph

    self.graph = graph
        
    # ─── Execution platform ('GPU')

    '''
    NB: Only GPU is supported.
    '''

    self.platform = platform
    self.cpu = None
    self.gpu = None

    self.multi = multi

    # ─── Agents

    self.agents = None
    # self.injection = None

    # ─── Display

    self.window = None
    self.animation = None
    
    # ─── Iterations

    # Running state
    self.running = False

    # Number of steps
    self.steps = None

    # Maximal number of steps
    self.max_steps = int(1e8)

    # Trigger
    self.trigger = None
    self.locked = False
    self.trigger_extra_factor = 2 

    # ─── Fields

    self.presence = None
    self.flow = None

    # ─── Measurements

    # Success ratio
    self.success = None

    # ─── Internal storage

    self.store_steps = None
    self.store_success = True
    self.store_blanks = False
    self.store_densities = False
    self.store_trajectories = False

    # ─── External storage

    # Storage object
    self._storage = None
    if storage is not None: self.storage = storage

    # Saving options
    self.save_success = False
    self.save_blanks = False
    self.save_trajectories = False

    # ─── Random number generator

    self.rng = np.random.default_rng() if rng is None else rng

  # ────────────────────────────────────────────────────────────────────────
  def add_agents(self, N, eta, **kwargs):
    '''
    Add agents.

    Typically, initial positions are determined by the initial_condition
    procedure.
    '''

    self.agents = agents(self, N, eta, **kwargs)

  # ────────────────────────────────────────────────────────────────────────
  def setup_display(self, atype, style='dark', **kwargs):
    '''
    Set up the display: window + animation
    '''

    # ─── Window

    self.window = anim.window(style=style)

    self.window.information.display(True)

    # Forbid backward animation
    self.window.allow_backward = False
    self.window.allow_negative_time = False

    # ─── Animation

    self.animation = atype(self, **kwargs)
    self.window.add(self.animation)

    # ─── Colormap

    vmin = 0
    vmax = 1

    if self.graph.solution is None:
      vmax = max(1, 3*self.agents.N/self.graph.number_of_positions)
    else:
      if self.animation.log_densities:

        vmin = -1
        vmax = 1 + np.ceil(np.log10(self.agents.N/len(self.graph.solution[0])))

      else:
        vmax = max(1, np.round(self.agents.N/len(self.graph.solution[0])))

    self.animation.colormap.range = [vmin, vmax]

  # ────────────────────────────────────────────────────────────────────────
  def run(self):
    '''
    Run the simulation
    '''

    # ─── Checks ────────────────────────────────

    # ─── No animation
    if self.animation is None:
    
      # Number of steps
      if self.trigger is None and self.steps is None:
        warnings.warn('The number of steps must be defined when there is no visualization.')
      
      # Storage
      if self.storage is None:
        warnings.warn('A storage location must be defined when there is no visualization.')
        return

    # ─── Initialization ────────────────────────

    # Reset success
    if self.store_success:
      self.l_success = [[] for i in range(self.multi)]

    # Reset blanks
    if self.store_blanks:
      self.l_blanks = [[] for i in range(self.multi)]

    match self.platform.upper():

      case 'GPU':

        # Create GPU object
        self.gpu = GPU_engine(self)

        # Compute initial densities
        self.gpu.compute_densities()

      case 'CPU':

        # Create CPU object
        self.cpu = CPU_engine(self)

        # Compute initial densities
        self.cpu.compute_densities()


      case _:
        raise NotImplementedError('The only supported platforms are CPU and GPU.')
  
    # ─── Storage ───────────────────────────────

    if self.storage is not None:
      '''
      Setup storage
      '''

      # ─── Storage already exist

      if self.storage.exists():
        os.remove(self.storage.filepath) 

      if self.store_densities:
        self.gpu.import_density = True

    # ─── Main loop ────────────────────────────────────────────────────────

    # Start run
    self.running = True

    if self.animation is None:

      if self.trigger is None:

        # ─── Fixed-size run ────────────────────

        with alive_bar(self.steps) as bar:
          bar.title = 'running'
          bar()

          for step in range(self.steps-1):
            self.update(step)

            # Stop simulation
            if not self.running: break

            bar()
            
      else:

        # ─── Triggered run ─────────────────────

        with alive_bar(unknown='waves') as bar:
          bar.title = f'U 0/{self.multi}'
          bar()

          for step in range(self.max_steps-1):
            self.update(step)

            # Stop simulation
            if not self.running: break

            # Update bar display
            if self.locked:
              bar.title = f'L @ {int(self.steps/self.trigger_extra_factor)}'
            else:
              bar.title = f'U {np.count_nonzero(self.success>=self.trigger)}/{self.multi}'
            bar()

      # === FOR DEBUGGING =======================
      # for step in range(self.steps-1):
      #   print(step)
      #   self.update(step)

      # self.end(self.steps)
      # =========================================

      # ─── End run

      self.end()

    else:

      # Initialize animation
      if hasattr(self.animation.__class__, 'initialize') and callable(getattr(self.animation.__class__, 'initialize')):
        self.animation.initialize()

      self.window.information.html = self.animation.html()
      self.window.show()

      # Ending
      if self.steps is None:
        self.end()

  # ────────────────────────────────────────────────────────────────────────
  def update(self, iteration):
    '''
    One step of the simulation
    '''

    # Fix behavior at low number of steps
    if self.steps is not None and iteration >= self.steps: 
      self.running = False
      if self.animation is not None:
        self.end()
      return
    
    match self.platform.upper():
      case 'GPU':        
        self.gpu.step()
      case 'CPU':        
        self.cpu.step()

    # ─── Locking ───────────────────────────────

    if self.trigger is not None:

      self.locked = np.all(self.success>=self.trigger)

      if self.locked:

        # Define step
        if self.steps is None:
          self.steps = min(iteration*self.trigger_extra_factor, self.max_steps)

      else:

        if self.steps is not None:
          self.steps = None

    # ─── Storage ───────────────────────────────

    if self.storage is not None:

      # ────────────────────────
      # Densities
      # ────────────────────────
      if self.store_densities:

        if self.store_steps is None or iteration in self.store_steps:
          self.storage[str(iteration)] = self.density()

    # ─── End of simulation ─────────────────────

    if (self.steps is not None and iteration>=self.steps) or \
       (self.max_steps is not None and iteration>=self.max_steps):
      self.running = False
      
  # ────────────────────────────────────────────────────────────────────────  
  def end(self):
    '''
    Operations to do when the simulation is over
    '''
    
    # ─── Storage ───────────────────────────────

    if self.storage is not None:

      with h5py.File(self.storage.filepath, 'a') as hf:

        # ─── Success

        if self.storage.save_success:

          # One last iteration
          match self.platform.upper():
            case 'GPU': self.gpu.step()
            case 'CPU': self.cpu.step()

          hf['success'] = self.l_success

        # ─── Blanks

        if self.storage.save_blanks:

          # One last iteration
          match self.platform.upper():
            case 'GPU': self.gpu.step()
            case 'CPU': self.cpu.step()

          hf['blanks'] = self.l_blanks
        
    # ─── Display ───────────────────────────────
    
    if self.animation is not None:
      self.animation.is_running = False
      self.animation.window.close()

  # ────────────────────────────────────────────────────────────────────────  
  def density(self, i=None, universe=0): 
    '''
    Current density at a given node
    '''

    if i is None:

      match self.platform.upper():
        case 'GPU': return self.gpu.h_dns[universe, :]
        case 'CPU': return self.cpu.ni[universe, :]
        case _: return 0

    else:

      match self.platform.upper():
        case 'GPU': return self.gpu.h_dns[universe, i]
        case 'CPU': return self.cpu.ni[universe, i]
        case _: return 0

  # ────────────────────────────────────────────────────────────────────────  
  def flow(self, i, j, universe=0): 
    '''
    Current flow between two nodes
    '''

    match self.platform.upper():
      case 'GPU': self.gpu.h_fls[universe,i,j]
      case 'CPU': self.cpu.flow[universe,i,j]
      case _: return 0

  # ══════════════════════════════════════════════════════════════════════════
  #                               Properties
  # ══════════════════════════════════════════════════════════════════════════

  # ─── Storage ──────────────────────────────────────────────────────────────

  @property
  def storage(self): return self._storage

  @storage.setter
  def storage(self, s):
    
    self._storage = storage(s) if isinstance(s, str) else s

    # Storage options
    self._storage.save_maze = False
    self._storage.save_trajectories = False
    self._storage.save_success = False
    self._storage.save_blanks = False

