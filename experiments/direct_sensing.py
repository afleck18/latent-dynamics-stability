import argparse
import yaml
import numpy as np

from src.simulation.dynamics import simulate_system
from src.sensing.direct import direct_measurement
from src.estimation.reconstruction import reconstruct_state
from src.estimation.system_id import estimate_dynamics
from src.metrics.stability import compute_stability, compute_variance
from src.utils.plotting import plot_system, plot_detection

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_experiment(cfg):
    x = simulate_system(cfg["system"])
    y = direct_measurement(x, cfg["sensing"])
    x_est = reconstruct_state(y)
    A_list = estimate_dynamics(x_est, cfg["estimation"], cfg["system"])
    alpha = compute_stability(A_list, cfg["metrics"])
    variance = compute_variance(y, cfg)

    return x, y, alpha, variance

def main():
    # -------------------------
    # Base system config
    # -------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/base.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)

    if "seed" in cfg:
        np.random.seed(cfg["seed"])

    x, y, alpha, variance = run_experiment(cfg)

    plot_system(x)
    plot_detection(alpha,variance,cfg)

    
if __name__ == "__main__":
    main()