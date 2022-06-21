

# partial derivative of scalar field f by x
def partial_x(f):
    return f[1:-1,1:-1] - f[0:-2,1:-1]

def partial_y(f):
    return f[1:-1,1:-1] - f[1:-1,0:-2]

def div(f, g):
    return partial_x(f) + partial_y(g)

def solve_poisson(p, f):
    # solve Δp = f
    # reflect boundary values
    f[0,:]  -= p[0,1:-1]
    f[-1,:] -= p[-1,1:-1]
    f[:,1]  -= p[1:-1,0]
    f[:,-1] -= p[1:-1,-1]
    m,n = p.shape
    N = (m - 1) * (n - 1)
    L = scipy.sparse.diags([-4.0,  1.0,  1.0,   1.0,  1.0  ], 
                           [   0,    1,   -1,     n,   -n  ], 
                           shape=(N,N))
    return scipy.sparse.linalg.solve(A, f.reshape(N))

def step(u, v, p, dt):
    c = 1
    # step 1: solve 
    #   Δp     = - ∇・(v・∇) v + c ∇・Δv + ∇・v / dt
    # x component of - (v・∇) v + c Δv
    rx = - (u[1:-1,1:-1] * partial_x(u) + v[1:-1,1:-1] * partial_y(u)) + c * lap(u)
    # y component of - (v・∇) v + c Δv
    ry = - (u[1:-1,1:-1] * partial_x(v) + v[1:-1,1:-1] * partial_y(v)) + c * lap(v)
    # - ∇・(v・∇)v + c ∇・Δv + ∇・v / dt
    rhs  = - div(rx, ry) + div(u, v)[1:-1,1:-1] / dt
    p[1:m-1,1:n-1] = solve_poisson(p, rhs)
    # step 2: evolve v with 
    #     v(t+dt) = v + (- (v・∇)v - ∇p + c Δv ) dt
    # x component: of - (v・∇)v - ∇p + c Δv 
    du_dt = - (u[1:-1,1:-1] * partial_x(u) + v[1:-1,1:-1] * partial_y(u)) - partial_x(p) + c * lap(u)
    # y component: of - (v・∇)v - ∇p + c Δv 
    dv_dt = - (u[1:-1,1:-1] * partial_x(v) + v[1:-1,1:-1] * partial_y(v)) - partial_y(p) + c * lap(v)
    # u += du/dt * dt
    # v += dv/dt * dt
    u[1:m-1,1:n-1] += du_dt * dt
    v[1:m-1,1:n-1] += dv_dt * dt
    
def main():
    m = 50
    n = 100
    dt = 0.01
    # u = x-coordinate of velocity field
    u = np.zeros((m, n))
    # v = y-coordinate of velocity field
    v = np.zeros((m, n))
    # pressure field
    p = np.zeros((m, n))
    for i in range(100):
        print("step %d" % i)
        step(u, v, p, dt)

main()
