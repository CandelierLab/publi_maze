__kernel void motion(
  __global const uint *n_agents,
  __global const uint *n_nodes,
  __global const unsigned char *dmax,
  __global const uint *edge,
  __global const float *eta,
  __global const uint *dns,
  __global const int *flw,
  __global uint *pos,
  __global uint *org,
  __global const float *rnd
  ) {

  // ─── Indices ────────────────────────────────

  // Agent id
  uint id = get_global_id(0);

  // Universe & index shifts
  uint u = (uint)id / n_agents[0];
  uint uu = u * n_nodes[0];
  uint uuu = u * n_nodes[0] * dmax[0];

  // ─── Motion ─────────────────────────────────

  // Motion probability
  float p_move = dns[uu + pos[id]]/(dns[uu + pos[id]] + eta[0]);

  // Stall
  if (p_move < rnd[id]) { return; }

  // ─── Set origin

  org[id] = pos[id];

  // ─── Position ──────────────────────────────────────────────────────────

  // ─── First pass: max flow and number of options

  uint ii = pos[id]*dmax[0];

  // Initialization
  int nopt = 1;
  int fmax = flw[uuu + ii];

  for (uint k=1; k<dmax[0]; k++) {

    // Loop only through edges
    if (edge[ii + k]==-1) { break; }

    int f = flw[uuu + ii + k];
    
    if (f>fmax) {
      fmax = f;
      nopt = 1;
    } else if (f==fmax) {
      nopt++;
    }

  }

  // ─── Second pass: select an option

  // Chosen option
  char opt = 0;

  if (nopt>1) {
    // NB: a new random number is generated from the previous one
    float r = rnd[id]*10;
    opt = (char) (nopt*(r-((int) r)));
  }

  // Current option
  char copt = 0;

  for (uint k=0; k<dmax[0]; k++) {
    if (flw[uuu + ii + k]==fmax) { 

      if (copt==opt) {
        
        // New position
        pos[id] = edge[ii + k];

        // Break
        break;

      } else { copt++; }
    }
  }

  // printf("id=%i, nopt=%i, opt=%i\n", id, nopt, opt);
  
}