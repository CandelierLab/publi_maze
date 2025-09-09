'''
graph API

The class can handle just one solution (loop) for the moment, despite the 
corresponding property 'self.solution' is an array of solutions. This
design simply anticipates the possibility of many solutions, which is not 
implemented yet.
'''

import networkx as nx

# ─── Visualization

import anim
import Animation.graph

class graph(nx.Graph):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, incoming_graph_data=None, algorithm=None, **attr):
    '''
    Constructor

    Args:
        incoming_graph_data (_type_, optional): _description_. Defaults to None.
    '''

    # Parent's constructor
    super().__init__(incoming_graph_data, **attr)

    # Algorithm
    self.algorithm = algorithm

    # Solution
    self.solution = None

  # ────────────────────────────────────────────────────────────────────────
  def add_sink(self):
    '''
    Add a sink node
    '''

    self.add_node(-1)

  # ────────────────────────────────────────────────────────────────────────
  def show(self, style='dark', **kwargs):
    '''
    Display the graph in an animation.
    
    → Produces just a static view, no dynamics involved.

    Arguments:
    * style ['dark', 'light']   The window style
    * **kwargs that are directly passed to the maze initialization method.
    '''

    # Create window
    W = anim.window('Graph view', style=style)
    W.autoplay = False

    # Create static animation
    A = Animation.graph.base(W, self, **kwargs)

    # Display
    W.add(A)
    W.show()

  # ────────────────────────────────────────────────────────────────────────
  @property
  def has_sink(self):
    return self.has_node(-1)

  @property
  def number_of_positions(self):
    return self.number_of_nodes() - self.has_node(-1)