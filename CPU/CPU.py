'''
CPU Engine
'''

import numpy as np

class CPU_engine:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine):

    # Get the engine
    self.engine = engine

    # ─── Constants ─────────────────────────────

    # Number of multiverses
    self.multi = self.engine.multi

    # Maximal number of agents
    self.n_agents = self.engine.agents.N

    # Constants
    self.NOT_A_NODE = -1

    # Number of nodes
    self.n_nodes = int(self.engine.graph.number_of_nodes())

    # Max degree
    self.dmax = np.max([d for n, d in self.engine.graph.degree()])

    # ─── Data ───────────────────────────

    # Edges array
    self.edges = np.full((self.n_nodes, self.dmax), self.NOT_A_NODE)
    for i in self.engine.graph.nodes():
      for k, edge in enumerate(self.engine.graph.edges(i)):
        self.edges[i,k] = edge[1]

    # Mirror index array
    self.kij = np.full((self.n_nodes, self.dmax), self.NOT_A_NODE)
    for i in self.engine.graph.nodes():
      for k, j in enumerate(self.edges[i,:]):
        if j==self.NOT_A_NODE: break
        self.kij[i,k] = np.where(self.edges[j,:]==i)[0][0]

    # Density arrays
    self.nij = np.zeros((self.multi, self.n_nodes, self.dmax))
    self.ni = np.zeros((self.multi, self.n_nodes))

    # Flows
    self.flow = np.zeros((self.multi, self.n_nodes, self.dmax))

    # Solution
    self.solution = np.sort(self.engine.graph.solution[0])
    # solution = np.insert(solution, 0, solution.size)
    self.zeta = np.zeros(self.multi)

  # ────────────────────────────────────────────────────────────────────────
  def compute_densities(self):
    '''
    Compute the densities based on the positions
    '''

    # ─── Sub-densities ─────────────────────────

    # Reset subdensities to zeros
    self.nij = np.zeros((self.multi, self.n_nodes, self.dmax))

    for u in range(self.engine.multi):
      for id in range(self.n_agents):

        # Position
        i = self.engine.agents.position[u,id]

        # Origin
        for k in range(self.dmax):
          if self.edges[i,k]==self.engine.agents.origin[u,id]:
            self.nij[u, i, k] += 1
            break

    # Update local density
    self.ni = np.sum(self.nij, axis=2)

    # ─── Square operations ─────────────────────

    # Reset zeta to zero
    self.zeta = np.zeros(self.multi)

    for u in range(self.engine.multi):

      # ─── Flows

      for i in range(self.n_nodes):

        for k in range(self.dmax):

          # Skip if all neighbors have been explored
          if self.edges[i,k]==self.NOT_A_NODE: break

          # Neighbor
          j = self.edges[i,k]

          # Assess local flow
          if (self.edges[j,1]==self.NOT_A_NODE):

            # Dead end
            self.flow[u, i, k] = -self.nij[u, i, k]

          else:

            # Other squares
            self.flow[u, i, k] = self.nij[u, j, self.kij[i, k]] - self.nij[u, i, k]

      # ─── Success ratio

      self.zeta[u] = np.sum(self.ni[u, self.solution])/self.n_agents

    # ─── Success ratios updates ────────────────

    self.engine.success = self.zeta
    if self.engine.store_success or (self.engine.storage is not None and self.engine.storage.save_success):
      for k in range(self.multi):
        self.engine.l_success[k].append(self.engine.success[k].item())

  # ────────────────────────────────────────────────────────────────────────
  def step(self):
    '''
    One step of the simulation
    '''

    # ─── Motion ────────────────────────────────

    for u in range(self.multi):

      # ─── Motion probability

      p_move = self.ni[u,:]/(self.ni[u,:] + self.engine.agents.eta)

      # Moving agents
      I = np.where(np.random.rand(self.n_agents) < p_move[self.engine.agents.position[u,:]])[0]

      # ─── Motion direction

      for id in I:

        # Position
        i = self.engine.agents.position[u,id]

        # Maximum flow
        flows = self.flow[u, i, np.where(self.edges[i,:]!=self.NOT_A_NODE)[0]]

        if self.engine.agents.gamma is None:

          # Pure max
          K = np.where(flows==np.max(flows))[0]
          k = np.random.choice(K)

        else:

          # Soft max
          Z = np.exp(flows*self.engine.agents.gamma/self.ni[u,i])
          k = np.random.choice(np.arange(flows.size), p=Z/np.sum(Z))

        # Update position
        self.engine.agents.position[u,id] = self.edges[i,k]

        # Update origin
        self.engine.agents.origin[u,id] = i

    # Re-compute the densities
    self.compute_densities()