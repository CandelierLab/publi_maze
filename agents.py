'''
Agents class
'''

import numpy as np

class agents:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine, N, eta, gamma=None, **kwargs):

    # ─── Definitions

    self.eta = eta
    self.gamma = gamma

    # ─── Positions & origins ───────────────────

    # Preparation: all possibilities
    E = engine.graph.edges()
    poss = np.concatenate((E, np.flip(E, axis=1)), axis=0)

    # Draw configurations
    C = engine.rng.choice(poss.shape[0], engine.multi*N)
    self.position = np.reshape(poss[C,0], shape=(engine.multi, N))
    self.origin = np.reshape(poss[C,1], shape=(engine.multi, N))

  # ─── Number of agents ───────────────────────────────────────────────────
  
  @property
  def N(self): return self.position.shape[1]


   # # Default: random positions
    # if position is None:
    #   position = self.rng.choice(self.graph.number_of_positions, n)

    # for i in range(n):
    #   self.agent.append(atype(int(position[i]), nest=self.nest, **kwargs))

  # ========================================================================
  # def initial_condition(self, n, filter= None, repartition='random'):
  #   '''
  #   Initial condition specify both wich and how graph nodes (positions) 
  #   receive agents (filter) and the repartition of the agents over these nodes.

  #   The filter is a list of weights, one for each position. In the simplest 
  #   case, the weitghs are 0 for forbidden positions and 1 for authorized 
  #   positions.

  #   There are also 3 shortcut notations:
  #   - None: all positions are authorized, with equal weights
  #   - 'solution': only the positons on the solution are authorized, with 
  #                 equal weights.
  #   - 'antisolution': only the positions not on the solution are authorized,
  #                     with equal weights.

  #   Then, the repartition is either 'random' or 'homogeneous'. In the 
  #   latter case, agents are reparted as evenly as possible among the 
  #   available positions.
  #   '''

  #   # --- Initialization ---------------------------------------------------
    
  #   # --- Weights

  #   if filter is None:
  #     ''' No filter: all positions are authorized, with equal weights '''

  #     w = np.ones(self.graph.number_of_positions)

  #   elif isinstance(filter, str):
  #     ''' Other special cases '''

  #     match filter:

  #       case 'solution':

  #         if self.graph.solution is None:
  #           raise ValueError

  #         w = np.zeros(self.graph.number_of_positions)
  #         w[self.graph.solution] = 1

  #       case 'antisolution':

  #         if self.graph.solution is None:
  #           raise ValueError
          
  #         w = np.ones(self.graph.number_of_positions)
  #         w[self.graph.solution] = 0

  #   else:
  #     ''' Default: the filter is directly a list of weights '''

  #     w = np.array(filter)

  #   # --- Repartition

  #   match repartition:

  #     case 'random':

  #       # Normalize weights
  #       w = w/np.sum(w)

  #       # Positions
  #       position = self.rng.choice(self.graph.number_of_positions, n, p=w)

  #     case 'homogeneous':

  #       # Compute numbers
  #       b = w/np.sum(w)*n
  #       nb = np.round(b).astype(int)

  #       # Remove excedent
  #       while np.sum(nb)>n:
  #         nb[np.argmax(nb)] -= 1

  #       # Complete misses
  #       if np.sum(nb)<n:
  #         I = np.argsort(nb-b)
  #         nb[I[:int(n-np.sum(nb))]] += 1

  #       # Assign positions
  #       position = np.empty(n, dtype=int)
  #       k = 0
  #       for i, m in enumerate(nb):
  #         if not m: continue
  #         position[k:k+m] = i
  #         k += m

  #   return position