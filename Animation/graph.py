from screeninfo import get_monitors   # information of physical screens
import networkx as nx                 # manages graphs
from PyQt6.QtGui import QColor        # packagfe for colors

import anim

import numpy as np

# ══════════════════════════════════════════════════════════════════════════
#                               BASE VIEW
# ══════════════════════════════════════════════════════════════════════════

class base(anim.plane.canva):
  '''
  Base class for graph visualization.

  → Uses the Animation toolbox to display static representations of a graph.
  → Subclass this class to create animations.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, graph,
               universe = 0, # display universe 0 unless stated otherwise
               layout = nx.kamada_kawai_layout,
               disp_id = False,
               edge_thickness = 0, 
               edge_color = 'white',
               node_radius = None,
               id_color = 'pink'):
    '''
    Arguments
    * window    Window
    * maze      Maze
    '''

    # Universe
    self.universe = universe

    # Define maze
    self.graph = graph

    # this method changes canva attribuites, which is the class (base is a subclass)
    super().__init__(window, 
                     boundaries=[[-1.1, 1.1], [-1.1, 1.1]],
                     display_boundaries=False)
    # boundaries of the graph
    # boundaries_color='red'
    # boundaries_thickness = 10

    
    # Information display
    self.window.information.show_algorithm = True
    self.window.information.show_agents = True
    self.window.information.show_success = True
    self.window.information.show_locking = True

    # Colormap
    self.colormap = anim.colormap(name='spring')
  
    
    # ─── Positions ─────────────────────────────

    # Position nodes using Kamada-Kawai path-length cost-function.
    # This determines the positions of the graph nodes
    nodes_position = layout(self.graph)
    
    # ─── Edges ─────────────────────────────────
    
    for (u,v) in self.graph.edges():

      pu = nodes_position[u].tolist()
      pv = nodes_position[v].tolist()
      
      # make a line for each edge at specified position
      self.item[f'edge_{u}_{v}'] = anim.plane.line(
        position = [pu[0], pu[1]],
        dimension = [pv[0]-pu[0], pv[1]-pu[1]], #length
        thickness = edge_thickness,
        color = edge_color,
        zvalue = 0)
      
    # ─── Nodes ─────────────────────────────────    

    # Auto radius
    if node_radius is None:
      node_radius = (self.graph.number_of_positions**-0.5)/5

    for k, pos in nodes_position.items():

      self.item[f'node_{k}'] = anim.plane.circle(
        position = pos.tolist(),
        radius = node_radius,
        stroke = edge_color,
        color = 'black',
        zvalue = 1)
              
    # ─── Cell indices ──────────────────────────

    if disp_id:

      for k, pos in nodes_position.items():

        self.item[f'id_{k}'] = anim.plane.text(
          position = pos.tolist(),
          center = True,
          string = str(k),
          fontsize = 0.03,
          color = id_color,
          zvalue = 100
        )

  # ────────────────────────────────────────────────────────────────────────
  def html(self):

    # Check engine
    if self.engine is None: return ''

    s = ''

    if self.window.style=='white':
      s += '<div style="color: black;">'
    else:
      s += '<div>'

    if self.window.information.show_algorithm:
      s += '<p><b>'
      s += self.engine.graph.algorithm
      s += '</b></p>'

    if self.window.information.show_agents:
      s += f'<p>Number of agents &nbsp; &nbsp; &nbsp; <b>'
      s += f'{self.engine.agents.N}'
      s += '</b></p>'

    if self.window.information.show_success:
      s += '<p>success ratio &nbsp; &nbsp; &nbsp; &nbsp; <b>&zeta; = '
      s += '---' if self.engine.success is None else f'{self.engine.success[self.universe]:.03f}'
      s += '</b></p></div>'

    if self.window.information.show_locking:    
      if self.engine.trigger is not None:
        s += f'<p>trigger: {self.engine.trigger} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; '

        if self.engine.locked:
          s += '<font color="#03EEAA">🔒</font>'
        else:
          s += '<font color="#EE9103">🔓</font>'
        s += '</p>'

    s += '</div>'

    return s

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):
    '''
    Update method
    '''

    # Compute step
    if self.engine is not None:
      self.engine.update(t.step)

    # Update information
    self.window.information.html = self.html()

    #  Update display
    self.update_display(t=t)

    # Confirm update
    super().update(t)

  # ────────────────────────────────────────────────────────────────────────
  def update_display(self, **kwargs):
    '''
    TO OVERLOAD ???????????????
    '''
    pass

# ══════════════════════════════════════════════════════════════════════════
#                               DENSITY
# ══════════════════════════════════════════════════════════════════════════

class density_view(base):
  '''
  Dynamic density maps; subclass of base
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine, graph, **kwargs):
    '''
    Arguments
    * window    Window
    * maze      Maze
    '''

    # Engine
    self.engine = engine

    # Animation canva constructor
    super().__init__(self.engine.window, graph, **kwargs)

    # Information
    self.window.information.html = self.html()

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Display initialization

    Create the items to represent the presence
    '''

    # ─── Colorbar
      
    # Set boundaries size
    self.window.information.canva.boundaries = [[0,1],[0,3]] # position of graph

    # potition of density colorbar
    self.window.information.canva.item.cbar = anim.plane.colorbar(
      position = [0.8, 1],
      dimension = [0.2, 2],
      colormap = self.colormap,
      ticks_number = 3,
      ticks_fontsize = 0.1,
      ticks_color = '#AAA'
    )

    # Update display ??????
    self.update_display()

 # ────────────────────────────────────────────────────────────────────────
  def update_display(self, **kwargs):
    '''
    Update display
    '''

    # Update information
    self.window.information.html = self.html()

    # ─── Update node colors

    for k in self.graph.nodes():

      # Set colorss
      C = self.colormap.qcolor(self.engine.density(k, universe=self.universe))
      self.item[f'node_{k}'].color = C


# ══════════════════════════════════════════════════════════════════════════
#                               ORIENTATION
# ══════════════════════════════════════════════════════════════════════════

class orientation_view(base):
  '''
  Dynamic orientation maps; subclass of base
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine, graph, **kwargs):
    '''
    Arguments
    * window    Window
    * maze      Maze
    '''

    # Engine
    self.engine = engine

    # Animation canva constructor
    super().__init__(self.engine.window, graph, **kwargs)

    # Information
    self.window.information.html = self.html()

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Display initialization

    Create the items to represent the presence
    '''

    # position of edges in graph view
    layout = nx.kamada_kawai_layout
    nodes_position = layout(self.graph)

    # ─── Colorbar ─────────────────────────────────

    # Set boundaries size
    self.window.information.canva.boundaries = [[0,1],[0,3]] # position of graph

    # potition of density colorbar
    self.window.information.canva.item.cbar = anim.plane.colorbar(
      position = [0.8, 1],
      dimension = [0.2, 2],
      colormap = self.colormap,
      ticks_number = 3,
      ticks_fontsize = 0.1,
      ticks_color = '#AAA'
    )

            
    # ─── Circle sectors ─────────────────────────────────

    # ===== COMPUTE FRAME OF REFERENCE (circle section)

    # compute maximum number of nodes in the graph
    self.dmax = np.max([d for n, d in self.engine.graph.degree()])

      
    # Construct edges object (stores edge indexes)
    self.h_edge = np.full((self.engine.graph.number_of_nodes(), self.dmax), np.nan)

    for i in self.engine.graph.nodes(): # original node

      for k, edge in enumerate(self.engine.graph.edges(i)): # current node

        # enumerate edges stemming from those nodes (with repetition)
        self.h_edge[i,k] = edge[1]      # h_edges is an object wich contains Nan where there are no nodes connecting to adjacent cells

        # ===== GEOMETRY
                
        # position of the center
        pu = nodes_position[edge[1]]             # current position
        pv = nodes_position[i]                   # original position

        # edge length (Euclidean space)
        len = np.linalg.norm(pv - pu)

        # angles (two cases according to abscises axis)
        if pv[1] < pu[1]: # new edge is below in absolute coordinates. -pi < phi < 0
          phi = - np.arccos( (pu[0] - pv[0]) / len )

        elif pv[1] >= pu[1]: # new edge is above in absolute coordinates. 0 < phi < pi
          phi = np.arccos( (pu[0] - pv[0]) / len )

        # absolute angles for A and B
        theta_A = [phi + np.pi / 5]
        theta_B = [phi - np.pi / 5]

        # Auto radius
        node_radius = (self.graph.number_of_positions**-0.5)/5

        # segment points
        O = [float(pu[0]), float(pu[1])]
        A = [float(pu[0] + node_radius * np.cos(theta_A)), float(pu[1] + node_radius * np.sin(theta_A))]
        B = [float(pu[0] + node_radius * np.cos(theta_B)), float(pu[1] + node_radius * np.sin(theta_B))]

        print(O, A, B)


        # ===== POLYGON (circle section)

        # Color
        C = self.colormap.qcolor(self.engine.orientation(i, k, universe=self.universe) )    

        # triangle (circle section)
        self.item[f'sector_{edge[1]}_{i}'] = anim.plane.polygon(
          points = [O, A, B],
          color = C,
          stroke = None,
          zvalue = 2)
           

    # Update display
    self.update_display()

 # ────────────────────────────────────────────────────────────────────────
  def update_display(self, **kwargs):
    '''
    Update display
    '''

    # Update information

    
    self.window.information.html = self.html()

    # ─── Update node colors

    for i in self.engine.graph.nodes(): # original node

      for k, edge in enumerate(self.engine.graph.edges(i)): # current node
       
        # Color
        C = self.colormap.qcolor(self.engine.orientation(i, k, universe=self.universe) )    
        self.item[f'sector_{edge[1]}_{i}'].color = C