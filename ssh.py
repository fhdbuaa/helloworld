# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def run(N):
    t = np.arange(0.0, N, 0.1)
    x = np.zeros(N * 10)
    vx = np.zeros(N * 10)
    ax = np.zeros(N * 10)
    y = np.zeros(N * 10)
    vy = np.zeros(N * 10)
    ay = np.zeros(N * 10)
    r = np.zeros(N * 10)
    G = 1
    m = 1
    d = 1

    def Acceleration(d, G, m):
        return -G * m / (d ** 2)

    x[0] = 0.5 * d
    vx[0] = -0.2 * d
    y[0] = 0.0 * d
    vy[0] = 1.63 * d
    r[0] = np.sqrt(x[0] ** 2 + y[0] ** 2)
    ax[0] = Acceleration(r[0], G, m) * x[0] / r[0]
    ay[0] = Acceleration(r[0], G, m) * y[0] / r[0]
    delta = 0.0001 / (np.sqrt(ax[0] ** 2 + ay[0] ** 2))
    for i in xrange(1, N * 10):
        vx[i] = vx[i - 1] + ax[i - 1] * delta
        vy[i] = vy[i - 1] + ay[i - 1] * delta
        x[i] = x[i - 1] + vx[i - 1] * delta
        y[i] = y[i - 1] + vy[i - 1] * delta
        r[i] = np.sqrt(x[i] ** 2 + y[i] ** 2)
        ax[i] = Acceleration(r[i], G, m) * x[i] / r[i]
        ay[i] = Acceleration(r[i], G, m) * y[i] / r[i]

    plt.title("Simulation Times: %d" % int(N * 10))
    plt.plot(x, y, '.')
    plt.show()


if __name__ == "__main__":
    run(20000)
