# Learning Stability from Partial Observations in Dynamical Systems
## Overview
This project demonstrates how to **infer time-varying system dynamics from partial, noisy observations** and use the learned dynamics to **detect the onset of instability**.

Rather than relying on full state access or predefined models, we estimate a local system operator directly from data and analyze its spectral properties over time.
## Core Idea
We consider a dynamical system with a **regime shift**:
* Early: stable (energy decays)
* Later: unstable (energy grows)

Only **partial observations** of the system are available.

We ask

&emsp;&emsp;Can we detect instability from incomplete measurements?
## Method
**1. Partial observation**
- Only a single state component is observed with noise

**2. State reconstruction (minimal)**
- Augment observations with a simple derivative-based estimate

**3. Local system identification**
- Estimate a time-varying linear operator A(t) using sliding-window regression

**4. Stability metric**
- Compute spectral radius:

$$
ρ(A(t))−1
$$

- Instability occurs when ρ(A)>1
## Results
### System Behavior
* Clear transition from stable to unstable dynamics
* Energy growth indicates loss of stability
### Stability Detection
* Learned operator tracks approach to instability
* Spectral radius approaches and slightly exceeds 1
* Statistical baselines (variance) fail to clearly capture the transition
## Key Insight
Instability can be detected from partial observations by analyzing the **spectral properties of learned local dynamics**, even when direct state access is unavailable.
## Why This Matters
This setup mirrors real-world systems where:
* full state is not observable
* dynamics change over time
* early detection of instability is critical

Examples include:
* geophysical systems
* navigation and sensing environments
* control systems under uncertain measurements
## Limitations (intentional and honest)
* Simple state reconstruction (not optimal)
* Linear local approximation
* Detection signal is subtle near marginal stability
## Future Directions
* Structured operator constraints (physics-informed)
* Robust estimation under noise
* Extension to higher-dimensional systems
* Integration with observer design