import argparse
import yaml
import numpy as np

from src.simulation.dynamics import simulate_system
from src.sensing.vision import vision_measurement
from src.estimation.reconstruction import reconstruct_state
from src.estimation.system_id import estimate_dynamics
from src.metrics.stability import compute_stability
from src.utils.plotting import plot_vision_measurements, plot_vision_stability

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    

def run_case(cfg, mode):
    x = simulate_system(cfg["system"])
    y = vision_measurement(x, cfg["sensing"], cfg[mode])
    x_est = reconstruct_state(y)
    A_list = estimate_dynamics(x_est, cfg["estimation"], cfg["system"])
    alpha = compute_stability(A_list, cfg["metrics"])

    return x, y, alpha


def run_experiment():

    # -------------------------
    # Base system config
    # -------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/vision.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)

    if "seed" in cfg:
        np.random.seed(cfg["seed"])
    
    # Run both
    x, y_good, alpha_good = run_case(cfg,"sensing_good")
    _, y_bad, alpha_bad = run_case(cfg,"sensing_bad")

    plot_vision_measurements(y_good,y_bad)
    plot_vision_stability(alpha_good,alpha_bad,cfg["estimation"]["window_pre"])


if __name__ == "__main__":
    run_experiment()