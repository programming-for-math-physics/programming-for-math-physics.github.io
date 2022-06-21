import numpy as np

def grad_phi(phi, r, n0):
    """
    """
    n,d = r.shape
    assert(phi.shape == (n,)), (phi.shape, n)
    g = np.zeros(n)
    for i in range(n):
        dr = r - r[i]
        dr_norm2 = np.array([ sum(dr[j,:] * dr[j,:]) for j in range(n) ])
        dr_norm = np.sqrt(dr_norm2)
        inv_dr = 1 / dr_norm2
        inv_dr[i] = 0.0
        g[i] = (d / n0) * np.sum((phi - phi[i]) * inv_dr * weight(dr_norm) * dr,
                                 axis=0)
    return g
