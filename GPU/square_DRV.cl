__kernel void square_DRV(
  __global const uint *multi,
  __global const uint *n_nodes,
  __global const unsigned char *dmax,  
  __global const uint *edge,
  __global const uint *k_ij,
  __global const uint *sol,
  __global const uint *n_ij,
  __global uint *dns,
  __global uint *flw,
  __global uint *nsol
  ) {
  // ───────────────────────────────────────────────────────────────────────
  // Square density-related variables
  // ───────────────────────────────────────────────────────────────────────

  // Square id
  int i = get_global_id(0);

  // ─── Loop over universes ────────────────────

  for (int u=0; u<multi[0]; u++) {

    // Universe index shift
    uint uu = u * n_nodes[0];
    uint uuu = u * n_nodes[0] * dmax[0];

    // ─── Local densities and flows

    dns[uu + i] = 0;

    for (uint k=0; k<dmax[0]; k++) {

      // Linearized index
      uint ij = i*dmax[0] + k;

      // Neighboring node
      uint j = edge[ij];

      // Skip non-relevant values
      if (j==-1) { break; }

      // Aggregate local density
      dns[uu + i] += n_ij[uuu + ij];

      // Assess local flow
      if (edge[j*dmax[0] + 1]==-1) {

        // Dead end
        flw[uuu + ij] = - n_ij[uuu + ij];

      } else {

        // Other squares
        flw[uuu + ij] = n_ij[uuu + j*dmax[0] + k_ij[ij]] - n_ij[uuu + ij];

      }

    }

    // ─── Solution

    for (int k=1; k<=sol[0]; k++) {

      // Skip largest solution squares
      if (sol[k]>i) { break; }

      // Square is part of the solution
      if (sol[k]==i) {
        atom_add(&nsol[u], dns[uu + i]);
        break;
      }
    }
  }
}