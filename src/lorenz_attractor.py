import numpy as np
from scipy.integrate import odeint


def lorenz(X, t, sigma, beta, rho):
    u, v, w = X

    up = -sigma * (u - v)
    vp = rho * u - v - u * w
    wp = -beta * w + u * v

    return up, vp, wp


def calculate_lorenz(tmax=100, n_points=10000, sigma=10, beta=2.667, rho=28, u0=0, v0=1, w0=1.05):
    t = np.linspace(0, tmax, n_points)
    f = odeint(lorenz, (u0, v0, w0), t, args=(sigma, beta, rho))
    x, y, z = f.T

    return x, y, z
