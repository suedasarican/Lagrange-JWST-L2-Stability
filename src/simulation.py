import numpy as np

def cr3bp_equations(t, state, mu):
    """ Hareket Denklemleri (CR3BP) """
    x, y, vx, vy = state
    r1 = np.sqrt((x + mu)**2 + y**2)
    r2 = np.sqrt((x - (1 - mu))**2 + y**2)
    
    omega_x = x - (1 - mu) * (x + mu) / r1**3 - mu * (x - 1 + mu) / r2**3
    omega_y = y - (1 - mu) * y / r1**3 - mu * y / r2**3
    
    ax = 2 * vy + omega_x
    ay = -2 * vx + omega_y
    return np.array([vx, vy, ax, ay])

def rk4_step(func, t, state, dt, mu):
    """ Runge-Kutta 4 Entegratörü """
    k1 = func(t, state, mu)
    k2 = func(t + 0.5*dt, state + 0.5*dt*k1, mu)
    k3 = func(t + 0.5*dt, state + 0.5*dt*k2, mu)
    k4 = func(t + dt, state + dt*k3, mu)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def run_mission_simulation(mu, initial_state, duration=3.2, dt=0.001):
    """ Simülasyonu çalıştırır ve veriyi döndürür """
    t = 0.0
    step_count = int(duration / dt)
    state = initial_state
    
    # Performans için NumPy dizileri
    x_vals = np.zeros(step_count)
    y_vals = np.zeros(step_count)
    
    for i in range(step_count):
        x_vals[i] = state[0]
        y_vals[i] = state[1]
        state = rk4_step(cr3bp_equations, t, state, dt, mu)
        t += dt
        
    return x_vals, y_vals