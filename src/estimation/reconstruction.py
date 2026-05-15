import numpy as np

def reconstruct_state(y):

    if y.ndim == 1:
        x_est = np.zeros((len(y),2))
        x_est[:,0] = y
        x_est[1:,1] = y[1:] - y[:-1]

    else:
        dim = y.shape[1]

        x_est = np.zeros((len(y), 2 * dim))
        x_est[:, :dim] = y
        x_est[1:, dim:2*dim] = y[1:] - y[:-1]

    return x_est