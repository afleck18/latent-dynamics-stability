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
    plt.savefig('results/system_dynamics.png')
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
    plt.savefig('results/instability_detection.png')
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
    plt.savefig('results/vision_measurements.png')
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
    plt.savefig('results/vision_stability.png')
    plt.show()
