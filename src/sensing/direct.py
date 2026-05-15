import numpy as np

def direct_measurement(x, cfg):
    noise = cfg["noise_std"] * np.random.randn(len(x))
    return x[:,0] + noise