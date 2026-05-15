import numpy as np

def simulate_system(cfg):

    T = cfg["T"]
    x = np.zeros((T,2))
    x[0] = [1.5, -1.0]

    for t in range(T-1):
        if t < cfg["transition_time"]:
            r = cfg["r_stable"]
        else:
            r = cfg["r_unstable"]

        theta = cfg["theta"]

        A = r * np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])

        noise = cfg["noise_std"] * np.random.randn(2)
        x[t+1] = A @ x[t] + noise

    return x