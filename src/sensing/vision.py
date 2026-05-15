import numpy as np

class VisionSensor:
    def __init__(self, cfg, case_cfg):
        self.fx = cfg["fx"]
        self.fy = cfg["fy"]
        self.z = cfg["z"]

        self.dropout_prob = case_cfg["dropout_prob"]
        self.base_noise = case_cfg["base_noise"]
        self.distance_noise_scale = case_cfg["distance_noise_scale"]

        self.bias = np.zeros(2)

    def project(self, state):
        """
        Project 2D position into image plane.
        state: [px, py]
        """
        px, py = state[0], state[1]

        u = self.fx * px / self.z
        v = self.fy * py / self.z

        return np.array([u, v])

    def compute_noise_std(self, state):
        """
        State-dependent noise: farther = noisier
        """
        dist = np.linalg.norm(state[:2])
        return self.base_noise + self.distance_noise_scale * dist

    def step(self, state):
        """
        Generate one measurement with:
        - projection
        - noise
        - dropout
        - bias drift
        """

        if np.random.rand() < self.dropout_prob:
            return None

        meas = self.project(state)

        noise_std = self.compute_noise_std(state)
        noise = noise_std * np.random.randn(2)

        self.bias += 0.0005 * np.random.randn(2)

        return meas + noise + self.bias


# -------------------------
# Main API (used by run.py)
# -------------------------

def vision_measurement(x, cfg, mode):
    """
    x: (T, state_dim)
    returns:
        y: (T, 2) image-plane measurements with dropout handling
    """

    sensor = VisionSensor(cfg, mode)

    T = len(x)
    y = np.zeros((T, 2))

    last_valid = np.zeros(2)

    for t in range(T):
        meas = sensor.step(x[t])

        if meas is None:
            y[t] = last_valid
        else:
            y[t] = meas
            last_valid = meas

    return y