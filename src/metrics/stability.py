import numpy as np

def compute_stability(A_list, cfg):

    alpha = []

    for A in A_list:
        rho = np.max(np.abs(np.linalg.eigvals(A)))
        alpha.append(rho - 1)

    alpha = np.array(alpha)
    k = cfg["smoothing"]
    alpha = np.convolve(alpha, np.ones(k)/k, mode='valid')

    return alpha

def compute_variance(y, cfg):
    variance = []
    for t in range(cfg["estimation"]["window_pre"], cfg["system"]["T"]):
        seg = y[t-cfg["estimation"]["window_pre"]:t]
        variance.append(np.var(seg))

    variance = np.array(variance)

    return variance