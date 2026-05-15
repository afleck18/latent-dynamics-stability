import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# SYSTEM BEHAVIOR
# -------------------------

def plot_system(x):
    energy = np.linalg.norm(x, axis=1)

    plt.figure(figsize=(10, 4))

    plt.plot(x[:, 0], label="State (x₁)")
    plt.plot(energy, label="Energy ‖x‖", linewidth=2)
    plt.axvline(100, linestyle="--", label="Regime change")

    plt.title("System Transition: Stable → Unstable Dynamics")
    plt.xlabel("Time")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -------------------------
# DETECTION
# -------------------------

def plot_detection(alpha_smooth,variance,cfg):
    
    t_alpha = np.arange(cfg["estimation"]["window_pre"]+5, cfg["system"]["T"]-1)
    t_var = np.arange(cfg["estimation"]["window_pre"], cfg["system"]["T"])

    plt.figure(figsize=(10, 4))

    plt.plot(t_alpha, alpha_smooth, label="Stability (ρ(A) - 1)")
    plt.plot(t_var, variance, label="Variance (baseline)", alpha=0.7)

    plt.fill_between(t_alpha, alpha_smooth, 0, where=alpha_smooth > -0.05, alpha=0.2)
    plt.text(142, -0.35, r'Aproach to marginal stability ($\rho$(A) $\approx$ 1)')

    plt.axhline(0, linestyle="--")
    plt.axvline(100, linestyle="--")

    plt.title("Detection of Instability from Partial Observations")
    plt.xlabel("Time")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -------------------------
# Measurement quality
# -------------------------

def plot_vision_measurements(y_good,y_bad):
    plt.figure(figsize=(10,4))

    plt.plot(y_good[:,0], label="Good perception", alpha=0.8)
    plt.plot(y_bad[:,0], label="Poor perception", alpha=0.6)
    plt.axvline(100, linestyle="--")
    plt.axvspan(120,200,color='green', alpha=0.1)
    plt.text(133,22, "Measurement sensitive regime", fontsize=11)
    plt.annotate(
        "Divergence begins",
        xy=(130,2),
        xytext=(125,6),
        arrowprops=dict(arrowstyle="->")
    )
    plt.title("Vision Measurements (Image Plane)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -------------------------
# Plot 2: Stability comparison
# -------------------------

def plot_vision_stability(alpha_good,alpha_bad,window):

    t_alpha = np.arange(window, window + len(alpha_good))
    t_good = np.argmax(alpha_good > 0)
    t_bad  = np.argmax(alpha_bad > 0)

    plt.figure(figsize=(10,4))
    plt.scatter(t_good+window, alpha_good[t_good], label="Detection (good)")
    plt.scatter(t_bad+window, alpha_bad[t_bad], label="Detection (poor)")
    plt.plot(t_alpha, alpha_good, label="Good perception")
    plt.plot(t_alpha, alpha_bad, label="Poor perception")
    plt.fill_between(t_alpha, alpha_bad, 0, alpha=0.15)
    plt.axhline(0, linestyle="--",linewidth=1.5,alpha=0.8)
    plt.axvline(100, linestyle="--")
    plt.annotate(
        "Delayed detection under poor perception",
        xy=(t_bad+window+2, -0.01),
        xytext=(t_bad+window-10, -.12),
        arrowprops=dict(arrowstyle="->")
    )
    plt.annotate(
        "Uncertain stability estimation",
        xy=(135, -0.02),
        xytext=(145,-0.03),
        arrowprops=dict(arrowstyle="->")
    )
    plt.title("Effect of Measurement Quality on Stability Estimation")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_trajectory(log, R_safe):
    x_true = np.array([l["x_true"] for l in log])
    x_ekf = np.array([l["x_ekf"] for l in log])
    meas = np.array([l["measurement"] for l in log])

    plt.figure(figsize=(6,6))

    # trajectories
    plt.plot(x_true[:,0], x_true[:,1], 'k--', label="True")
    plt.plot(x_ekf[:,0], x_ekf[:,1], 'b', label="EKF")
    plt.scatter(meas[:,0], meas[:,1], s=10, alpha=0.3, label="Measurements")

    # safe region
    circle = plt.Circle((0,0), R_safe, color='green', fill=False, linestyle='--')
    plt.gca().add_patch(circle)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Trajectory and Safe Region")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_uncertainty(log):
    u_ekf = [l["uncertainty_ekf"] for l in log]
    u_ours = [l["uncertainty_ours"] for l in log]

    plt.figure(figsize=(8,4))

    plt.plot(u_ekf, label="EKF uncertainty", linewidth=2)
    plt.plot(u_ours, label="Residual uncertainty", linewidth=2)

    plt.xlabel("Time")
    plt.ylabel("Uncertainty")
    plt.title("Uncertainty Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_risk(log, threshold=1.0):
    risk_ekf = [l["risk_ekf"] for l in log]
    risk_ours = [l["risk_ours"] for l in log]

    plt.figure(figsize=(10,5))

    plt.plot(risk_ekf, label="EKF risk", linewidth=2)
    plt.plot(risk_ours, label="Residual risk", linewidth=2)

    # threshold
    plt.axhline(threshold, linestyle="--", color="red", label="Risk threshold")

    # highlight dangerous region
    risk_ours = np.array(risk_ours)
    plt.fill_between(
        range(len(risk_ours)),
        threshold,
        risk_ours,
        where=(risk_ours > threshold),
        alpha=0.2
    )

    plt.xlabel("Time")
    plt.ylabel("Risk")
    plt.title("Risk Evolution (Failure Detection)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_stability(log):
    for l in log:
        print(l)
    stability = [l["stability"] for l in log]
    quality = [l["measurement_quality"] for l in log]

    fig, ax1 = plt.subplots(figsize=(10,4))

    ax1.plot(stability, label="Stability", color='blue')
    ax1.axhline(0, linestyle="--", color="black")

    ax2 = ax1.twinx()
    ax2.plot(quality, label="Measurement quality", color='orange', alpha=0.7)

    ax1.set_xlabel("Time")
    ax1.set_ylabel("Stability")
    ax2.set_ylabel("Measurement quality")

    plt.title("Stability vs Measurement Quality")
    fig.tight_layout()
    plt.show()