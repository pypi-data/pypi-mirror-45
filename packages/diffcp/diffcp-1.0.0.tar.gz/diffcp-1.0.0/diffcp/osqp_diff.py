import osqp
import numpy as np
import scipy as sp
import scipy.sparse as sparse
from scipy.sparse.linalg import lsqr
import IPython as ipy
import time

def solve_osqp(P, q, A, l, u, **kwargs):
    prob = osqp.OSQP()
    prob.setup(P=P, q=q, A=A, l=l, u=u, **kwargs)
    res = prob.solve()

    x = res.x
    y = res.y
    z = A @ res.x
    return x, y, z

def backward_osqp(dx, dy, dz, P, q, A, l, u, x, y, z, **kwargs):
    m, n = A.shape

    M = sparse.bmat([
        [P, A.T, None],
        [A, None, -sparse.eye(m)],
        [None, ((y > 0) * (z - u))[np.newaxis,:], np.maximum(y, 0)[np.newaxis,:]],
        [None, ((y < 0) * (z - l))[np.newaxis,:], np.minimum(y, 0)[np.newaxis,:]]
    ])

    dxtilde = np.concatenate([dx, dy, dz])
    xtilde = np.concatenate([x, y, z])

    sol = lsqr(M.T, dxtilde, **kwargs)[0]

    # dQ is equal to -np.outer(sol, xtilde). Instead of materializing this,
    # the below code only computes the entries needed to compute dP and dA.
    P_rows, P_cols = P.nonzero()

    P_values = - sol[P_rows] * xtilde[P_cols]
    dP = sparse.csc_matrix((P_values, (P_rows, P_cols)), shape=P.shape)

    A_rows, A_cols = A.nonzero()

    A_values = - sol[A_cols+n] * xtilde[A_rows] - sol[n + A_rows] * xtilde[A_cols]
    dA = sparse.csc_matrix((A_values, (A_rows, A_cols)), shape=A.shape)

    dq = - sol[:n]
    dl = sol[-1] * np.minimum(y, 0)
    du = sol[-2] * np.maximum(y, 0)

    return dP, dq, dA, dl, du

if __name__ == '__main__':
    # Generate problem data
    m = 50
    n = 30
    Ad = sparse.random(m, n, density=0.7, format='csc')
    b = np.random.randn(m)

    # OSQP data
    P = sparse.block_diag((sparse.csc_matrix((n, n)), sparse.eye(m)), format='csc')
    q = np.zeros(n+m)
    A = sparse.vstack([
            sparse.hstack([Ad, -sparse.eye(m)]),
            sparse.hstack((sparse.eye(n), sparse.csc_matrix((n, m))))
        ]).tocsc()
    l = np.hstack([b, np.zeros(n)])
    u = np.hstack([b, np.ones(n)])

    start = time.perf_counter()
    x, y, z = solve_osqp(P, q, A, l, u, eps_abs=1e-8, eps_rel=1e-8, verbose=False)
    end = time.perf_counter()
    print ("forward:", end-start)

    start = time.perf_counter()
    dP, dq, dA, dl, du = backward_osqp(P@x, np.zeros(y.size), np.zeros(z.size), P, q, A, l, u, x, y, z)
    end = time.perf_counter()
    print ("backward:", end-start)

    base = .5*x@P@x

    rows, cols = P.nonzero()
    values = np.random.uniform(-1e-5,1e-5, size=rows.size)
    P_change = sparse.csc_matrix((values, (rows, cols)), shape=P.shape)
    P_change = (P_change + P_change.T)/2
    l_change = np.random.uniform(-1e-5,0,size=y.size)
    u_change = np.random.uniform(0,1e-5,size=y.size)
    q_change = np.random.uniform(-1e-5,1e-5,size=x.size)
    rows, cols = A.nonzero()
    values = np.random.uniform(-1e-5,1e-5,size=rows.size)
    A_change = sparse.csc_matrix((values, (rows, cols)), shape=A.shape)
    x, y, z = solve_osqp(P+P_change, q+q_change, A+A_change, l+l_change, u+u_change, eps_abs=1e-8, eps_rel=1e-8, verbose=False)
    base_change = .5*x@P@x - base
    print (dq@q_change+(dP*P_change).sum()+(dA*A_change).sum()+dl@l_change+du@u_change, base_change)
