import numpy as np

def compute_stability(A):
    A_sym = 0.5 * (A + A.T)
    eigvals = np.linalg.eigvals(A_sym)
    return np.max(np.real(eigvals))