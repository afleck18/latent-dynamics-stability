import numpy as np

def estimate_dynamics(x_est, cfg, sys_cfg):
    T = len(x_est)
    A_list = []

    for t in range(max(cfg["window_pre"], cfg["window_post"]), T-1):

        if t < sys_cfg["transition_time"]:
            window = cfg["window_pre"]
        else:
            window = cfg["window_post"]

        X = x_est[t-window:t]
        Y = x_est[t-window+1:t+1]

        XtX = X.T @ X
        XtY = X.T @ Y

        A_T = np.linalg.inv(XtX + cfg["lambda_reg"] * np.eye(np.shape(XtX)[0])) @ XtY
        A = A_T.T

        A_list.append(A)

    return A_list