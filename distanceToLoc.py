import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


# coordinates = np.zeros((10,3))


# coordinates[:,:2]= 30*np.random.randn(10,2)


def get_predicted(coordinates, noise=.2):
    X = (coordinates - coordinates[0])
    x_true, y_true, z_true = X.transpose()

    D = distance_matrix(coordinates, coordinates)

    M = np.inner(X, X)
    noise = noise * np.random.randn(*M.shape)
    noise = (noise + noise.transpose()) / 2
    w, v = np.linalg.eigh(M + noise)

    size = len(w)
    nd = coordinates.shape[1]
    vevs = np.arange(size - nd, size)[::-1]

    x_v = v[:, vevs]

    sqrt_s = np.expand_dims(np.sqrt(w[vevs]), 0)
    x_v = (sqrt_s * x_v)
    x, y, z = x_v.transpose()

    R, loss = Rotation.align_vectors(x_v, X)

    x_new, y_new, z_new = R.apply(x_v, inverse=True).transpose()

    return x_true, y_true, x_new, y_new, loss


def get_predicted_distance(coordinates, noise=0):
    X = (coordinates - coordinates[0])
    x_true, y_true, z_true = X.transpose()

    D2 = distance_matrix(coordinates, coordinates) ** 2

    M = np.zeros_like(D2)
    for i in range(10):
        for j in range(10):
            M[i, j] = (D2[0, j] + D2[i, 0] - D2[i, j]) / 2
            M[j, i] = M[i, j]

    noise = noise * np.random.randn(*M.shape)
    noise = (noise + noise.transpose()) / 2
    w, v = np.linalg.eigh(M + noise)

    size = len(w)
    nd = coordinates.shape[1]
    vevs = np.arange(size - nd, size)[::-1]

    x_v = v[:, vevs]

    sqrt_s = np.expand_dims(np.sqrt(w[vevs]), 0)
    x_v = (sqrt_s * x_v)
    x, y, z = x_v.transpose()

    R, loss = Rotation.align_vectors(x_v, X)
    x_new, y_new, z_new = R.apply(x_v, inverse=True).transpose()

    return x_true, y_true, x_new, y_new, loss



if __name__ == "__main__":
    noise_base = 30
    coordinates = np.zeros((10, 3))
    coordinates[:, :2] = noise_base * np.random.randn(10, 2)

    losses_a = []
    noise_vals = []
    increment = .2
    for i in range(200):
        losses_b = []
        noise_vals.append((i * increment) / noise_base)
        for _ in range(50):
            x_true, y_true, x_new, y_new, loss = get_predicted(coordinates, noise=i * increment)
            losses_b.append(loss)

        losses_a.append(np.mean(losses_b))

    plt.figure(figsize=(15, 15))
    plt.plot(np.array(noise_vals) / 30, losses_a)
    plt.show()


    noise_base = 30
    coordinates = np.zeros((10, 3))
    coordinates[:, :2] = noise_base * np.random.randn(10, 2)
    x_true, y_true, x_new, y_new, loss = get_predicted_distance(coordinates, noise=10)

    fig, axes = plt.subplots(1, 3)
    fig.set_size_inches((12, 12))
    axes[0].scatter(x_new, y_new)
    axes[0].set_title("prediction")
    axes[1].set_title("true")
    axes[2].set_title("together")
    axes[1].scatter(x_true, y_true)
    axes[2].scatter(x_true, y_true)
    axes[2].scatter(x_new, y_new)
    axes[0].set_aspect(1)
    axes[1].set_aspect(1)
    axes[2].set_aspect(1)
    plt.show()

