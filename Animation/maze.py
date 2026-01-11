import numpy as np

import anim

# ══════════════════════════════════════════════════════════════════════════
#                               BASE VIEW
# ══════════════════════════════════════════════════════════════════════════

class base(anim.plane.canva):
  '''
  Base class for maze visualization.

  → Uses the Animation toolbox to display static representations of a maze.
  → Subclass this class to create animations.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window:anim.window, maze, universe=0,
               disp_solution = False, 
               disp_graph = False, 
               disp_id = False, 
               wall_thickness = None, 
               wall_color = 'gray',
               portal_color = 'red',
               solution_thickness = None,
               solution_color = 'magenta',
               edge_thickness = None,
               edge_color = 'cyan',
               id_color = 'gray', **kwargs):
    '''
    Arguments
    * window    Window
    * maze      Maze
    '''

    # Engine
    self.engine = None
    self.universe = universe

    # Define maze
    self.maze = maze

    super().__init__(window, 
                     boundaries=[[0, self.maze.X], [0, self.maze.Y]],
                     display_boundaries=False)
    
    # Information display
    self.window.information.show_algorithm = True
    self.window.information.show_agents = True
    self.window.information.show_success = True
    self.window.information.show_locking = True

    # Colormap
    self.colormap = anim.colormap(name='inferno')

    # Initial informations
    self.window.information.html = self.html()
    
    # ─── Thicknesses

    if wall_thickness is None:
      wall_thickness = self.maze.X/500
    
    if solution_thickness is None:
      solution_thickness = self.maze.X/500

    if edge_thickness is None:
      edge_thickness = self.maze.X/500

    # ─── Walls ─────────────────────────────────

    # Wall items
    for i, pts in enumerate(self.maze.walls()):
      
      self.item[f'wall_{i}'] = anim.plane.path(
        points = pts,
        thickness = wall_thickness,
        stroke = wall_color,
        zvalue = 100)

    # ─── Portals ───────────────────────────────

    """     match self.maze.type:

      case 'entries':

        poly_arrow = [[0,0], 
                      [-0.1,0.1], 
                      [-0.1, 0.04], 
                      [-0.25,0.04], 
                      [-0.25,-0.04], 
                      [-0.1,-0.04], 
                      [-0.1,-0.1]]

        # Input
        self.add(polygon, 'in_arrow',
          position = [-0.1, self.maze.input_door[0][1]+0.5],
          points = poly_arrow,
          colors = [io_color, None])
        
        # Output
        match self.maze.output_side:

          case 'right':
            self.add(polygon, 'out_arrow',
              position = [self.maze.width+0.1, self.maze.output_door[0][1]+0.5],
              points = poly_arrow,
              orientation = np.pi,
              colors = [io_color, None])

          case 'top':
            self.add(polygon, 'out_arrow',
              position = [self.maze.output_door[0][0]+0.5, self.maze.height+0.1],
              points = poly_arrow,
              orientation = -np.pi/2,
              colors = [io_color, None]) """

    # ─── Graph ─────────────────────────────────

    # if disp_graph:

    #   # Links items
    #   for id, edge in enumerate(self.maze.graph.edges):

    #     self.add(anim.plane.line, f'edge_{id}',
    #       points = [[edge[0]%self.maze.X+0.5, edge[0]//self.maze.X+0.5],
    #                 [edge[1]%self.maze.X+0.5, edge[1]//self.maze.X+0.5]],
    #       thickness = edge_thickness,
    #       color = edge_color,
    #       zvalue = 101)
          
    # ─── Solutions ─────────────────────────────

    if disp_solution:

      for k, solution in enumerate(self.maze.graph.solution):

        X = solution%self.maze.X+0.5
        Y = solution//self.maze.X+0.5

        # Find ruptures
        tmp = np.abs(np.diff(solution % self.maze.X))>1
        if np.any(tmp):
          ir = np.argwhere(np.abs(np.diff(solution % self.maze.X))>1)[0][0]
          X_ = np.concatenate((X[ir+1:], X[:ir+1]))
          Y_ = np.concatenate((Y[ir+1:], Y[:ir+1]))
        else:
          X_ = X
          Y_ = Y

        P = [[0, Y_[0]]] if X_[0]==0.5 else [[X_[0]+0.5, Y_[0]]]
        
        for i in range(X_.size):
          P.append([X_[i], Y_[i]])
        P.append([0, Y_[-1]] if X_[-1]==0.5 else [X_[-1]+0.5, Y_[-1]])

        self.item[f'solution_{k}'] = anim.plane.path(
          points = P,
          thickness = solution_thickness,
          linestyle = '--',
          stroke = solution_color,
          zvalue = 10
        )
        
    # ─── Cell indices ──────────────────────────

    if disp_id:

      for id in range(self.maze.graph.number_of_positions):

        x = id % self.maze.X
        y = id // self.maze.X

        self.item[f'id_{id}'] = anim.plane.text(
          position = [x+0.5, y+0.5],
          center = True,
          string = f'{id}',
          fontsize = 0.5,
          color = id_color,
          zvalue = 103
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
      s += f'<p>Number of agents &nbsp;<b>'
      s += f'{self.engine.agents.N}'
      s += '</b></p>'

    if self.window.information.show_success:
      s += '<p>solving ratio &nbsp; &nbsp; &nbsp; &nbsp; <b>&zeta; = '
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
    TO OVERLOAD
    '''
    pass

# ══════════════════════════════════════════════════════════════════════════
#                               DENSITY
# ══════════════════════════════════════════════════════════════════════════

class density(base):
  '''
  Dynamic density maps
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine, maze, **kwargs):

    # Animation canva constructor
    super().__init__(engine.window, maze, **kwargs)

    # Engine
    self.engine = engine
    
    # Information
    self.window.information.html = self.html()

    # Options
    self.show_densities = kwargs['show_densities'] if 'show_densities' in kwargs else False
    self.colorbar = kwargs['colorbar'] if 'colorbar' in kwargs else True
    self.log_densities = kwargs['log_densities'] if 'log_densities' in kwargs else False
    
  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Display initialization 

    Create the square items to represent the presence
    '''

    # ─── Colorbar
      
    # Set boundaries size
    self.window.information.canva.boundaries = [[0,1],[0,3]]

    if self.colorbar:
      self.window.information.canva.item.cbar = anim.plane.colorbar(
        position = [0.8, 1],
        dimension = [0.2, 2],
        colormap = self.colormap,
        ticks_number = 2,
        ticks_fontsize = 0.1,
        ticks_color = '#AAA'
      )

    # ─── Squares ────────────────────────────────

    for k in range(self.maze.size):

      # Cell position
      x = k % self.maze.X
      y = k // self.maze.X

      # Color
      if self.log_densities:
        C = self.colormap.qcolor(np.log10(self.engine.density(k, universe=self.universe)))
      else:
        C = self.colormap.qcolor(self.engine.density(k, universe=self.universe))

      # Square
      self.item[f'cell_{k}'] = anim.plane.rectangle(
        position = [x+0.5, y+0.5],
        dimension = [1,1], #[0.5, 0.5], 
        color = C,
        stroke = None,
        zvalue = 0)
      
    # ─── Densities ─────────────────────────────

    if self.show_densities:

      for id in range(self.maze.graph.number_of_positions):

        x = id % self.maze.X
        y = id // self.maze.X

        self.item[f'density_{id}'] = anim.plane.text(
          position = [x+0.5, y+0.5],
          center = True,
          string = '-',
          fontsize = 0.5,
          color = 'grey',
          zvalue = 103
        )

  # ────────────────────────────────────────────────────────────────────────
  def update_display(self, **kwargs):
    '''
    Update display
    '''

    # Update information
    self.window.information.html = self.html()

    # ─── Update square densities

    for k in range(self.maze.size):

      d = int(self.engine.density(k, universe=self.universe))

      if self.show_densities:
        self.item[f'density_{k}'].string = str(d)

      # Color
      if self.log_densities:
        C = self.colormap.qcolor(np.log10(d))
      else:
        C = self.colormap.qcolor(d)


      # Square
      self.item[f'cell_{k}'].color = C

# ══════════════════════════════════════════════════════════════════════════
#                               FLOW VIEW
# ══════════════════════════════════════════════════════════════════════════

class flows(base):
  '''
  Visualization of the orientations
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, engine, maze, **kwargs):

    super().__init__(engine.window, maze, **kwargs)

    self.engine = engine

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Display initialization 

    Create the square items to represent the presence
    '''

    # ─── Information ──────────────────────────
    
    # self.initialize_info(agents = self.engine.agent)
    # self.initialize_info(occupation = self.engine.occupation)

    # if self.engine.graph.solution is not None:
    #   self.initialize_info(_lambda = self.engine.graph.solution)
    #   self.initialize_info(success = self.engine.success)    

    # ─── Colorbar ──────────────────────────────
      
    # self.window.information.add(anim.plane.colorbar, 'colorbar',
    #   stack = False,
    #   colormap = self.colormap,
    #   height = 0.25,
    #   width = 0.025)

   # ─── Squares ────────────────────────────────

    for k in range(self.maze.size):

      # Cell position
      x = k % self.maze.X
      y = k // self.maze.X

      # Color
      C = self.colormap.qcolor(self.engine.density(k))

      # Square
      self.item[f'cell_{k}'] = anim.plane.rectangle(
        position = [x+0.5, y+0.5],
        dimension = [0.5, 0.5], 
        color = C,
        stroke = None,
        zvalue = 0)
      
    # ─── Flows ─────────────────────────────────

    self.edges = []

    for (u,v), flow in self.engine.flow.items():

      # Ignore sink
      if flow is None: continue      

      # Color
      C = self.colormap.qcolor(abs(self.engine.flow[(u,v)]))

      # Horizontal arrows
      if v==u+1:

        # Store edge
        self.edges.append((u,v))

        # Position
        x = (u % self.maze.X) + 1
        y = (u // self.maze.X) + 0.5

        # Positive arrow
        self.item[f'arrow_positive_{u}_{v}'] = anim.plane.polygon(
          points = [[x-0.15, y-0.25], [x+0.15, y], [x-0.15, y+0.25]])

        # Negative arrow
        self.item[f'arrow_negative_{u}_{v}'] = anim.plane.polygon(
          points = [[x+0.15, y-0.25], [x-0.15, y], [x+0.15, y+0.25]])
        
      # Vertical arrows
      if v==u+self.maze.X:

        # Store edge
        self.edges.append((u,v))

        # Position
        x = (u % self.maze.X) + 0.5
        y = (u // self.maze.X) + 1

        # Positive arrow
        self.item[f'arrow_positive_{u}_{v}'] = anim.plane.polygon(
          points = [[x-0.25, y-0.15], [x, y+0.15], [x+0.25, y-0.15]])

        # Negative arrow
        self.item[f'arrow_negative_{u}_{v}'] = anim.plane.polygon(
          points = [[x-0.25, y+0.15], [x, y-0.15], [x+0.25, y+0.15]])
        
      # Colors and z-indices
      if self.engine.flow[(u,v)]>0:
        self.item[f'arrow_positive_{u}_{v}'].color = C
        self.item[f'arrow_positive_{u}_{v}'].zvalue = 1
        self.item[f'arrow_negative_{u}_{v}'].color = 'k'
        self.item[f'arrow_negative_{u}_{v}'].zvalue = 0
      else:
        self.item[f'arrow_positive_{u}_{v}'].color = 'k'
        self.item[f'arrow_positive_{u}_{v}'].zvalue = 0
        self.item[f'arrow_negative_{u}_{v}'].color = C
        self.item[f'arrow_negative_{u}_{v}'].zvalue = 1

  # ────────────────────────────────────────────────────────────────────────
  def update_display(self, **kwargs):
    '''
    Update display
    '''

    # ─── Update dislayed information

    # self.update_info(agents = self.engine.agent)
    # if self.engine.graph.solution is not None:
    #   self.update_info(success=self.engine.success)
    # self.update_info(occupation = self.engine.occupation)

    # ─── Update square colors

    for k in range(self.maze.size):

      # Color
      C = self.colormap.qcolor(self.engine.presence[k])

      # Square
      self.item[f'cell_{k}'].color = C

    # ─── Update flow colors

    for (u,v) in self.edges:

      C = self.colormap.qcolor(abs(self.engine.flow[(u,v)]))

      # Colors and z-indices
      if self.engine.flow[(u,v)]>0:
        self.item[f'arrow_positive_{u}_{v}'].color = C
        self.item[f'arrow_positive_{u}_{v}'].zvalue = 1
        self.item[f'arrow_negative_{u}_{v}'].color = 'k'
        self.item[f'arrow_negative_{u}_{v}'].zvalue = 0
      else:
        self.item[f'arrow_positive_{u}_{v}'].color = 'k'
        self.item[f'arrow_positive_{u}_{v}'].zvalue = 0
        self.item[f'arrow_negative_{u}_{v}'].color = C
        self.item[f'arrow_negative_{u}_{v}'].zvalue = 1