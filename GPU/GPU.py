'''
GPU Engine
'''

import os
import numpy as np
import pyopencl as cl
from pyopencl.clrandom import PhiloxGenerator
import pyopencl.array as cl_array

os.environ['PYOPENCL_CTX'] = '0'
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

class GPU_engine:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine):

    # Get the engine
    self.engine = engine

    # Kernels
    self.kernel = type('obj', (object,), {'sub_densities': None, 
                                          'square_DRV': None,
                                          'motion': None})

    # ─── Import options ────────────────────────

    self.import_density = self.engine.store_blanks    # False by default
    self.import_flow = False
    self.import_position = False
    self.import_origin = False

    # ─── Formats ───────────────────────────────

    '''
    Square ids:
      Use uint16 for mazes up to size a = 255
      Use uint32 for mazes up to size a = 65535
    '''

    # Constants
    self.multi_format = np.uint32
    self.n_agents_format = np.uint32
    self.degmx_format = np.uint8
    self.eta_format = np.float32

    # Arrays
    self.squid_depth = 32
    self.denst_depth = 32
    self.flow_depth = 32

    # Formats
    match self.squid_depth:
      case 16: self.squid_format = np.uint16
      case 32: self.squid_format = np.uint32

    match self.denst_depth:
      case 16: self.denst_format = np.uint16
      case 32: self.denst_format = np.uint32

    match self.flow_depth:
      case 16: self.flow_format = np.int16
      case 32: self.flow_format = np.int32

    # ─── Constants ─────────────────────────────

    # Number of multiverses
    self.multi = self.multi_format(self.engine.multi)

    # Maximal number of agents
    self.n_agents = self.n_agents_format(self.engine.agents.N)

    # Constants
    self.NOT_A_NODE = int(2**self.squid_depth-1)

    # Number of nodes
    self.n_nodes = self.squid_format(self.engine.graph.number_of_nodes())

    # Max degree
    dmax = np.max([d for n, d in self.engine.graph.degree()]).astype(self.degmx_format)

    # Eta
    eta = np.array(self.engine.agents.eta, dtype=self.eta_format)

    # ─── OpenCL machinery ──────────────────────

    # ─── Context

    platform = cl.get_platforms()
    my_gpu_devices = [platform[0].get_devices(device_type=cl.device_type.GPU)[0]]
    ctx = cl.Context(devices=my_gpu_devices)

    # Queue
    self.queue = cl.CommandQueue(ctx)

    # Random number generator
    self.rng =  PhiloxGenerator(context=ctx)

    # ─── Kernels ───────────────────────────────

    kernel_path = os.path.dirname(__file__) + os.path.sep

    # ─── Sub-density
    '''
    KERNEL 1: Sub-density
              position & origin to sub-density map n_ij and zeta
    '''

    prg = cl.Program(ctx, open(kernel_path + 'sub_densities.cl').read()).build()
    self.kernel.sub_densities = prg.sub_densities

    # ─── Square density-related variables
    '''
    KERNEL 2: Square density-related variables
              Local density and max flow squares
    '''

    prg = cl.Program(ctx, open(kernel_path + 'square_DRV.cl').read()).build()
    self.kernel.square_DRV = prg.square_DRV
  
    # ─── get_motion
    '''
    KERNEL 3: get_motion
          n_ij to (new) position & orientation

      Probability to move:
      - Compute local density: sum of n_ij over j
      - Apply to formula to get p_move
      - decide motion and store as binary array 'motion'

      Orientation decision:
      - Compute flows: store n_ji - n_ij for all j
      - Take the argmax of these sums
      - store as an int array 'orientation'

      Determine new position and orientation
    '''

    prg = cl.Program(ctx, open(kernel_path + 'motion.cl').read()).build()
    self.kernel.motion = prg.motion

    # ─── Data ───────────────────────────

    # ─── Host arrays

    # Position and origin
    self.engine.agents.position = self.engine.agents.position.astype(self.squid_format)
    self.engine.agents.origin = self.engine.agents.origin.astype(self.squid_format)

    # Edges array
    self.h_edg = np.full((self.n_nodes, dmax), self.NOT_A_NODE, dtype=self.squid_format)
    for i in self.engine.graph.nodes():
      for k, edge in enumerate(self.engine.graph.edges(i)):
        self.h_edg[i,k] = edge[1]

    # Mirror index array
    self.h_kij = np.full((self.n_nodes, dmax), self.NOT_A_NODE, dtype=self.squid_format)
    for i in self.engine.graph.nodes():
      for k, j in enumerate(self.h_edg[i,:]):
        if j==self.NOT_A_NODE: break
        self.h_kij[i,k] = np.where(self.h_edg[j,:]==i)[0][0]

    # Density arrays
    self.h_nij = np.zeros((self.multi, self.n_nodes, dmax), dtype=self.denst_format)
    self.h_dns = np.zeros((self.multi, self.n_nodes), dtype=self.denst_format)

    # Flows
    self.h_flw = np.zeros((self.multi, self.n_nodes, dmax), dtype=self.flow_format)

    # Solution
    solution = np.sort(self.engine.graph.solution[0]).astype(self.squid_format)
    solution = np.insert(solution, 0, solution.size)
    self.h_nsl = np.zeros(self.multi, dtype=self.denst_format)

    # ─── Device arrays

    mf = cl.mem_flags

    # Constants
    self.d_mlt = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.multi)
    self.d_nag = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.n_agents)
    self.d_nnd = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.n_nodes)
    self.d_dmx = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = dmax)
    self.d_edg = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.h_edg)
    self.d_kij = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.h_kij)
    self.d_eta = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = eta)
    self.d_sol = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = solution)

    # Arrays
    self.d_pos = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = self.engine.agents.position)
    self.d_org = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = self.engine.agents.origin)
    self.d_nij = cl.Buffer(ctx, mf.READ_WRITE, self.h_nij.nbytes)
    self.d_dns = cl.Buffer(ctx, mf.READ_WRITE, self.h_dns.nbytes)
    self.d_flw = cl.Buffer(ctx, mf.READ_WRITE, self.h_flw.nbytes)
    self.d_nsl = cl.Buffer(ctx, mf.READ_WRITE, self.h_nsl.nbytes)
    self.d_rnd = cl_array.zeros(self.queue, self.multi*self.n_agents, dtype=np.float32)

  # ────────────────────────────────────────────────────────────────────────
  def compute_densities(self):
    '''
    Compute the densities based on the positions
    '''

    # Reset subdensities to zeros
    cl.enqueue_fill_buffer(self.queue, self.d_nij, np.uint32(0), 0, self.h_nij.nbytes)

    self.kernel.sub_densities(self.queue, [self.n_agents*self.multi], None, # Required arguments
                           self.d_nag, self.d_nnd, self.d_dmx, self.d_edg,              # Constants
                           self.d_pos, self.d_org,                          # Inputs
                           self.d_nij                                       # Outputs
                           ).wait()
    
    # Get back the sub density
    # cl.enqueue_copy(self.queue, self.h_nij, self.d_nij)
    
    # Reset zeta to zero
    cl.enqueue_fill_buffer(self.queue, self.d_nsl, np.uint32(0), 0, self.h_nsl.nbytes)

    self.kernel.square_DRV(self.queue, [self.n_nodes], None,                # Required arguments
                           self.d_mlt, self.d_nnd, self.d_dmx, self.d_edg, self.d_kij, self.d_sol,  # Constants
                           self.d_nij,                                      # Inputs
                           self.d_dns, self.d_flw, self.d_nsl               # Outputs
                           ).wait()

    # Flow and density
    if self.import_density or self.engine.animation is not None:
      cl.enqueue_copy(self.queue, self.h_dns, self.d_dns)
    if self.import_flow:
      cl.enqueue_copy(self.queue, self.h_flw, self.d_flw)

    # Import success
    cl.enqueue_copy(self.queue, self.h_nsl, self.d_nsl)
    self.engine.success = self.h_nsl/self.n_agents
    if self.engine.store_success or (self.engine.storage is not None and self.engine.storage.save_success):
      for k in range(self.multi):
        self.engine.l_success[k].append(self.engine.success[k].item())

    # Import blanks
    if self.engine.store_blanks:

      blanks = np.count_nonzero(self.h_dns==0, axis=1)

      for k in range(self.multi):
        self.engine.l_blanks[k].append(blanks[k].item())    

  # ────────────────────────────────────────────────────────────────────────
  def step(self):
    '''
    One step of the simulation
    '''

    # Prepare random array
    self.rng.fill_uniform(self.d_rnd)

    self.kernel.motion(self.queue, [self.n_agents*self.multi], None,        # Required arguments
                           self.d_nag, self.d_nnd, self.d_dmx, self.d_edg, self.d_eta,  # Constants
                           self.d_dns, self.d_flw,                          # Inputs
                           self.d_pos, self.d_org,                          # Outputs
                           self.d_rnd.data,                                 # Misc (random values)
                           ).wait()

    if self.import_position:    
      cl.enqueue_copy(self.queue, self.engine.agents.position, self.d_pos)

    if self.import_origin:
      cl.enqueue_copy(self.queue, self.engine.agents.origin, self.d_org)

    # Re-compute the densities
    self.compute_densities()