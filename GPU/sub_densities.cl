__kernel void sub_densities(
  __global const uint *n_agents,
  __global const uint *n_nodes,
  __global const unsigned char *dmax,
  __global const uint *edge,
  __global const uint *pos,
  __global const uint *org,
  __global uint *n_ij) {

  // ─── Indices ────────────────────────────────

  // Agent id
  uint id = get_global_id(0);

  // Universe index shift
  uint uuu = ((uint) id / n_agents[0]) * n_nodes[0] * dmax[0];

  // ─── Get density ────────────────────────────

  // Row index (position)
  uint ii = pos[id]*dmax[0];

  // Column index (origin)
  uint jj = 0;
  for (uint k=0; k<dmax[0]; k++) {
    if (edge[ii + k] == org[id]) {
      jj = k;
      break; 
    }
  }

  // Atomic increment to build the density map
  atom_inc(&n_ij[uuu + ii + jj]);

}