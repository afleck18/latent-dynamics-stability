import argparse
import yaml
import numpy as np

from src.simulation.dynamics import simulate_system
from src.sensing.direct import direct_measurement
from src.sensing.vision import vision_measurement
from src.estimation.reconstruction import reconstruct_state
from src.estimation.system_id import estimate_dynamics
from src.metrics.stability import compute_stability, compute_variance
from src.utils.plotting import plot_system, plot_detection, plot_vision_measurements, plot_vision_stability

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_experiment(cfg):
    x = simulate_system(cfg["system"])

    if cfg["sensing"]["type"] == "direct":
        y = [direct_measurement(x, cfg["sensing"])]
    elif cfg["sensing"]["type"] == "vision":
        y = [
            vision_measurement(x, cfg["sensing"], cfg["sensing_good"]),
            vision_measurement(simulate_system(cfg["system"]), cfg["sensing"], cfg["sensing_bad"])
        ]
    else:
        raise ValueError("Unknown sensing type")

    alpha = []
    variance = []
    for i in range(len(y)):
        x_est = reconstruct_state(y[i])
        A_list = estimate_dynamics(x_est, cfg["estimation"], cfg["system"])

        alpha.append(compute_stability(A_list, cfg["metrics"]))
        variance.append(compute_variance(y[i], cfg))
    
    return x, y, alpha, variance

def main(experiment):

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=f'configs/{experiment}.yaml')
    args = parser.parse_args()

    cfg = load_config(args.config)

    if "seed" in cfg:
        np.random.seed(cfg["seed"])

    x, y, alpha, variance = run_experiment(cfg)

    if cfg["sensing"]["type"] == "direct":
        plot_system(x)
        plot_detection(alpha[0],variance[0],cfg)
    
    if cfg["sensing"]["type"] == "vision":
        plot_vision_measurements(y[0],y[1])
        plot_vision_stability(alpha[0],alpha[1],cfg["estimation"]["window_pre"])

if __name__ == "__main__":
    ### vision or base ###
    main("vision")