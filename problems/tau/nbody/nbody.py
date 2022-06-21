#!/usr/bin/python3
from vpython import *
import numpy as np
import random
import matplotlib.pyplot as plt

def initial_cfg(n, dim):
    X = np.random.random((n,dim))
    V = np.zeros((n,dim), dtype=np.float)
    M = np.ones((n,), dtype=np.float) / n
    return M,X,V

def calc_interaction(M, X, eps):
    n,dim = X.shape
    assert(dim == 3), X.shape
    A = np.zeros((n,dim), dtype=np.float)
    U = 0.0
    for i in range(n):
        # i が全粒子から受ける加速度を計算
        dX = X[i] - X
        assert(dX.shape == (n,dim)), dX.shape
        l2 = np.linalg.norm(dX, axis=1) + eps*eps
        assert(l2.shape == (n,)), l2.shape
        l = np.sqrt(l2)
        assert(l.shape == (n,)), l.shape
        l3 = l2 * l
        assert(l3.shape == (n,)), l3.shape
        k = M / (l2 * l)
        assert(k.shape == (n,)), k.shape
        kdx = (k * dX.T).T
        assert(kdx.shape == (n,dim)), kdx.shape
        a = kdx.sum(axis=0)
        assert(a.shape == (dim,)), a.shape
        u = (M[i] * M / l).sum()
        U -= u
        A[i] = a
    return A,U

def calc_kinetic(M, V):
    return (0.5 * M * (V * V).sum(axis=1)).sum()

def make_pos(X):
    n,dim = X.shape
    return [ vector(X[i][0], X[i][1], X[i][2]) for i in range(n) ]

def main():
    rg = random.Random()
    n = 2
    dim = 3
    M,X,V = initial_cfg(n, dim)
    t = 0
    P = points(pos=make_pos(X))
    n_steps = 20
    eps = 1.0e-2
    dt = 1e-1
    n_steps = 10000
    Thist = []
    Uhist = []
    Khist = []
    KUhist = []
    for i in range(n_steps):
        A,U = calc_interaction(M, X, eps)
        K = calc_kinetic(M, V)
        KU = K + U
        Thist.append(t)
        Khist.append(K)
        Uhist.append(U)
        KUhist.append(KU)
        X += V * dt
        V += A * dt
        t += dt
        for i in range(n):
            P.point(i)["pos"] = vector(X[i][0], X[i][1], X[i][2])
        rate(int(1.0/dt))
    plt.plot(Thist, Uhist, label="U")
    plt.plot(Thist, Khist, label="K")
    plt.plot(Thist, KUhist, label="K+U")
    plt.legend(loc='upper left')
    plt.show()

main()

