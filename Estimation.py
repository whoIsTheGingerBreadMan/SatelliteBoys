import numpy as np
from scipy.spatial import distance_matrix
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

import Environment
import Satellite
from distanceToLoc import get_predicted_distance
        
def EKF_filter(self):
    pass

def particle_filter(satellite_num, dt, x0, sig0, y_true, Q, R, N_pf, u, t):
    
    # initialize variables
    x_pf = np.zeros((n_total, t))
    x_pf[:, 0] = x0
    sig_pf = np.zeros((n_total, n_total, t))
    sig_pf[:, :, 0] = sig0
    w = np.zeros((N_pf, t))

    X = np.zeros((n_total, N_pf, t))
    X[:, :, 0] = np.transpose(np.random.multivariate_normal(x_pf[:, 0], sig_pf[:, :, 0], N_pf))
    w[:, 0] = np.squeeze(np.ones((N_pf, 1)) / N_pf)
    X_new = np.zeros((n_total, N_pf, t))
    y_est = np.zeros((satellite_num, satellite_num, N_pf, t))

    for k in range(t):
        # predict
        for i in range(N_pf):
            noise_w = Q * np.random.randn(n_total)
            X_new[:, i, k], _ = transition_dyn(X[:, i, k -1], v_init, dt, u) + noise_w

        # update
        for i in range(N_pf):
            y_est[:, :, i, k] = measurement(X_new[:, i, k], satellite_num, n)
            w[i, k] = multivariate_normal.pdf(np.reshape(y_true[:, :, k], (-1)),  np.reshape(y_est[:, :, i, k], (-1)), R)
            # w[i, k] = 1/np.sqrt((2*np.pi)**satellite_num * np.linalg.det(R)) * np.exp(-1/2* (D_matrix - D_gen).T.dot(np.linalg.inv(R)).dot(D_matrix - D_gen))
        
        # normalization
        w[:, k] = w[:, k] / np.sum(w[:, k])
        x_pf[:, k] = weighted_mean(w[:, k], X_new[:, :, k])
        # sig_pf[:, :, k] = weighted_cov(w[:, k], X_new[:, :, k], X_new[:, :, k], N_pf)
        X[:, :, k] = X_new[:, :, k]

        # resample
        idx = np.random.choice(N_pf, size=N_pf, replace=True, p=w[:, k])
        X[:, :, k] = X[:, idx, k]
        w[:, k] = np.ones((N_pf)) / N_pf

    return x_pf, sig_pf


def simulation_test(t, dt, x, v_init, y, satellite_num, n, Q, R, u):
    
    for i in range(1, t):
        x[:, i], _ = transition_dyn(x[:, i - 1], v_init, dt, u)
        x[:, i] += Q * np.random.randn(satellite_num * n)
        y[:, :, i] = measurement(x[:, i], satellite_num, n) + R * np.eye(satellite_num)

    return x, y 


def transition_dyn(x, v_init, dt, u):
    # Assumption: dt is small enough that the acceleration can be ignored
    # for mass in self.env.masses:
        # u += mass.get_acceleration(x_est)
    x += .5 * u * dt**2 + v_init * dt
    v_init += u * dt

    return x, v_init

def measurement(x, satellite_num, n):

    coordinates = np.zeros((satellite_num, n))
    coordinates[:, 0] = x[::2]
    coordinates[:, 1] = x[1::2]
    y = distance_matrix(coordinates, coordinates)

    return y

def weighted_mean(w, x):
    """
    Parameters: pass in one sample of x, with size of (n_total * N_pf) 
    where n_total is the dim of state variables and N_pf is the number of particles

    """
    w_mean = x.dot(w)

    return w_mean

def weighted_cov(w, x, y, N_pf):
    mu_x = weighted_mean(w, x)
    mu_y = weighted_mean(w, y)

    w_cov = (x - mu_x.dot(np.ones((1, N_pf)))).dot(np.diag(w)).dot(y - mu_y.odt(np.ones((1, N_pf))))

    return w_cov

def plot_trajectory(x_true, satellite_num):
    fig = plt.figure()
    x1_true = x_true[::2]
    x2_true = x_true[1::2]
    color = ('blue', 'green', 'red', 'black', 'purple')
    for i in range(satellite_num):
        plt.plot(x1_true[i, :], x2_true[i, :], color=color[i])
    plt.show()

if __name__ == "__main__":
    # constants
    dt = 0.1
    T = 10
    t = int(T / dt + 1)
    # num of state variables
    n = 2 
    satellite_num = 5
    n_total = int(satellite_num * n)
    # initialize velocity for all satellites
    v = 1
    v_init = v * np.random.randn((n_total))
    # process noise covariance
    Q = 0.05
    # measurement noise covariance
    R = 0.1
    # particle number
    N_pf = 1000

    # initialize variables
    x0 = np.array([0, 0, 1, 1, 0, 3, 2, 0, 1, 4])
    x0 = np.zeros((n_total))
    sig0 = np.eye(n_total)
    # true states
    x_true = np.zeros((n_total, t))
    x_true[:, 0] = x0
    u = np.zeros((n_total))
    # measurements - distance matrices
    y_true = np.zeros((satellite_num, satellite_num, t))
    
    # simulation 
    x_true, y_true = simulation_test(t, dt, x_true, v_init, y_true, satellite_num, n, Q, R, u)

    # particle filter
    x_pf, sig_pf = particle_filter(satellite_num, dt, x0, sig0, y_true, Q, R, N_pf, u, t)

    # plotting the trajectories
    plot_trajectory(x_true, satellite_num)
    plot_trajectory(x_pf, satellite_num)


    # noise_base = 30
    # coordinates = np.zeros((8, 3))
    # coordinates[:, :2] = noise_base * np.random.randn(10, 2)
    # x_true, y_true, x_new, y_new, D, D2, loss = get_predicted_distance(coordinates, noise=10)

    # fig, axes = plt.subplots(1, 3)
    # fig.set_size_inches((12, 12))
    # axes[0].scatter(x_new, y_new)
    # axes[0].set_title("prediction")
    # axes[1].set_title("true")
    # axes[2].set_title("together")
    # axes[2].scatter(x_true, y_true)
    # axes[2].scatter(x_new, y_new)
    # axes[0].set_aspect(1)
    # axes[1].set_aspect(1)
    # axes[2].set_aspect(1)
  







